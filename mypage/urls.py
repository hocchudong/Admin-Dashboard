from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'mypage.views.home'),
    url(r'^performance$', 'mypage.views.performance'),
    url(r'^instances$', 'mypage.views.instances'),
    #url(r'^test$', 'mypage.views.test'),
    url(r'^admin/', include(admin.site.urls)),
]
