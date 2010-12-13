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

	def search(self, param):
		results = []
		businesses = self.json
		for business in businesses:
			 results.append(business[param])
		return results

	def searches(self, params):
		results = []
		businesses = self.json
		for business in businesses:
			results.append([business[thing] for thing in params])
		return results

url = 'http://api.scraperwiki.com/api/1.0/datastore/getdata?format=json&name=oregon_business_registry&limit=10'

b = BizData()
b.get(url)
b.decode()

#b.search('name')

print b.searches(['name', 'source_url', 'registered_date'])






