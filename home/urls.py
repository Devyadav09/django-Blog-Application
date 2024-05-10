from django.urls import path
from . import views
from .views import UpdatePostView

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.user_login,name='user_login'),
    path('logout/',views.user_logout,name='user_logout'),
    path('menupage/',views.menu,name='menu'),
    path('addpost/',views.addpost,name='addpost'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('blog_detail/<slug>/', views.blog_detail, name='blog_detail'),
    path('mypost/',views.mypost,name='mypost'),
    path('deletepost/<slug>/',views.deletepost,name='deletepost'),
    path('edit_blog_post/<slug:slug>/', UpdatePostView.as_view(), name='edit_blog_post'),
    path("search/", views.search, name="search"),
]



