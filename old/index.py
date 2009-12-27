'''
	index.py 	I shall do nothing but render the interface
'''

import os

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import web2hunter as WH

class MainHandler(webapp.RequestHandler):
	tPath = os.path.join( os.path.dirname (__file__), "templates" )

	def get(self):
		todo = self.request.get('getname');
		
		if (todo == 'true'):
			if (self.request.headers.get('Referer') != None):
				# stop others from stealing your bandwidth
				#if (self.request.headers.get('Referer').find('web2hunter.appspot.com')!=-1):

					# return a possible domain name
					possiblename = WH.genName()
			
					while (possiblename == ""):
						possiblename = WH.genName()
			
					# lets sanitize the possible name
					# for sometime we get the response header for some reason -
					# Content-Type: text/html; charset=utf-8 Cache-Control: ... blabla
					# well a foo.split()[-1] would help

					# food for javascript + sanitization
					self.response.out.write (possiblename.split()[-1])
				#else:
					#self.response.out.write ("nothing for you");
			else:
				self.response.out.write ("nothing for you");
		else:
			# render the template
			outstr = template.render (
				self.tPath + '/index.html', None )
	
			self.response.out.write (outstr)
		

def main():
	application = webapp.WSGIApplication( [('/.*',MainHandler)], debug=True )
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()

