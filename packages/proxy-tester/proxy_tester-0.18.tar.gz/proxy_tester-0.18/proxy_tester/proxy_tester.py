#!c:/SDK/Anaconda2/python.exe
#encoding:utf-8
import requests
from bs4 import BeautifulSoup as bs
from pydebugger.debug import debug
from make_colors import make_colors
import os
import sys
if sys.version_info.major == 3:
	from urllib.parse import urlparse
else:
	from urlparse import urlparse
import configset
import warnings
from parserheader.parserheader import parserheader
if sys.version_info.major == 3:
	from fake_headers import Headers

warnings.filterwarnings("ignore")

class proxy_tester(object):
	URL = "https://free-proxy-list.net/anonymous-proxy.html"
	test_url = None
	configname = os.path.join(os.path.dirname(__file__), 'proxy_tester.ini')
	CONFIG = configset.configset(configname)

	def __init__(self, test_url=None):
		super(proxy_tester, self)
		if test_url:
			self.test_url = test_url
		# self.URL = "https://free-proxy-list.net/anonymous-proxy.html"
		# self.configname = os.path.join(os.path.dirname(__file__), 'proxy_tester.ini')
		# self.CONFIG = configset.configset(self.configname)
		

	@classmethod
	def getProxyList(self, url=None):
		if not url:
			url = self.URL
		while 1:
			try:
				a = requests.get(url)
				print("\n")
				break
			except:
				sys.stdout.write(".")
		b = bs(a.content, 'lxml')
		proxylisttable = b.find('table', {'id':'proxylisttable'}).find('tbody')
		# debug(proxylisttable=proxylisttable)
		proxylisttable_tr = proxylisttable.find_all('tr')
		# debug(proxylisttable_tr=proxylisttable_tr)
		proxy_list = []
		for i in proxylisttable_tr:
			all_td = i.find_all('td')
			# debug(all_td=all_td)
			# for t in all_td:
			data = {}
			ip = all_td[0].text
			port = all_td[1].text
			cd = all_td[2].text
			ct = all_td[3].text
			tp = all_td[4].text
			gs = all_td[5].text
			hs = all_td[6].text
			ls = all_td[7].text
			data.update({'ip':ip, 'port':port, 'code':cd, 'country':ct, 'anonimity':tp, 'google_support':gs, 'type':hs, 'last_checked':ls})
			# debug(data=data)
			proxy_list.append(data)
		debug(proxy_list=proxy_list)

		return proxy_list

	@classmethod
	def getProxyList2(self, page=None):
		user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.27 Safari/537.36 OPR/74.0.3904.0"
		if sys.version_info.major == 3:
			h = Headers()
			user_agent = h.generate()['User-Agent']
		headers_str = """Host: hidemy.name
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: {0}  
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: navigate
Sec-Fetch-Dest: document
Referer: https://www.google.com/
Accept-Encoding: gzip
Accept-Language: en-US,en;q=0.9""".format(user_agent)
		
		
		ph = parserheader()
		headers = ph.parserHeader(headers_str)
		debug(headers = headers)
		
		data = []
		url = "https://hidemy.name/en/proxy-list/"
		# https://hidemy.name/en/proxy-list/?start=64
		if page and str(page).isdigit():
			if int(page) > 1:
				url = "https://hidemy.name/en/proxy-list/?start={}".format(int(page)*64)
		a = requests.get(url, headers = headers)
		content = a.content
		# debug(content = content, debug = True)
		b = bs(content, 'lxml')
		table_block = b.find('div', {'class':'table_block'})
		# debug(table_block = table_block, debug = True)
		if not table_block:
			return []
		data_proxy = table_block.find('tbody')
		all_tr = data_proxy.find_all('tr')
		for i in all_tr:
			data_add = {}
			all_td = i.find_all('td')
			ip = all_td[0].text
			port = all_td[1].text
			ct = all_td[2].find('span', {'class':'country'}).text # + "/" + all_td[3].find('span', {'class':'city'}).text
			sp = all_td[3].find('p').text
			tp = all_td[4].text.lower()
			an = all_td[5].text.lower()
			ls = all_td[6].text
			data_add.update({'ip':ip, 'port':port, 'country':ct, 'type':tp, 'speed':sp, 'anonimity':an, 'last_checked':ls})
			data.append(data_add)
		debug(data = data)

		return data

	def test_proxy_ip(self, test_url=None, timeout=3, server_url=None, verbose=None, type = 1, print_list=True, limit=0):
		timeout = float(timeout)
		list_ok = []
		debug(test_url=test_url)
		debug(timeout=timeout)
		if not test_url:
			test_url = self.test_url
		if not test_url:
			print(make_colors("No Test URL", 'lightwhite', 'lightred', attrs=['blink']))
			return False
		if str(type) == '2':
			lists = self.getProxyList2(server_url)
		else:
			lists = self.getProxyList(server_url)
		for i in lists:
			if urlparse(test_url).scheme == 'https' and i.get('https') == 'yes':
				proxies = {'http': 'http://%s:%s'%(i.get('ip'), i.get('port')), 'https':'https://%s:%s'%(i.get('ip'), i.get('port'))}
			else:
				proxies = {'http': 'http://%s:%s'%(i.get('ip'), i.get('port'))}

			debug(proxies=proxies)
			try:
				a = requests.request('GET', test_url, proxies=proxies, verify=False, timeout=timeout)
				if print_list:
					print(make_colors('TEST PROXY: ', 'lightwhite', 'lightred') + make_colors('%s'%(i.get('ip')), 'lightcyan') + ":" + make_colors('%s'%(i.get('port')), 'lightyellow') + " [" + make_colors("OK", 'black', 'lightgreen') + "] [" + make_colors(str(a.status_code), 'lightwhite', 'lightblue') + "]")
				list_ok.append(i.get('ip')+":"+i.get('port'))
				if limit:
					if limit == len(list_ok):
						break
				if verbose:
					print("STATUS:", a.status_code)
			except:
				if verbose:
					print("STATUS:", "ERROR")
		self.CONFIG.write_config('OK', 'proxy', value="\n".join(list_ok))
		return list_ok

	def usage(self):
		import argparse
		parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument('URL', help='URL to tester', action='store')
		parser.add_argument('-z', '--timeout', help='Timeout for checking', action='store', default=3)
		parser.add_argument('-l', '--load-config', help='Check Proxy list on config first', action='store_true')
		parser.add_argument('-v', '--verbose', help='Show process checking', action='store_true')
		parser.add_argument('-t', '--type', action = 'store', help = 'Type Proxy "1" or "2", default: "1"', type=int, default = 1)
		if len(sys.argv) == 1:
			parser.print_help()
		else:
			args = parser.parse_args()
			self.test_proxy_ip(args.URL, args.timeout, None, args.verbose, type = args.type)


def usage():
	c = proxy_tester()
	c.usage()

if __name__ == '__main__':
	PID = os.getpid()
	print("PID =", PID)
	c = proxy_tester()
	# c.getProxyList()
	# data = c.getProxyList2()
	# print(data)
	# print(len(data))
	# c.test_proxy_ip(*sys.argv[1:])
	c.usage()