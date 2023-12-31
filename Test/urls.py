from django.contrib import admin
from django.urls import path, include
from test_app.views import your_view_name
from test_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('your-view-url/', views.your_view_name, name='your_view_name'),
    path('', views.index, name="home")
]