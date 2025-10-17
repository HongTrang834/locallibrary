from django.urls import path
from . import views

urlpatterns = [
    # Thêm các URL của ứng dụng catalog vào đây
    path('', views.index, name='index'),
]