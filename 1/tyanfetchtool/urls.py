from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'tyanfetchtool.views.home'),


)

urlpatterns += patterns('',
    (r'^zhidao/$','fetchZhidao.views.view'),
    (r'^zhidao/start$','fetchZhidao.views.startFetch'),
    (r'^zhidao/see$','fetchZhidao.views.seezhidaono'),
    (r'^zhidao/fstart$','fetchZhidao.views.start'),
    (r'^zhidao/realstart$','fetchZhidao.views.realstart'),
)
