"""A conversion module for googletrans"""
import json

def format_querystringlang():
    querystring = {
        "client":"te",
    }
    return querystring

def format_querystring(token, text, src='auto', dest='en'):
    querystring = {
        "anno":"3",
        "format":"html",
        "key":"",
        "logld":"vTE_20201130_00",
        "client":"te",
        "v":"1.0",
        "sl": src,
        "tl": dest,
        "tk": token,
        "q": text.encode('utf-8'),
        "tc":"1",
        "sr":"1",
        "mode":"1"
    }
    return querystring


def format_param(rpcids):
    params = {
        'rpcids': rpcids,
        'bl': 'boq_translate-webserver_20201207.13_p0', 
        'soc-app': 1, 'soc-platform': 1, 
        'soc-device': 1, 
        'rt': 'c'
    }
    return params


def format_data(rpcids, text, src, dest):
        return {'f.req': json.dumps([[
            [
                rpcids,
                json.dumps([[text, src, dest, True],[None]], separators=(',', ':')),
                None,
                'generic',
            ],
        ]], separators=(',', ':'))}


def format_response(a):
    result = {}
    b = a.split('\n')
    li_filter = []
    flag = False
    for _b in b:
        if _b.isnumeric():
            flag = not flag
            _b = ''
        if flag:
            li_filter.append(_b)
    fi_data = str(''.join(li_filter)).replace('"[', '[').replace(']"', ']').replace('\\n', '').replace('\\','')
    li_data = json.loads(fi_data.replace('"[', '[').replace(']"', ']'))
    return li_data
    