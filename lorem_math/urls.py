from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^/*$', 'lorem_math.views.index'),
    url(r'^random/*$', 'lorem_math.views.random_latex'),
)
