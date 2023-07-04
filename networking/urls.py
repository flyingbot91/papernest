from django.urls import path

from . import views

urlpatterns =  [
	#path("", views.coverage, name='coverage')
	path("<slug:q>", views.coverage, name='coverage')
]
