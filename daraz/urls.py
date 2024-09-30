from django.contrib import admin
from django.urls import path, include
from . import views
# from .views import *


urlpatterns = [
    path('', views.landing_page, name="productinfo"),
    path('productinfo/', views.ProductInfo, name="productinfo"),
    path('upload/', views.SimpleUpload, name="upload"),
    path('search/', views.Search, name="search"),
    path('multiplesearch/', views.MultiSearch, name="multiplesearch"),
    path('signup/', views.SignUp, name="signup"),
    path('accountverify/<auth_token>', views.AccountVerify, name="accountverify"),
    path('login/', views.LoginUser, name="login"),
    path('logout/', views.LogoutUser, name="logout"),
    path('forgetpassword/', views.Forget, name="forgetpassword"),
    path('changepassword/<token>/', views.ChangePassword, name="changepassword"),
    path('seller/', views.ShowSellerDataToAdmin, name="seller"),
    path('delete/<int:id>/', views.SellerDeleteByAdmin, name="delete"),
    path('update/<int:id>/', views.SellerDataUpdateByAdmin, name="update"),
    path('tracking/<int:id>', views.SellerTracking, name="tracking"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('profit_calculator/', views.profit_cal, name="profit_calculator"),
    path('account/', views.accountSettings, name="account"),
    path('contact/', views.contact, name="contact"),



]