#!/usr/bin/env python

import multiprocessing
import argparse
import requests
import sys
import string
from numpy import array_split

requests.packages.urllib3.disable_warnings()
_GETstatus = 0
_GETresponseSize = 0
_POSTstatus = 0
_POSTresponseSize = 0
_POSTdata = {}
_paramValue = 'discobiscuits'

def version_info():
	VER = 'parameth v1.0 - \033[033mfind parameters and craic rocks\033[0m'
	AUTH = 'Author: \033[033mCiaran McNally - https://makthepla.net\033[0m'
	print '\033[1;34m                                       |   |'
	print '  __ \\   _` |  __| _` | __ `__ \\   _ \\ __| __ \\'
	print '  |   | (   | |   (   | |   |   |  __/ |   | | |'
	print '  .__/ \\__,_|_|  \\__,_|_|  _|  _|\\___|\\__|_| |_|'
	print '  _|\033[0m'
	print VER
	print AUTH
	print '\033[1;30m================================================\033[0m'

def getHeaderObj(header):
	h3 = {}
	h1 = string.split(header, ':')[0]
	h2 = string.split(header, ':')[1]
	h3[h1] = h2
	return h3

def getCookieObj(cookie):
	cookies = {}
	c1 = string.split(cookie, ':')[1]
	c2 = string.split(c1, ';')
	for i in c2:
		if len(i) != 0:
			c3 = string.split(i, '=')[0]
			c4 = string.split(i, '=')[1]
			cookies.update({c3:c4})
	return cookies

def getParamObj(data):
	newParam = ''
	newValue = ''
	params = []
	requestData = {}
	if data.startswith('?'):
		newParam = data[1:]
	else:
		newParam = data
	if len(data) != 0:
		params = string.split(newParam, '&')
		for i in params:
			newParam = string.split(i, '=')[0]	
			newValue = string.split(i, '=')[1]
			requestData[newParam] = newValue
		return requestData
	else:
		return requestData

def getParamStr(data):
	dataString = ''
	if len(data) != 0:
		for i,j in data.iteritems():
			dataString += i + '=' +j
			dataString += '&'
	return dataString[:-1]

def split_params(u, t):
	return array_split(u, t)

def statusMatch(ignore, status_code):
	if status_code in ignore:
		return False
	else:
		return True

def printOut(filename, string):
	f = open(filename,'a')
	f.write(string+'\n')
	f.close()

def requestor(url, parameter, header, agent, variance, proxy, 
				ignore, data, out, size, igmeth, cookie):
	headers = {}
	post = {}
	proxies = {}
	providedData = {}
	cookies = {}
	
	if ':' in cookie:
		cookies = getCookieObj(cookie)
	if ':' in header:
		headers = getHeaderObj(header)
	headers['User-agent'] = agent
	if ':' in proxy:
		proxies = getHeaderObj(proxy)
	
	for i in parameter:
		newrl = url
		strvar = ''
		post = {}
		post[i] = _paramValue
		if '?' in url:
			newrl += '&' + i + '=' + _paramValue
		else:
			newrl += '?' + i + '=' + _paramValue
		post.update(_POSTdata)
		try:	 
			#GET parameter
			if igmeth != 'g':
				g = requests.get(newrl, timeout=10, headers=header, 
					allow_redirects=False, verify=False, proxies=proxies,
					cookies=cookies)
				plusvar = len(g.content) + variance
				subvar = len(g.content) - variance

				if g.status_code != _GETstatus and statusMatch(ignore, str(g.status_code)):
					print '\033[032mGET(status)\033[0m: '+i+' | '+str(_GETstatus)+'->',
					print str(g.status_code)+' ( '+newrl+' )'
					if out != 'out':
						strvar = 'GET(status) '+i+' '+str(g.status_code)+' '+newrl
						printOut(out, strvar)
			
				if statusMatch(ignore, str(g.status_code)):
					if len(g.content) != _GETresponseSize and len(g.content) != size:
						if len(g.content) >= plusvar or len(g.content) <= subvar:
							print '\033[032mGET(size)\033[0m: '+i+' | '+str(_GETresponseSize),
							print '->' +str(len(g.content))+ ' ( '+newrl+' )'
							if out != 'out':
								strvar = 'GET(size) '+i+' '+str(len(g.content))+' '+newrl
								printOut(out, strvar)
			
			#POST parameter
			if igmeth != 'p':
				p = requests.post(url, timeout=10, headers=header, data=post,
					allow_redirects=False, verify=False, proxies=proxies,
					cookies=cookies)
				plusvar = len(p.content) + variance
				subvar = len(p.content) - variance

				if p.status_code != _POSTstatus and statusMatch(ignore, str(p.status_code)):
					print '\033[032mPOST(status)\033[0m: '+i+' | '+str(_POSTstatus)+'->',
					print str(p.status_code)+' ( '+url+' )'
					if out != 'out':
						strvar = 'POST(status) '+i+' '+str(p.status_code)+' '+url
						printOut(out, strvar)
			
				if statusMatch(ignore, str(p.status_code)):
					if len(p.content) != _POSTresponseSize and len(p.content) != size:
						if len(p.content) >= plusvar or len(p.content) <= subvar:
							print '\033[032mPOST(size)\033[0m: '+i+' | '+str(_POSTresponseSize),
							print '->' +str(len(p.content))+ ' ( '+url+' )'
							if out != 'out':
								strvar = 'POST(size) '+i+' '+str(len(p.content))+' '+url
								printOut(out, strvar)

		except requests.exceptions.Timeout:
			print 'Request Timed out on parameter "'+i+'"'
		except requests.exceptions.ConnectionError:
			print 'Connection Error on parameter "'+i+'"'
		except requests.exceptions.TooManyRedirects:
			print 'Redirect loop on parameter "'+i+'"'		
	

