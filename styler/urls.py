from django.conf.urls.defaults import *

urlpatterns = patterns('inlinestylr.styler.views',
	(r'^$', 'index'),
	(r'^convert/$', 'convert'),
	(r'^api/$', 'api'),
)
