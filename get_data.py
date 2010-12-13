#!/usr/bin/python

import sys
import json
import pycurl

class BizData:
	def __init__(self):
		self.contents = ''
		self.archive = []

	def body_callback(self, buf):
		self.contents = self.contents + buf

	def collect_json(self):
		self.archive.append(self.json)

	def reset_json(self):
		self.archive = []

	def decode(self):
		try:
			self.json = json.loads(self.contents);
			self.collect_json()
		except ValueError, e: 
			print >>sys.stderr, 'Could not load JSON object from body_callback(): %', e

	def get(self, url):
		c = pycurl.Curl()
		c.setopt(c.URL, url)
		c.setopt(c.WRITEFUNCTION, self.body_callback)
		c.perform()
		c.close()

	def get_all(self, url, limit):
		c = pycurl.Curl()
		url = url + "limit=%", limit
		# reset contents for each and call decode on each
		self.contents = ''
		while self.contents != '[]': 
			self.get(url)
			if self.contents != '[]':
				self.decode()

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

print b.searches(['name', 'source_url', 'registered_date'])


