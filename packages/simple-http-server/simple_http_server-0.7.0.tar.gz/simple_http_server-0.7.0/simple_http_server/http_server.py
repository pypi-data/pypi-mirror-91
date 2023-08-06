# -*- coding: utf-8 -*-

"""
Copyright (c) 2018 Keijack Wu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import os
import re
import json
import ssl as _ssl
import inspect
import threading
import http.cookies as cookies
import http.server
import datetime

from collections import OrderedDict
from socketserver import ThreadingMixIn
from urllib.parse import unquote
from urllib.parse import quote
from typing import Callable, Dict, List, Tuple

from simple_http_server import ModelDict, RegGroup, RegGroups, HttpError, StaticFile, \
    Headers, Redirect, Response, Cookies, Cookie, JSONBody, Header, Parameters, PathValue, \
    Parameter, MultipartFile, Request, Session, ControllerFunction, version, _get_session_factory
from simple_http_server._http_session_local_impl import SESSION_COOKIE_NAME

from simple_http_server.logger import get_logger

_logger = get_logger("simple_http_server.http_server")


class RequestWrapper(Request):

    def __init__(self):
        super().__init__()
        self._headers_keys_in_lowcase = {}
        self._path = ""
        self.__session = None

    def get_session(self, create: bool = False) -> Session:
        if not self.__session:
            sid = self.cookies[SESSION_COOKIE_NAME].value if SESSION_COOKIE_NAME in self.cookies.keys() else ""
            session_fac = _get_session_factory()
            self.__session = session_fac.get_session(sid, create)
        return self.__session


class ResponseWrapper(Response):
    """ """

    def __init__(self, handler,
                 status_code=200,
                 headers=None):
        super(ResponseWrapper, self).__init__(status_code=status_code, headers=headers, body="")
        self.__req_handler = handler
        self.__is_sent = False
        self.__send_lock__ = threading.Lock()

    @property
    def is_sent(self) -> bool:
        return self.__is_sent

    def send_error(self, status_code: int, message: str = "") -> None:
        self.status_code = status_code
        msg = message if message is not None else ""
        self.body = {"error": msg}
        self.send_response()

    def send_redirect(self, url: str) -> None:
        self.status_code = 302
        self.set_header("Location", url)
        self.body = None
        self.send_response()

    def send_response(self) -> None:
        with self.__send_lock__:
            self.__send_response()

    def __send_response(self):
        assert not self.__is_sent, "This response has benn sent"
        self.__is_sent = True
        self.__req_handler._send_response({
            "status_code": self.status_code,
            "headers": self.headers,
            "cookies": self.cookies,
            "body": self.body
        })


class FilterContex:
    """Context of a filter"""

    def __init__(self, req, res, controller: ControllerFunction, filters=None):
        self.__request = req
        self.__response = res
        self.__controller: ControllerFunction = controller
        self.__filters = filters if filters is not None else []

    @property
    def request(self) -> Request:
        return self.__request

    @property
    def response(self) -> Response:
        return self.__response

    def _run_ctroller(self):
        args = self.__prepare_args()
        kwargs = self.__prepare_kwargs()

        if kwargs is None:
            ctr_res = self.__controller.func(*args)
        else:
            ctr_res = self.__controller.func(*args, **kwargs)
        return ctr_res

    def do_chain(self):
        if self.response.is_sent:
            return
        if len(self.__filters) == 0:

            ctr_res = self._run_ctroller()

            session = self.request.get_session()
            if session and session.is_valid:
                exp = datetime.datetime.utcfromtimestamp(session.last_acessed_time + session.max_inactive_interval)
                sck = Cookies()
                sck[SESSION_COOKIE_NAME] = session.id
                sck[SESSION_COOKIE_NAME]["httponly"] = True
                sck[SESSION_COOKIE_NAME]["path"] = "/"
                sck[SESSION_COOKIE_NAME]["expires"] = exp.strftime(Cookies.EXPIRE_DATE_FORMAT)
                self.response.cookies.update(sck)
            elif session and SESSION_COOKIE_NAME in self.request.cookies:
                exp = datetime.datetime.utcfromtimestamp(0)
                sck = Cookies()
                sck[SESSION_COOKIE_NAME] = session.id
                sck[SESSION_COOKIE_NAME]["httponly"] = True
                sck[SESSION_COOKIE_NAME]["path"] = "/"
                sck[SESSION_COOKIE_NAME]["expires"] = exp.strftime(Cookies.EXPIRE_DATE_FORMAT)
                self.response.cookies.update(sck)

            if ctr_res is not None:
                if isinstance(ctr_res, tuple):
                    status, headers, cks, body = self.__decode_tuple_response(ctr_res)
                    self.response.status_code = status if status is not None else self.response.status_code
                    self.response.body = body if body is not None else self.response.body
                    self.response.add_headers(headers)
                    self.response.cookies.update(cks)
                elif isinstance(ctr_res, Response):
                    self.response.status_code = ctr_res.status_code
                    self.response.body = ctr_res.body
                    self.response.add_headers(ctr_res.headers)
                elif isinstance(ctr_res, Redirect):
                    self.response.send_redirect(ctr_res.url)
                elif isinstance(ctr_res, int) and ctr_res >= 200 and ctr_res < 600:
                    self.response.status_code = ctr_res
                elif isinstance(ctr_res, Headers):
                    self.response.add_headers(ctr_res)
                elif isinstance(ctr_res, cookies.BaseCookie):
                    self.response.cookies.update(ctr_res)
                else:
                    self.response.body = ctr_res

            if self.request.method.upper() == "HEAD":
                self.response.body = None
            if not self.response.is_sent:
                self.response.send_response()
        else:
            func = self.__filters[0]
            self.__filters = self.__filters[1:]
            func(self)

    def __decode_tuple_response(self, ctr_res):
        status_code = None
        headers = Headers()
        cks = cookies.SimpleCookie()
        body = None
        for item in ctr_res:
            if isinstance(item, int):
                if status_code is None:
                    status_code = item
            elif isinstance(item, Headers):
                headers.update(item)
            elif isinstance(item, cookies.BaseCookie):
                cks.update(item)
            elif type(item) in (str, dict, StaticFile, bytes):
                if body is None:
                    body = item
        return status_code, headers, cks, body

    def __prepare_args(self):
        args = _get_args_(self.__controller.func)
        arg_vals = []
        if len(args) > 0:
            ctr_obj = self.__controller.ctrl_object
            if ctr_obj is not None:
                arg_vals.append(self.__controller.ctrl_object)
                args = args[1:]
        for arg, arg_type_anno in args:
            if arg not in self.request.parameter.keys() \
                    and arg_type_anno not in (Request, Session, Response, RegGroups, RegGroup, Headers, cookies.BaseCookie, cookies.SimpleCookie, Cookies, PathValue, JSONBody, ModelDict):
                raise HttpError(400, f"Parameter[{arg}] is required! ")
            param = self.__get_params_(arg, arg_type_anno)
            arg_vals.append(param)

        return arg_vals

    def __get_params_(self, arg, arg_type, val=None, type_check=True):
        if val is not None:
            kws = {"val": val}
        else:
            kws = {}

        if arg_type == Request:
            param = self.request
        elif arg_type == Session:
            param = self.request.get_session(True)
        elif arg_type == Response:
            param = self.response
        elif arg_type == Headers:
            param = Headers(self.request.headers)
        elif arg_type == RegGroups:
            param = RegGroups(self.request.reg_groups)
        elif arg_type == Header:
            param = self.__build_header(arg, **kws)
        elif inspect.isclass(arg_type) and issubclass(arg_type, cookies.BaseCookie):
            param = self.request.cookies
        elif arg_type == Cookie:
            param = self.__build_cookie(arg, **kws)
        elif arg_type == MultipartFile:
            param = self.__build_multipart(arg, **kws)
        elif arg_type == Parameter:
            param = self.__build_param(arg, **kws)
        elif arg_type == PathValue:
            param = self.__build_path_value(arg, **kws)
        elif arg_type == Parameters:
            param = self.__build_params(arg, **kws)
        elif arg_type == RegGroup:
            param = self.__build_reg_group(**kws)
        elif arg_type == JSONBody:
            param = self.__build_json_body()
        elif arg_type == str:
            param = self.__build_str(arg, **kws)
        elif arg_type == bool:
            param = self.__build_bool(arg, **kws)
        elif arg_type == int:
            param = self.__build_int(arg, **kws)
        elif arg_type == float:
            param = self.__build_float(arg, **kws)
        elif arg_type in (list, List, List[str], List[Parameter], List[int], List[float], List[bool], List[dict], List[Dict]):
            param = self.__build_list(arg, target_type=arg_type, **kws)
        elif arg_type == ModelDict:
            param = self.__build_model_dict()
        elif arg_type in (dict, Dict):
            param = self.__build_dict(arg, **kws)
        elif type_check:
            raise HttpError(400, f"Parameter[{arg}] with Type {arg_type} is not supported yet.")
        else:
            param = val
        return param

    def __build_reg_group(self, val: RegGroup = RegGroup(group=0)):
        if val.group >= len(self.request.reg_groups):
            raise HttpError(400, f"RegGroup required an element at {val.group}, but the reg length is only {len(self.request.reg_groups)}")
        return RegGroup(group=val.group, _value=self.request.reg_groups[val.group])

    def __build_model_dict(self):
        mdict = ModelDict()
        for k, v in self.request.parameters.items():
            if len(v) == 1:
                mdict[k] = v[0]
            else:
                mdict[k] = v
        return mdict

    def __prepare_kwargs(self):
        kwargs = _get_kwargs_(self.__controller.func)
        if kwargs is None:
            return None
        kwarg_vals = {}
        for k, v, t in kwargs:
            kwarg_vals[k] = self.__get_params_(k, type(v) if v is not None else t, v, False)

        return kwarg_vals

    def __build_path_value(self, key, val=PathValue()):
        name = val.name if val.name is not None and val.name != "" else key
        if name in self.request.path_values:
            return PathValue(name=name, _value=self.request.path_values[name])
        else:
            raise HttpError(500, f"path name[{name}] not in your url mapping!")

    def __build_cookie(self, key, val=None):
        name = val.name if val.name is not None and val.name != "" else key
        if val._required and name not in self.request.cookies:
            raise HttpError(400, f"Cookie[{name}] is required.")
        if name in self.request.cookies:
            morsel = self.request.cookies[name]
            cookie = Cookie()
            cookie.set(morsel.key, morsel.value, morsel.coded_value)
            cookie.update(morsel)
            return cookie
        else:
            return val

    def __build_multipart(self, key, val=MultipartFile()):
        name = val.name if val.name is not None and val.name != "" else key
        if val._required and name not in self.request.parameter.keys():
            raise HttpError(400, f"Parameter[{name}] is required.")
        if name in self.request.parameter.keys():
            v = self.request.parameter[key]
            if isinstance(v, MultipartFile):
                return v
            else:
                raise HttpError(400, f"Parameter[{name}] should be a file.")
        else:
            return val

    def __build_dict(self, key, val={}):
        if key in self.request.parameter.keys():
            try:
                return json.loads(self.request.parameter[key])
            except:
                raise HttpError(400, f"Parameter[{key}] should be a JSON string.")
        else:
            return val

    def __build_list(self, key, target_type=list, val=[]):
        if key in self.request.parameters.keys():
            ori_list = self.request.parameters[key]
        else:
            ori_list = val

        if target_type == List[int]:
            try:
                return [int(p) for p in ori_list]
            except:
                raise HttpError(400, f"One of the parameter[{key}] is not int. ")
        elif target_type == List[float]:
            try:
                return [float(p) for p in ori_list]
            except:
                raise HttpError(400, f"One of the parameter[{key}] is not float. ")
        elif target_type == List[bool]:
            return [p.lower() not in ("0", "false", "") for p in ori_list]
        elif target_type in (List[dict], List[Dict]):
            try:
                return [json.loads(p) for p in ori_list]
            except:
                raise HttpError(400, f"One of the parameter[{key}] is not JSON string. ")
        elif target_type == List[Parameter]:
            return [Parameter(name=key, default=p, required=False) for p in ori_list]
        else:
            return ori_list

    def __build_float(self, key, val=None):
        if key in self.request.parameter.keys():
            try:
                return float(self.request.parameter[key])
            except:
                raise HttpError(400, f"Parameter[{key}] should be an float. ")
        else:
            return val

    def __build_int(self, key, val=None):
        if key in self.request.parameter.keys():
            try:
                return int(self.request.parameter[key])
            except:
                raise HttpError(400, f"Parameter[{key}] should be an int. ")
        else:
            return val

    def __build_bool(self, key, val=None):
        if key in self.request.parameter.keys():
            v = self.request.parameter[key]
            return v.lower() not in ("0", "false", "")
        else:
            return val

    def __build_str(self, key, val=None):
        if key in self.request.parameter.keys():
            return Parameter(name=key, default=self.request.parameter[key], required=False)
        elif val is None:
            return None
        else:
            return Parameter(name=key, default=val, required=False)

    def __build_json_body(self):
        if "content-type" not in self.request._headers_keys_in_lowcase.keys() or \
                not self.request._headers_keys_in_lowcase["content-type"].lower().startswith("application/json"):
            raise HttpError(400, 'The content type of this request must be "application/json"')
        return JSONBody(self.request.json)

    def __build_header(self, key, val=Header()):
        name = val.name if val.name is not None and val.name != "" else key
        if val._required and name not in self.request.headers:
            raise HttpError(400, f"Header[{name}] is required.")
        if name in self.request.headers:
            v = self.request.headers[name]
            return Header(name=name, default=v, required=val._required)
        else:
            return val

    def __build_params(self, key, val=Parameters()):
        name = val.name if val.name is not None and val.name != "" else key
        if val._required and name not in self.request.parameters:
            raise HttpError(400, f"Parameter[{name}] is required.")
        if name in self.request.parameters:
            v = self.request.parameters[name]
            return Parameters(name=name, default=v, required=val._required)
        else:
            return val

    def __build_param(self, key, val=Parameter()):
        name = val.name if val.name is not None and val.name != "" else key
        if val._required and name not in self.request.parameter:
            raise HttpError(400, f"Parameter[{name}] is required.")
        if name in self.request.parameter:
            v = self.request.parameter[name]
            return Parameter(name=name, default=v, required=val._required)
        else:
            return val


def _get_args_(func):
    argspec = inspect.getfullargspec(func)
    # ignore first argument like `self` or `clz` in object methods or class methods
    start = 1 if inspect.ismethod(func) else 0
    if argspec.defaults is None:
        args = argspec.args[start:]
    else:
        args = argspec.args[start: len(argspec.args) - len(argspec.defaults)]
    arg_turples = []
    for arg in args:
        if arg in argspec.annotations:
            ty = argspec.annotations[arg]
        else:
            ty = str
        arg_turples.append((arg, ty))
    return arg_turples


def _get_kwargs_(func):
    argspec = inspect.getfullargspec(func)
    if argspec.defaults is None:
        return None

    kwargs = OrderedDict(zip(argspec.args[-len(argspec.defaults):], argspec.defaults))
    kwarg_turples = []
    for k, v in kwargs.items():
        if k in argspec.annotations:
            k_anno = argspec.annotations[k]
        else:
            k_anno = str
        kwarg_turples.append((k, v, k_anno))
    return kwarg_turples


def _remove_url_first_slash(url):
    _url = url
    while _url.startswith("/"):
        _url = url[1:]
    return _url


class _SimpleDispatcherHttpRequestHandler(http.server.BaseHTTPRequestHandler):
    """The Class will dispatch the request to the controller configured in RequestMapping"""

    server_version = f"python-simple-http-server/{version}"

    def version_string(self):
        return self.server_version

    def __process(self, method):
        mth = method.upper()

        req = self.__prepare_request(mth)
        path = req._path

        ctrl, req.path_values, req.reg_groups = self.server.get_url_controller(path, mth)

        res = ResponseWrapper(self)
        if ctrl is None:
            res.status_code = 404
            res.body = {"error": "Cannot find a controller for your path"}
            res.send_response()
        else:
            filters = self.server.get_matched_filters(req.path)
            ctx = FilterContex(req, res, ctrl, filters)
            try:
                ctx.do_chain()
            except HttpError as e:
                res.status_code = e.code
                res.body = {"error": e.message}
                res.send_response()
            except Exception as e:
                _logger.exception("error occurs! returning 500")
                res.status_code = 500
                res.body = {"error":  str(e)}
                res.send_response()

    def __prepare_request(self, method) -> RequestWrapper:
        path = self.__get_path(self.path)
        req = RequestWrapper()
        req.path = "/" + path

        req._path = path
        headers = {}
        _headers_keys_in_lowers = {}
        for k in self.headers.keys():
            headers[k] = self.headers[k]
            _headers_keys_in_lowers[k.lower()] = self.headers[k]
        req.headers = headers
        req._headers_keys_in_lowcase = _headers_keys_in_lowers

        # cookies
        if "cookie" in _headers_keys_in_lowers.keys():
            req.cookies.load(_headers_keys_in_lowers["cookie"])

        req.method = method
        query_string = self.__get_query_string(self.path)

        req.parameters = self.__decode_query_string(query_string)

        if "content-length" in _headers_keys_in_lowers.keys():
            req.body = self.rfile.read(int(_headers_keys_in_lowers["content-length"]))
            self.rfile.close()
            content_type = _headers_keys_in_lowers["content-type"]
            if content_type.lower().startswith("application/x-www-form-urlencoded"):
                data_params = self.__decode_query_string(req.body.decode("UTF-8"))
            elif content_type.lower().startswith("multipart/form-data"):
                data_params = self.__decode_multipart(content_type, req.body.decode("ISO-8859-1"))
            elif content_type.lower().startswith("application/json"):
                req.json = json.loads(req.body.decode("UTF-8"))
                data_params = {}
            else:
                data_params = {}
            req.parameters = self.__merge(data_params, req.parameters)
        return req

    def __merge(self, dic0, dic1):
        """Merge tow dictionaries of which the structure is {k:[v1, v2]}"""
        dic = dic1
        for k, v in dic0.items():
            if k not in dic.keys():
                dic[k] = v
            else:
                for i in v:
                    dic[k].append(i)
        return dic

    def __get_query_string(self, ori_path):
        parts = ori_path.split('?')
        if len(parts) == 2:
            return parts[1]
        else:
            return ""

    def __get_path(self, ori_path):
        path = ori_path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = _remove_url_first_slash(path)
        return path

    def __decode_multipart(self, content_type, data):
        boundary = "--" + content_type.split("; ")[1].split("=")[1]
        fields = data.split(boundary)
        # ignore the first empty row and the last end symbol
        fields = fields[1: len(fields) - 1]
        params = {}
        for field in fields:
            # trim the first and the last empty row
            f = field[field.index("\r\n") + 2: field.rindex("\r\n")]
            key, val = self.__decode_multipart_field(f)
            self.__put_to(params, key, val)
        return params

    def __decode_multipart_field(self, field):
        # first line: Content-Disposition
        line, rest = self.__read_line(field)

        kvs = self.__decode_content_disposition(line)
        kname = kvs["name"].encode("ISO-8859-1").decode("UTF-8")
        if len(kvs) == 1:
            # this is a string field, the second line is an empty line, the rest is the value
            val = self.__read_line(rest)[1].encode("ISO-8859-1").decode("UTF-8")
        elif len(kvs) == 2:
            filename = kvs["filename"].encode("ISO-8859-1").decode("UTF-8")
            # the second line is Content-Type line
            ct_line, rest = self.__read_line(rest)
            content_type = ct_line.split(":")[1].strip()
            # the third line is an empty line, the rest is the value
            content = self.__read_line(rest)[1].encode("ISO-8859-1")

            val = MultipartFile(kname, filename=filename, content_type=content_type, content=content)
        else:
            val = "UNKNOWN"

        return kname, val

    def __decode_content_disposition(self, line):
        cont_dis = {}
        es = line.split(";")[1:]
        for e in es:
            k, v = self.__break(e.strip(), "=")
            cont_dis[k] = v[1: -1]  # ignore the '"' symbol
        return cont_dis

    def __read_line(self, txt):
        return self.__break(txt, "\r\n")

    def __break(self, txt, separator):
        try:
            idx = txt.index(separator)
            return txt[0: idx], txt[idx + len(separator):]
        except ValueError:
            return txt, None

    def __decode_query_string(self, query_string):
        params = {}
        if not query_string:
            return params
        pairs = query_string.split("&")
        for item in pairs:
            key, val = self.__break(item, "=")
            if val is None:
                val = ""
            self.__put_to(params, unquote(key), unquote(val))

        return params

    def __put_to(self, params, key, val):
        if key not in params.keys():
            params[key] = [val]
        else:
            params[key].append(val)

    def _send_response(self, response):
        headers = response["headers"]
        cks = response["cookies"]

        status_code, content_type, body = self.__prepare_res_body(response)

        if "Content-Type" not in headers.keys() and "content-type" not in headers.keys():
            headers["Content-Type"] = content_type

        self.send_response(status_code)
        self.send_header("Last-Modified", str(self.date_time_string()))
        for k, v in headers.items():
            if isinstance(v, str):
                self.send_header(k, v)
            elif isinstance(v, list):
                for iov in v:
                    if isinstance(iov, str):
                        self.send_header(k, iov)

        for k in cks:
            ck = cks[k]
            self.send_header("Set-Cookie", ck.OutputString())

        if body is None:
            self.send_header("Content-Length", 0)
            self.end_headers()
        elif isinstance(body, str):
            data = body.encode("utf-8")
            self.send_header("Content-Length", len(data))
            self.end_headers()
            self.wfile.write(data)

        elif isinstance(body, bytes):
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)
        elif isinstance(body, StaticFile):
            file_size = os.path.getsize(body.file_path)
            self.send_header("Content-Length", file_size)
            self.end_headers()
            buffer_size = 1024 * 1024  # 1M
            with open(body.file_path, "rb") as in_file:
                data = in_file.read(buffer_size)
                while data:
                    self.wfile.write(data)
                    data = in_file.read(buffer_size)

    def __prepare_res_body(self, response: Response):
        status_code = response["status_code"]
        raw_body = response["body"]
        content_type = "text/plain; chartset=utf8"
        if raw_body is None:
            body = ""
        elif isinstance(raw_body, dict):
            content_type = "application/json; charset=utf8"
            body = json.dumps(raw_body, ensure_ascii=False)
        elif isinstance(raw_body, str):
            body = raw_body.strip()
            if body.startswith("<?xml") and body.endswith(">"):
                content_type = "text/xml; charset=utf8"
            elif body.lower().startswith("<!doctype html") and body.endswith(">"):
                content_type = "text/html; charset=utf8"
            elif body.lower().startswith("<html") and body.endswith(">"):
                content_type = "text/html; charset=utf8"
            else:
                content_type = "text/plain; charset=utf8"
        elif isinstance(raw_body, StaticFile):
            if not os.path.isfile(raw_body.file_path):
                _logger.error(f"Cannot find file[{raw_body.file_path}] specified in StaticFile body.")
                status_code = 404
                content_type = "application/json; charset=utf8"
                body = json.dumps({
                    "error": "Cannot find file for this url."
                }, ensure_ascii=False)
            else:
                body = raw_body
                content_type = body.content_type
        elif isinstance(raw_body, bytes):
            body = raw_body
            content_type = "application/octet-stream"
        else:
            body = raw_body
        return status_code, content_type, body

    def do_method(self, method):
        self.__process(method)

    def do_OPTIONS(self):
        self.do_method("OPTIONS")

    def do_GET(self):
        self.do_method("GET")

    def do_HEAD(self):
        self.do_method("HEAD")

    def do_POST(self):
        self.do_method("POST")

    def do_PUT(self):
        self.do_method("PUT")

    def do_DELETE(self):
        self.do_method("DELETE")

    def do_TRACE(self):
        self.do_method("TRACE")

    def do_CONNECT(self):
        self.do_method("CONNECT")

    # @override
    def log_message(self, format, *args):
        _logger.info(f"{self.client_address[0]} - {format % args}")


class _HttpServerWrapper(http.server.HTTPServer):

    HTTP_METHODS = ["OPTIONS", "GET", "HEAD", "POST", "PUT", "DELETE", "TRACE", "CONNECT"]

    def __init__(self, addr, res_conf={}):
        super(_HttpServerWrapper, self).__init__(addr, _SimpleDispatcherHttpRequestHandler)
        self.method_url_mapping: Dict[str, Dict[str, ControllerFunction]] = {"_": {}}
        self.path_val_url_mapping: Dict[str, Dict[str, ControllerFunction]] = {"_": OrderedDict()}
        self.method_regexp_mapping: Dict[str, Dict[str, ControllerFunction]] = {"_": OrderedDict()}
        for mth in _HttpServerWrapper.HTTP_METHODS:
            self.method_url_mapping[mth] = {}
            self.path_val_url_mapping[mth] = OrderedDict()
            self.method_regexp_mapping[mth] = OrderedDict()

        self.filter_mapping = OrderedDict()
        self._res_conf = []
        self.add_res_conf(res_conf)

    @property
    def res_conf(self):
        return self._res_conf

    @res_conf.setter
    def res_conf(self, val: Dict[str, str]):
        self._res_conf.clear()
        self.add_res_conf(val)

    def add_res_conf(self, val):
        if not val or not isinstance(val, dict):
            return
        for res_k, v in val.items():
            if res_k.startswith("/"):
                k = res_k[1:]
            else:
                k = res_k
            if k.endswith("/*"):
                key = k[0:-1]
            elif k.endswith("/**"):
                key = k[0:-2]
            elif k.endswith("/"):
                key = k
            else:
                key = k + "/"

            if v.endswith(os.path.sep):
                val = v
            else:
                val = v + os.path.sep
            self._res_conf.append((key, val))
        self._res_conf.sort(key=lambda it: -len(it[0]))

    def __get_path_reg_pattern(self, url):
        _url: str = url
        path_names = re.findall("(?u)\\{\\w+\\}", _url)
        if len(path_names) == 0:
            # normal url
            return None, path_names
        for name in path_names:
            _url = _url.replace(name, "([\\w%.-@!\\(\\)\\[\\]\\|\\$]+)")
        _url = f"^{_url}$"

        quoted_names = []
        for name in path_names:
            name = name[1: -1]
            quoted_names.append(quote(name))
        return _url, quoted_names

    def map_url(self, ctrl: ControllerFunction):
        url = ctrl.url
        regexp = ctrl.regexp
        method = ctrl.method
        _logger.debug(f"map url {url}|{regexp} with method[{method}] to function {ctrl.func}. ")
        assert method is None or method == "" or method.upper() in _HttpServerWrapper.HTTP_METHODS
        _method = method.upper() if method is not None and method != "" else "_"
        if regexp:
            self.method_regexp_mapping[_method][regexp] = ctrl
        else:
            _url = _remove_url_first_slash(url)

            path_pattern, path_names = self.__get_path_reg_pattern(_url)
            if path_pattern is None:
                self.method_url_mapping[_method][_url] = ctrl
            else:
                self.path_val_url_mapping[_method][path_pattern] = (ctrl, path_names)

    def _res_(self, path, res_pre, res_dir):
        fpath = os.path.join(res_dir, path.replace(res_pre, ""))
        _logger.debug(f"static file. {path} :: {fpath}")
        fext = os.path.splitext(fpath)[1]
        ext = fext.lower()
        if ext in (".html", ".htm", ".xhtml"):
            content_type = "text/html"
        elif ext == ".xml":
            content_type = "text/xml"
        elif ext == ".css":
            content_type = "text/css"
        elif ext in (".jpg", ".jpeg"):
            content_type = "image/jpeg"
        elif ext == ".png":
            content_type = "image/png"
        elif ext == ".webp":
            content_type = "image/webp"
        elif ext == ".js":
            content_type = "text/javascript"
        elif ext == ".pdf":
            content_type = "application/pdf"
        elif ext == ".mp4":
            content_type = "video/mp4"
        elif ext == ".mp3":
            content_type = "audio/mp3"
        else:
            content_type = "application/octet-stream"

        return StaticFile(fpath, content_type)

    def get_url_controller(self, path="", method="") -> Tuple[Callable, Dict, List]:
        # explicitly url matching
        if path in self.method_url_mapping[method]:
            return self.method_url_mapping[method][path], {}, ()
        elif path in self.method_url_mapping["_"]:
            return self.method_url_mapping["_"][path], {}, ()

        # url with path value matching
        fun_and_val = self.__try_get_from_path_val(path, method)
        if fun_and_val is None:
            fun_and_val = self.__try_get_from_path_val(path, "_")
        if fun_and_val is not None:
            return fun_and_val[0], fun_and_val[1], ()

        # regexp
        func_and_groups = self.__try_get_from_regexp(path, method)
        if func_and_groups is None:
            func_and_groups = self.__try_get_from_regexp(path, "_")
        if func_and_groups is not None:
            return func_and_groups[0], {}, func_and_groups[1]
        # static files
        for k, v in self.res_conf:
            if path.startswith(k):
                def static_fun():
                    return self._res_(path, k, v)
                return static_fun, {}, ()
        return None, {}, ()

    def __try_get_from_regexp(self, path, method):
        for regex, ctrl in self.method_regexp_mapping[method].items():
            m = re.match(regex, path)
            _logger.debug(f"regexp::pattern::[{regex}] => path::[{path}] match? {m is not None}")
            if m:
                return ctrl, tuple([unquote(v) for v in m.groups()])
        return None

    def __try_get_from_path_val(self, path, method):
        for patterns, val in self.path_val_url_mapping[method].items():
            m = re.match(patterns, path)
            _logger.debug(f"url with path value::pattern::[{patterns}] => path::[{path}] match? {m is not None}")
            if m:
                fun, path_names = val
                path_values = {}
                for idx in range(len(path_names)):
                    key = unquote(path_names[idx])
                    path_values[key] = unquote(m.groups()[idx])
                return fun, path_values
        return None

    def map_filter(self, path_pattern, filter_fun):
        self.filter_mapping[path_pattern] = filter_fun

    def get_matched_filters(self, path):
        available_filters = []
        for key, val in self.filter_mapping.items():
            if re.match(key, path):
                available_filters.append(val)
        return available_filters


class _ThreadingHttpServer(ThreadingMixIn, _HttpServerWrapper):
    pass


class SimpleDispatcherHttpServer(object):
    """Dispatcher Http server"""

    def map_filter(self, path_pattern, filter_fun):
        self.server.map_filter(path_pattern, filter_fun)

    def map_request(self, ctrl: ControllerFunction):
        self.server.map_url(ctrl)

    def __init__(self,
                 host: Tuple[str, int] = ('', 9090),
                 ssl: bool = False,
                 ssl_protocol: int = _ssl.PROTOCOL_TLS_SERVER,
                 ssl_check_hostname: bool = False,
                 keyfile: str = "",
                 certfile: str = "",
                 keypass: str = "",
                 multithread: bool = True,
                 ssl_context: _ssl.SSLContext = None,
                 resources: Dict[str, str] = {}):
        self.host = host
        self.multithread = multithread
        self.ssl = ssl
        if self.multithread:
            self.server = _ThreadingHttpServer(self.host, res_conf=resources)
        else:
            self.server = _HttpServerWrapper(self.host, res_conf=resources)

        if ssl:
            if ssl_context:
                ssl_ctx = ssl_context
            else:
                assert keyfile and certfile, "keyfile and certfile should be provided. "
                ssl_ctx = _ssl.SSLContext(protocol=ssl_protocol)
                ssl_ctx.check_hostname = ssl_check_hostname
                ssl_ctx.load_cert_chain(certfile=certfile, keyfile=keyfile, password=keypass)
            self.server.socket = ssl_ctx.wrap_socket(
                self.server.socket,
                server_side=True
            )

    def resources(self, res={}):
        self.server.res_conf = res

    def start(self):
        if self.ssl:
            ssl_hint = " with SSL on"
        else:
            ssl_hint = ""
        _logger.info(f"Dispatcher Http Server starts. Listen to port [{self.host[1]}]{ssl_hint}.")
        self.server.serve_forever()

    def shutdown(self):
        # server must shutdown in a separate thread, or it will be deadlocking...WTF!
        t = threading.Thread(target=self.server.shutdown)
        t.daemon = True
        t.start()
