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
			print >>sys.stderr, 'Could not load JSON oboject from body_callback(): %', e

b = BizData()
c = pycurl.Curl()
c.setopt(c.URL, 'http://api.scraperwiki.com/api/1.0/datastore/getdata?format=json&name=oregon_business_registry&limit=10')
c.setopt(c.WRITEFUNCTION, b.body_callback)
c.perform()
c.close()

b.decode()
		
print b.json
