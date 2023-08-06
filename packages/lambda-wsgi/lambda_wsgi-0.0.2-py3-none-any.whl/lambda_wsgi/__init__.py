from base64 import b64decode, b64encode
from collections import defaultdict
from io import BytesIO
from os import getenv
from sys import stderr
from urllib.parse import quote, unquote

_headers_mv = lambda ev: {k.lower(): ','.join(v) for k, v in ev['multiValueHeaders'].items()}
_qs_mv = lambda ev, quote=lambda v: v: '&'.join([
    '&'.join([f'{quote(k)}={quote(v)}' for v in vs])
    for k, vs in (ev['multiValueQueryStringParameters'] or {}).items()
])
_set_cookie = 'set-cookie Set-cookie sEt-cookie SEt-cookie seT-cookie SeT-cookie sET-cookie SET-cookie set-Cookie Set-Cookie sEt-Cookie SEt-Cookie seT-Cookie SeT-Cookie sET-Cookie SET-Cookie set-cOokie Set-cOokie sEt-cOokie SEt-cOokie seT-cOokie SeT-cOokie sET-cOokie SET-cOokie set-COokie Set-COokie sEt-COokie SEt-COokie seT-COokie SeT-COokie sET-COokie SET-COokie set-coOkie Set-coOkie sEt-coOkie SEt-coOkie seT-coOkie SeT-coOkie sET-coOkie SET-coOkie set-CoOkie Set-CoOkie sEt-CoOkie SEt-CoOkie seT-CoOkie SeT-CoOkie sET-CoOkie SET-CoOkie set-cOOkie Set-cOOkie sEt-cOOkie SEt-cOOkie seT-cOOkie SeT-cOOkie sET-cOOkie SET-cOOkie set-COOkie Set-COOkie sEt-COOkie SEt-COOkie seT-COOkie SeT-COOkie sET-COOkie SET-COOkie'


def _req_api(ev):
    req_ctx = ev['requestContext']
    stage = req_ctx['stage']

    method = req_ctx.get('httpMethod') or req_ctx['http']['method']  # v1 or v2
    path = req_ctx['path'] if 'path' in req_ctx else req_ctx['http']['path']  # v1 or v2
    script = ''
    if stage != '$default':
        script = f'/{stage}'
        path = path[len(script):]
    return {
        'method': method,
        'path': path,
        'script': script
    }


def _req_alb(ev):
    script = getenv('SCRIPT_NAME', '')
    return {
        'method': ev['httpMethod'],
        'path': unquote(ev['path'])[len(script):],
        'script': script
    }


def _environ(req, ev, ctx):
    headers = req['headers']
    body = (b64decode if ev['isBase64Encoded'] else str.encode)(ev.get('body') or '')
    environ = {f'HTTP_{k.upper().replace("-", "_")}': v for k, v in headers.items()}
    environ.update({
        'CONTENT_LENGTH': headers.get('content-length', 0),
        'CONTENT_TYPE': headers.get('content-type', ''),
        'PATH_INFO': req['path'].encode().decode('latin1'),
        'QUERY_STRING': req['qs'],
        'REMOTE_ADDR': headers['x-forwarded-for'].split(',')[-1].strip(),  # need to check via cloudfront
        'REQUEST_METHOD': req['method'],
        'SCRIPT_NAME': req['script'],
        'SERVER_NAME': headers['host'],
        'SERVER_PORT': headers['x-forwarded-port'],
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'this.context': ctx,
        'this.event': ev,
        'wsgi.errors': stderr,
        'wsgi.input': BytesIO(body),
        'wsgi.multiprocess': False,
        'wsgi.multithread': False,
        'wsgi.run_once': False,
        'wsgi.url_scheme': headers['x-forwarded-proto'],
        'wsgi.version': (1, 0)
    })
    return environ


def _rsp(app, req, ev, ctx):
    def start_rsp(status, rsp_headers):
        rsp['statusCode'] = int(status.split(' ')[0])
        rsp['statusDescription'] = status
        headers = defaultdict(list)
        for k, v in rsp_headers:
            headers[k.lower()].append(v)

        if req['_mv']:  # api v1 / alb mv
            rsp['multiValueHeaders'] = headers

        else:  # api v2 / alb
            cookies = headers.pop('set-cookie', [])
            headers = {k: ','.join(v) for k, v in headers.items()}
            headers.update({k: v for k, v in zip(_set_cookie.split(' '), cookies)})
            rsp['headers'] = headers

    rsp = {'isBase64Encoded': True}
    rsp['body'] = b64encode(b''.join(app(_environ(req, ev, ctx), start_rsp)))
    return rsp


def make_handler(app):
    def handler(ev, ctx):
        ver = ev.get('version')

        if ver == '1.0':  # api v1
            req = _req_api(ev)
            req.update({
                '_mv': True,
                'headers': _headers_mv(ev),
                'qs': _qs_mv(ev, quote)
            })
            if '.amazonaws.com' not in req['headers']['host']:
                ev_path, req_path = ev['path'].split('/'), req['path'].split('/')
                if len(ev_path) > len(req_path):
                    req['script'] = f'/{ev_path[1]}'

        elif ver == '2.0':  # api v2
            req = _req_api(ev)
            req.update({
                '_mv': False,
                'headers': {**ev['headers'], **{'cookie': ';'.join(ev.get('cookies', []))}},
                'qs': ev['rawQueryString']
            })
            if '.amazonaws.com' not in req['headers']['host']:
                req['script'] = getenv('SCRIPT_NAME', '')

        elif 'headers' in ev:  # alb
            req = _req_alb(ev)
            req.update({
                '_mv': False,
                'headers': ev['headers'],
                'qs': '&'.join([f'{k}={v}' for k, v in ev['queryStringParameters'].items()])
            })

        else:  # alb mv
            req = _req_alb(ev)
            req.update({
                '_mv': True,
                'headers': _headers_mv(ev),
                'qs': _qs_mv(ev)
            })

        rsp = _rsp(app, req, ev, ctx)
        return rsp

    return handler
