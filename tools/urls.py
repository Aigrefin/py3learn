from django.conf.urls import url

from .views import frequency_view

app_name = 'tools'

urlpatterns = [
    url(r'^$', frequency_view, name='frequency'),
]
