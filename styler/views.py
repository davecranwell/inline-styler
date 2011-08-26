from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import Context, Template

import re
import urllib
import sys

from lxml import etree

from django.conf import settings

from converter import Conversion, MyURLopener

exampleHTML='''
<html>
	<head>
		<title>Example</title>
		<link rel="stylesheet" href="%(root_url)s/static/css/example.css" />
	</head>
	<body>
		<style type="text/css">
			h1{
				color:yellow
			}
		</style>
		<h1>An example title</h1>
		<p>Paragraph 1</p>
		<p class="p2">Paragraph 2</p>
	</body>
</html>'''

def index(request):
	example=exampleHTML %  {'root_url': settings.ROOT_URL}
	return render_to_response('index.html', {'example':example})

def api(request):
	return render_to_response('api.html')
	
def convert(request):
	urllib._urlopener = MyURLopener()
	sourceHTML=''
	sourceURL=''
	
	if request.POST.has_key('source'):
		sourceHTML=request.POST['source']
	if request.POST.has_key('source_url'):
		sourceURL=request.POST['source_url'].strip()
	if request.POST.has_key('returnraw'):
		outputTemplate='raw.html'
	else:
		outputTemplate='index.html'				
	
	if request.method == 'POST': # form submitted
		#parse HTML
		try:
			if len(sourceURL):
				urlregexpt=re.compile('((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)')
				#check for valid URL
				if(not urlregexpt.match(sourceURL)):
					return render_to_response(outputTemplate,{'sourceHTML':sourceHTML,'sourceURL':sourceURL,'error_message':'The source URL does not appear to be valid.'})
				#if valid URL attempt to download
				try:
					f=urllib.urlopen(sourceURL)
					document = etree.HTML(f.read())
				except:
					return render_to_response(outputTemplate,{'sourceHTML':sourceHTML,'sourceURL':sourceURL,'error_message':'The source URL could not be accessed.'})
			else:
				try:
					document = etree.HTML(sourceHTML)
				except:
					return render_to_response(outputTemplate,{'sourceHTML':sourceHTML,'sourceURL':sourceURL,'error_message':'The source HTML does not appear to be valid.'})
		except KeyError:
			return HttpResponseRedirect("/")
		
		# do conversion
		try:
			converter=Conversion()
			converter.perform(document,sourceHTML,sourceURL)
		except IOError:
			return render_to_response(outputTemplate,{'sourceHTML':sourceHTML, 'sourceURL':sourceURL, 'error_message': str(sys.exc_info()[1])})
				
		return render_to_response(outputTemplate,{'sourceHTML':sourceHTML,'sourceURL':sourceURL,'convertedHTML':converter.convertedHTML, 'warnings':converter.CSSErrors, 'support':converter.CSSUnsupportErrors,'supportPercentage':converter.supportPercentage})
	else:
		return HttpResponseRedirect("/")