def getBase(url, header, agent, variance, proxy, data, igmeth, cookie):
	headers = {}
	proxies = {}
	cookies = {}
	get = ''
	url_base = ''
	global _GETstatus
	global _GETresponseSize	
	global _POSTstatus
	global _POSTresponseSize
	global _POSTdata
	
	if ':' in cookie:
		cookies = getCookieObj(cookie)
	if ':' in header:
		headers = getHeaderObj(header)
	headers['User-agent'] = agent
	if ':' in proxy:
		proxies = getHeaderObj(proxy)
	if '?' in url:
		get = string.split(url, '?')[1]
		url_base = string.split(url, '?')[0]
	else:
		url_base = url
	
	_POSTdata = getParamObj(get)
	if len(data) != 0:
		_POSTdata.update(getParamObj(data))
	print 'Establishing base figures...'
	if igmeth != 'p':
		print '\033[031mPOST data: \033[0m'+getParamStr(_POSTdata)
	print '\033[031mOffset value: \033[0m'+str(variance)
	try:
		if igmeth != 'g':
			g = requests.get(url, timeout=10, headers=headers, verify=False,
								allow_redirects=False, proxies=proxies,
								cookies=cookies)
			_GETstatus = g.status_code
			_GETresponseSize = len(g.content)
			print '\033[031mGET: content-length->\033[0m '+str(len(g.content)),
			print '\033[031m status->\033[0m '+str(g.status_code)
	
		if igmeth != 'p':
			p = requests.post(url_base, timeout=10, headers=headers, 
								verify=False, allow_redirects=False, 
								proxies=proxies, data=_POSTdata,
								cookies=cookies)
			_POSTstatus = p.status_code
			_POSTresponseSize = len(p.content)
			print '\033[031mPOST: content-length->\033[0m '+str(len(p.content)),
			print '\033[031m status->\033[0m '+str(p.status_code)
		
		if _POSTstatus != _GETstatus and igmeth != 'p' and igmeth != 'g':
			print 'POST and GET are different sizes'

	except requests.exceptions.Timeout:
		print 'Request Timed out!'
	except requests.exceptions.ConnectionError:
		print 'Connection Error!'
	except requests.exceptions.TooManyRedirects:
		print 'Redirect loop!'
	

if __name__ == '__main__':
	parse = argparse.ArgumentParser()
	parse.add_argument('-v', '--version', action='store_true', default=False,
						help='Version Information')
	parse.add_argument('-u', '--url', type=str, default='', help='Target URL')
	parse.add_argument('-p', '--params', type=str, default='lists/all.txt',
						help='Provide a list of parameters to scan for')
	parse.add_argument('-H', '--header', type=str, default='', 
						help='Add a custom header to the requests')
	parse.add_argument('-a', '--agent', type=str, default='parameth v1.0',
						help='Specify a user agent')
	parse.add_argument('-t', '--threads', type=int, default='2',
						help='Specify the number of threads.')
	parse.add_argument('-off', '--variance', type=int, default='0',
						help='The offset in difference to ignore (if dynamic pages)')
	parse.add_argument('-o', '--out', type=str, default='out',help='Specify output file')
	parse.add_argument('-P', '--proxy', type=str, default='',
						help='Specify a proxy in the form http|s://[IP]:[PORT]')
	parse.add_argument('-x', '--ignore', type=str, default='',
						help='Specify a status to ignore eg. 404,302...')
	parse.add_argument('-s', '--sizeignore', type=int, default='-1', 
						help='Ignore responses of specified size')
	parse.add_argument('-d', '--data', type=str, default='', 
						help='Provide default post data (also taken from provided url after ?)')
	parse.add_argument('-i', '--igmeth', type=str, default='',
						help='Ignore GET or POST method. Specify g or p')
	parse.add_argument('-c', '--cookie', type=str, default='',
						help='Specify Cookies')
	args = parse.parse_args()

	if len(sys.argv) <= 1:
		parse.print_help()
		sys.exit(0)
	
	if args.version:
		version_info()

	if args.url:
		version_info()
		getBase(args.url, args.header, args.agent, args.variance, args.proxy, 
				args.data, args.igmeth, args.cookie)
		print 'Scanning it like you own it...'	
		try:
			with open(args.params, "r") as f:
				params = f.read().splitlines()
		except IOError:
			print "IOError: Your file is a sex offender."
		threads = []
		splitlist = list(split_params(params, args.threads))
		for i in range(0, args.threads):
			p = multiprocessing.Process(target=requestor, args=(args.url,
				splitlist[i], args.header, args.agent, args.variance, 
				args.proxy, args.ignore, args.data, args.out, args.sizeignore,
				args.igmeth, args.cookie))
			threads.append(p)
		try:
			for p in threads:
				p.start()
			for p in threads:
				p.join()
		except KeyboardInterrupt:
			print 'Scagging out scanner...'
			for p in threads:
				p.terminate()
			sys.exit(0)
		threads = []
