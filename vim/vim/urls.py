from tastypie.api import Api
from django.conf.urls import patterns, include, url
from vim_app.api import CustomerResource,MarketsResource
from django.contrib import admin

admin.autodiscover()


customer_resource = CustomerResource()
markets_resource = MarketsResource()

v1_api = Api(api_name='v1')
v1_api.register(CustomerResource())
v1_api.register(MarketsResource())

print v1_api.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vim.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', include('vim_app.urls')),
    (r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
