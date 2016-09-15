#!/usr/bin/env python

import multiprocessing
import argparse
import requests
import sys
import string
from numpy import array_split

requests.packages.urllib3.disable_warnings()
BASE_GETstatus = 0
BASE_GETresponseSize = 0
BASE_POSTstatus = 0
BASE_POSTresponseSize = 0
BASE_paramValue = 'discobiscuits'

def version_info():
	VERSION_INFO = 'parameth v1.0 - \033[033mfind parameters and craic rocks\033[0m'
	AUTHOR_INFO = 'Author: \033[033mCiaran McNally - https://makthepla.net\033[0m'
	print '\033[1;34m                                       |   |'
	print '  __ \\   _` |  __| _` | __ `__ \\   _ \\ __| __ \\'
	print '  |   | (   | |   (   | |   |   |  __/ |   | | |'
	print '  .__/ \\__,_|_|  \\__,_|_|  _|  _|\\___|\\__|_| |_|'
	print '  _|\033[0m'
	print VERSION_INFO
	print AUTHOR_INFO
	print '\033[1;30m=====================================================\033[0m'

def getHeaderObj(header):
	h1 = string.split(header, ':')[0]
	h2 = h1+':'
	h3 = string.split(header, h2)[1]
	h2 = {h1:h3}
	return h2

def split_params(u, t):
	return array_split(u, t)

def statusMatch(ignore, status_code):
	if status_code in ignore:
		return False
	else:
		return True

def requestor(url, parameter, header, agent, variance, proxy, ignore):
	headers = {}
	post = {}
	proxies = {}
	if ':' in header:
		headers = getHeaderObj(header)
	headers['User-agent'] = agent
	if ':' in proxy:
		proxies = getHeaderObj(proxy)
	for i in parameter:
		newrl = url
		post = {}
		post[i] = BASE_paramValue
		if '?' in url:
			newrl += '&' + i + '=' + BASE_paramValue
		else:
			newrl += '?' + i + '=' + BASE_paramValue
		try:	 
			#GET parameter
			g = requests.get(newrl, timeout=10, headers=header, 
				allow_redirects=False, verify=False, proxies=proxies)
			plusvar = len(g.content) + variance
			subvar = len(g.content) - variance

			if g.status_code != BASE_GETstatus and statusMatch(ignore, str(g.status_code)):
				print '\033[032mGET(status)\033[0m: '+i+' | '+str(BASE_GETstatus)+'->',
				print str(g.status_code)+' ( '+newrl+' )'
			
			if statusMatch(ignore, str(g.status_code)):
				if len(g.content) != BASE_GETresponseSize:
					if len(g.content) >= plusvar or len(g.content) <= subvar:
						print '\033[032mGET(size)\033[0m: '+i+' | '+str(BASE_GETresponseSize),
						print '->' +str(len(g.content))+ ' ( '+newrl+' )'
			
			#POST parameter
			p = requests.post(url, timeout=10, headers=header, data=post,
				allow_redirects=False, verify=False, proxies=proxies)
			plusvar = len(p.content) + variance
			subvar = len(p.content) - variance

			if p.status_code != BASE_POSTstatus and statusMatch(ignore, str(p.status_code)):
				print '\033[032mPOST(status)\033[0m: '+i+' | '+str(BASE_POSTstatus)+'->',
				print str(p.status_code)+' ( '+url+' )'
			
			if statusMatch(ignore, str(g.status_code)):
				if len(p.content) != BASE_POSTresponseSize:
					if len(p.content) >= plusvar or len(p.content) <= subvar:
						print '\033[032mPOST(size)\033[0m: '+i+' | '+str(BASE_POSTresponseSize),
						print '->' +str(len(p.content))+ ' ( '+url+' )'

		except requests.exceptions.Timeout:
			print 'Request Timed out on parameter "'+i+'"'
		except requests.exceptions.ConnectionError:
			print 'Connection Error on parameter "'+i+'"'
		except requests.exceptions.TooManyRedirects:
			print 'Redirect loop on parameter "'+i+'"'		
	

def getBase(url, header, agent, proxy):
	headers = {}
	proxies = {}
	global BASE_GETstatus
	global BASE_GETresponseSize	
	global BASE_POSTstatus
	global BASE_POSTresponseSize
	
	if ':' in header:
		headers = getHeaderObj(header)
	headers['User-agent'] = agent
	if ':' in proxy:
		proxies = getHeaderObj(proxy)
	print 'Establishing base figures...'
	try:
		g = requests.get(url, timeout=10, headers=headers, verify=False,
							proxies=proxies)
		BASE_GETstatus = g.status_code
		BASE_GETresponseSize = len(g.content)
		print '\033[031mGET: content-length-> '+str(len(g.content)),
		print ' status-> '+str(g.status_code)+'\033[0m'
	
		p = requests.post(url, timeout=10, headers=headers, verify=False,
							proxies=proxies)
		BASE_POSTstatus = p.status_code
		BASE_POSTresponseSize = len(p.content)
		print '\033[031mPOST: content-length-> '+str(len(p.content)),
		print ' status-> '+str(p.status_code)+'\033[0m'
		
		if BASE_POSTstatus != BASE_GETstatus:
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
	parse.add_argument('-o', '--variance', type=int, default='0',
						help='The offset in difference to ignore (if dynamic pages)')
	parse.add_argument('-P', '--proxy', type=str, default='',
						help='Specify a proxy in the form http|s://[IP]:[PORT]')
	parse.add_argument('-x', '--ignore', type=str, default='',
						help='Specify a status to ignore eg. 404,302...')
	args = parse.parse_args()

	if len(sys.argv) <= 1:
		parse.print_help()
		sys.exit(0)
	
	if args.version:
		version_info()

	if args.url:
		version_info()
		getBase(args.url, args.header, args.agent, args.proxy)
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
				args.proxy, args.ignore))
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
