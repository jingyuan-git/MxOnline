__author__ = 'jingyuan'
__date__ = '2020/5/16 9:22'

from django.conf.urls import url

from apps.organizations.views import OrgView, AddAskView

urlpatterns = [
    url(r'^list$', OrgView.as_view(), name='list'),
    url(r'^add_ask$', AddAskView.as_view(), name='add_ask'),
]
