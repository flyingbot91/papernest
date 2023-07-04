from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path("networking/", include("networking.urls")),
	path("admin/", admin.site.urls),
]
