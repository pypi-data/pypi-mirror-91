#!c:/SDK/Anaconda2/python.exe
from __future__ import print_function
import sys
try:
    from . proxy_tester import proxy_tester
except:
    from proxy_tester import proxy_tester
import progressbar
from pydebugger.debug import debug
from make_colors import make_colors
import requests

if sys.version_info.major == 3:
    raw_input = input
    from urllib.parse import urlparse
else:
    from urlparse import urlparse

    
def auto(session, url, func = None, no_verify = False, all = False, http = False, https = False, max_try = 10, limit=0, by_status_code = None):
    #ERROR = False
    slimit = 0
    proxy = []
    scheme = urlparse(url).scheme    
    prefix = '{variables.task} >> {variables.subtask}'
    variables =  {'task': '--', 'subtask': '--'}
    max_value = 10
    bar = progressbar.ProgressBar(max_value = max_value, prefix = prefix, variables = variables)
    pc = proxy_tester()
    n_try = 1
    list_proxy = pc.getProxyList()
    while 1:
        bar.max_value = len(list_proxy)
        c = ''
        for i in list_proxy:
            debug(use_proxy = i)
            proxies = {}
            proxy_str = ''
            #bar.update(bar.value + 1, task = make_colors("Get Proxy", 'black', 'lightyellow'), subtask = make_colors(proxies.get(scheme), 'lightwhite', 'lightblue') + " ")
            if no_verify:
                if all:
                    if https:
                        proxies.update({
                            'https': 'https://' + str(i.get('ip') + ":" + i.get('port')),
                        })
                        proxy_str = 'https://' + str(i.get('ip') + ":" + i.get('port'))
                    elif http:
                        proxies.update({
                            'http': 'http://' + str(i.get('ip') + ":" + i.get('port')),
                        })
                        proxy_str = 'http://' + str(i.get('ip') + ":" + i.get('port'))                                    
                    else:
                        proxies.update({
                            'https': 'https://' + str(i.get('ip') + ":" + i.get('port')),
                                        'http': 'http://' + str(i.get('ip') + ":" + i.get('port')),
                        })
                        proxy_str = str(i.get('ip') + ":" + i.get('port'))
                else:
                    if i.get('https') == 'yes':
                        if http:
                            proxies.update({
                                'http': 'http://' + str(i.get('ip') + ":" + i.get('port')),
                                            #'http': 'http://' + str(i.get('ip') + ":" + i.get('port')),
                            })
                            proxy_str = 'http://' + str(i.get('ip') + ":" + i.get('port'))
                        else:
                            proxies.update({
                                'https': 'https://' + str(i.get('ip') + ":" + i.get('port')),
                                            #'http': 'http://' + str(i.get('ip') + ":" + i.get('port')),
                            })
                            proxy_str = 'https://' + str(i.get('ip') + ":" + i.get('port'))
                    else:
                        if https:
                            proxies.update({'https': 'https://' + str(i.get('ip') + ":" + i.get('port')),})
                            proxy_str = 'https://' + str(i.get('ip') + ":" + i.get('port'))                                        
                        else:
                            proxies.update({'http': 'http://' + str(i.get('ip') + ":" + i.get('port')),})
                            proxy_str = 'http://' + str(i.get('ip') + ":" + i.get('port'))
                bar.update(n_try, task = make_colors("Check Proxy", 'black', 'lightgreen'), subtask = make_colors(i.get('ip') + ":" + i.get('port'), 'lightwhite', 'lightblue') + " ")
                try:
                    req_test = requests.request('GET', url, proxies=proxies, verify=False, timeout=3)
                    debug(proxies = proxies)
                    #print("\n")
                    #print(make_colors("Use proxy: ", 'lightyellow') + make_colors(proxies.get(scheme), 'lightwhite', 'blue'))
                    bar.update(n_try, task = make_colors("Try Proxy", 'lightwhite', 'lightred'), subtask = make_colors(proxy_str, 'lightwhite', 'lightblue') + " ")
                    session.proxies = proxies
                    if func:
                        c = func()
                    if by_status_code:
                        if req_test.status_code <= int(by_status_code):
                            if len(proxy) > 1 and not proxy[-1] == proxies:
                                proxy.append(proxies)
                    else:
                        if len(proxy) > 1 and not proxy[-1] == proxies:
                            proxy.append(proxies)
                    
                    if limit > 0:
                        if slimit == limit:
                            return session, proxy
                        else:
                            slimit += 1
                    break
                    
                except:
                    bar.max_value = len(list_proxy)
                    bar.value = n_try
                    #bar.value + 1

                debug(n_try = n_try)
                if n_try == len(list_proxy):
                    break
                else:
                    n_try += 1                            
            else:
                if scheme == 'https' and i.get('https') == 'yes':
                    proxies = {scheme: str(scheme + "://" + i.get('ip') + ":" + i.get('port')),}
                    bar.update(n_try, task = make_colors("Match Proxy", 'black', 'lightgreen'), subtask = make_colors(proxies.get(scheme), 'lightwhite', 'lightblue') + " ")
                    try:
                        req_test = requests.request('GET', url, proxies=proxies, verify=False, timeout=3)
                        #print("\n")
                        #print(make_colors("Use proxy: ", 'lightyellow') + make_colors(proxies.get(scheme), 'lightwhite', 'blue'))
                        bar.update(n_try, task = make_colors("Try Proxy", 'lightwhite', 'lightred'), subtask = make_colors(proxies.get(scheme), 'lightwhite', 'lightblue') + " ")
                        debug(proxies = proxies)
                        session.proxies = proxies
                        if func:
                            c = func()
                        
                        if by_status_code:
                            if req_test.status_code <= int(by_status_code):
                                if len(proxy) > 1 and not proxy[-1] == proxies:
                                    proxy.append(proxies)
                        else:
                            if len(proxy) > 1 and not proxy[-1] == proxies:
                                proxy.append(proxies)
                        if limit > 0:
                            if slimit == limit:
                                return session, proxy
                            else:
                                slimit += 1
                        break
                    except:
                        bar.max_value = len(list_proxy)
                        bar.value = n_try
                else:
                    bar.value + 1
                debug(n_try = n_try)
                if n_try == len(list_proxy):
                    break
                else:
                    n_try += 1

        if n_try == len(list_proxy):
            bar.finish()
            if len(proxy) == 0:
                print("\n")
                print(make_colors("[ERROR] No Proxy is Matched !", 'lightwhite', 'lightred', ['blink']))
            break                    
        if c:
            break   
        #if not ERROR:
        #    break
    #else:
        #debug(proxy = proxy)
        #if proxy:
        #    session.proxies = proxy
        #bar.max_value = max_try
        #if func:
        #    c = func()
        #if not c:
        #    sys.exit(make_colors("[ERROR CONNECTION]", 'lightwhite', 'lightred') + make_colors('Try Again !', 'black', 'lightyellow'))
            
    return session, proxy


def test(url, limit = 0):
    session = requests.Session()
    a, list_proxy = auto(session, url, func = None, no_verify = False, all = False, http = False, https = False, max_try = 10, limit=limit, by_status_code = 350)
    b = a.get(url)
    print("List Proxy =", list_proxy)
    print("STATUS :", b.status_code)
    
if __name__ == '__main__':
    test(sys.argv[1], limit = 5)