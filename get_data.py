#!/usr/bin/python

import sys
import json
import pycurl

class BizData:
	def __init__(self):
		self.contents = ''

	def body_callback(self, buf):
		self.contents = self.contents + buf

	def decode(self):
		try:
			self.json = json.loads(self.contents);
		except ValueError, e: 
			print >>sys.stderr, 'Could not load JSON object from body_callback(): %', e

	def get(self, url):
		c = pycurl.Curl()
		c.setopt(c.URL, url)
		c.setopt(c.WRITEFUNCTION, self.body_callback)
		c.perform()
		c.close()


url = 'http://api.scraperwiki.com/api/1.0/datastore/getdata?format=json&name=oregon_business_registry&limit=10'

b = BizData()
b.get(url)
b.decode()
		
print b.json



