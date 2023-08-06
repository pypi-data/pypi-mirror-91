#encoding:utf-8
#!/usr/bin/python2
import requests
from bs4 import BeautifulSoup as bs
from debug import debug
from make_colors import make_colors
import os
import sys
import urlparse
import configset
import re
import parserheader

class proxy_tester(object):
	def __init__(self, test_url=None):
		super(proxy_tester, self)
		self.test_url = test_url
		self.URL = "http://www.freeproxylists.net/"
		self.CONFIG = configset.configset()
		self.CONFIG.configname = os.path.join(os.path.dirname(__file__), 'proxy_tester2.ini')
		self.proxy = {}

	def setProtocol(self, protocol, params):
		"""
			- protocol_name: HTTP, HTTPS, ALL
		"""
		if protocol.lower() == 'http':
			params.update({'pt':'HTTP'})
		elif protocol.lower() == 'https':
			params.update({'pt':'HTTPS'})
		elif protocol.lower() == 'all':
			params.update({'pt':''})
		return params

	def setPort(self, port, params):
		params.update({'pr':str(port)})

	def setAnonimity(self, anonymity, params):
		"""
			- anonimity: NONE, ANONYMOUSE, HIGH_ANONYMOUSE
		"""
		if anonymity.lower() == 'none':
			params.update({'a[]':0})
		if anonymity.lower() == 'anonymouse':
			params.update({'a[]':1})
		if anonymity.lower() == 'high_anonymouse':
			params.update({'a[]':2})
		if isinstance(anonimity, list):
			params = ''
			data_str = str(anonimity)
			if hasattr(re.search('NONE', data_str, re.I), 'group'):
				params += 'a[]=0&'
			if hasattr(re.search('ANONYMOUSE', data_str, re.I), 'group'):
				params += 'a[]=1&'
			if hasattr(re.search('HIGH_ANONYMOUSE', data_str, re.I), 'group'):
				params += 'a[]=2&'
			# else:
			# 	params = 'a[]=0&a[]=1&a[]=2'
		return params

	def setUptime(self, uptime, params):
		if int(uptime) < 10:
			params.update({'u':0})
		elif int(uptime) < 20 and int(uptime) >= 10:
			params.update({'u':10})
		elif int(uptime) < 30 and int(uptime) >= 20:
			params.update({'u':30})
		elif int(uptime) < 40 and int(uptime) >= 30:
			params.update({'u':40})
		elif int(uptime) < 50 and int(uptime) >= 40:
			params.update({'u':50})
		elif int(uptime) < 60 and int(uptime) >= 50:
			params.update({'u':60})
		elif int(uptime) < 70 and int(uptime) >= 60:
			params.update({'u':70})
		elif int(uptime) < 80 and int(uptime) >= 70:
			params.update({'u':80})
		elif int(uptime) < 90 and int(uptime) >= 80:
			params.update({'u':90})
		elif int(uptime) <= 100 and int(uptime) >= 90:
			params.update({'u':100})
		else:
			params.update({'u':0})
		return params

	def checkPage(self, b=None, url=None, headers=None, proxies=None):
		if not b:
			if not url:
				url = self.URL
			while 1:
				try:
					a = requests.get(url, headers=headers, proxies=proxies)
					debug(a_url=a.url)
					debug(content=a.content)
					print "\n"
					break
				except:
					sys.stdout.write("۞")
			b = bs(a.content, 'lxml')
		return b.find('div', {'class':'page'})

	def setProxy(self, ip_port):
		pass

	def getPage(self):
		checkpage = self.checkPage(headers=self.setHeaders())
		page = []
		next_page = ""
		if checkpage:
			b = checkpage.find_all('a')
			for i in b:
				p = page.append(i.text)
				if p.isdigit():
					page.append(int(p))
				else:
					next = i.get('href')
		page = list(set(page))
		debug(page=page)
		debug(next_page=next_page)
		return page, next_page

	def setHeaders(self, headers_strings=None):
		if not headers_strings:
			headers_strings = """Host: www.freeproxylists.net
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://www.freeproxylists.net/
Connection: keep-alive
Cookie: hl=en; pv=9; userno=20181212-007950; from=google; refdomain=www.google.com; visited=2018%2F12%2F12+16%3A32%3A39
Upgrade-Insecure-Requests: 1"""
		return parserheader.parserHeader(headers_strings)

	def getProxyList(self, url=None, page=None, port=None, protocol=None, anonymity=None, uptime=None):
		params = {}

		if not url:
			url = self.URL
		while 1:
			try:
				a = requests.get(url)
				print "\n"
				break
			except:
				sys.stdout.write("۞")
		b = bs(a.content, 'lxml')
		proxylisttable = b.find('table', {'class':'DataGrid'}).find('tbody')
		# debug(proxylisttable=proxylisttable)
		proxylisttable_tr = proxylisttable.find_all('tr')
		# debug(proxylisttable_tr=proxylisttable_tr)
		n = 1
		proxy_list = []
		for i in proxylisttable_tr[1:]:
			all_td = i.find_all('td')
			# debug(all_td=all_td)
			# for t in all_td:
			data = {}
			ip = all_td[0].text.find(a).text
			port = all_td[1].text
			protocol = all_td[2].text
			anonymity = all_td[3].text
			country = all_td[4].get('img').text
			region = all_td[5].text
			city = all_td[6].text
			uptime = all_td[7].text

			data.update({'ip':ip, 'port':port, 'protocol':protocol, 'anonymity':anonymity, 'country':country, 'region':region, 'city':city, 'uptime':uptime})
			# debug(data=data)
			proxy_list.append(data)
		debug(proxy_list=proxy_list)

		return proxy_list

	def test_proxy_ip(self, test_url=None, timeout=3, server_url=None, verbose=None):
		timeout = float(timeout)
		list_ok = []
		debug(test_url=test_url)
		debug(timeout=timeout)
		if not test_url:
			test_url = self.test_url
		if not test_url:
			print make_colors("No Test URL", 'lightwhite', 'lightred', attrs=['blink'])
			return False
		lists = self.getProxyList(server_url)
		for i in lists:
			if urlparse.urlparse(test_url).scheme == 'https' and i.get('https') == 'yes':
				proxies = {'http': 'http://%s:%s'%(i.get('ip'), i.get('port')), 'https':'https://%s:%s'%(i.get('ip'), i.get('port'))}
			else:
				proxies = {'http': 'http://%s:%s'%(i.get('ip'), i.get('port'))}

			debug(proxies=proxies)
			try:
				a = requests.request('GET', test_url, proxies=proxies, verify=False, timeout=timeout)
				print make_colors('TEST PROXY: ', 'lightwhite', 'lightred') + make_colors('%s'%(i.get('ip')), 'lightcyan') + ":" + make_colors('%s'%(i.get('port')), 'lightyellow') + " [" + make_colors("OK", 'black', 'lightgreen') + "]"
				list_ok.append(i.get('ip')+":"+i.get('port'))
				if verbose:
					print "STATUS:", a.status_code
			except:
				if verbose:
					print "STATUS:", "ERROR"
		self.CONFIG.write_config('OK', 'proxy', value="\n".join(list_ok))

	def usage(self):
		import argparse
		parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument('URL', help='URL to tester', action='store')
		parser.add_argument('-t', '--timeout', help='Timeout for checking', action='store', default=3)
		parser.add_argument('-l', '--load-config', help='Check Proxy list on config first', action='store_true')
		parser.add_argument('-v', '--verbose', help='Show process checking', action='store_true')
		if len(sys.argv) == 1:
			parser.print_help()
		else:
			args = parser.parse_args()
			self.test_proxy_ip(args.URL, args.timeout, None, args.verbose)

if __name__ == '__main__':
	PID = os.getpid()
	print "PID =", PID
	c = proxy_tester()
	# c.getProxyList()
	# c.test_proxy_ip(*sys.argv[1:])
	# c.usage()
	c.getPage()