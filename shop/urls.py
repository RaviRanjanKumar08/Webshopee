from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("about", views.about, name="aboutus"),
    path("contact", views.contact, name="contact us"),
    path("tracker", views.tracker, name="tracker"),
    path("search", views.search, name="search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout", views.checkout, name="checkout"),
    path("signup", views.signup, name="signup"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("profile", views.profile, name="profile"),
    path("orders", views.orders, name="orders"),
    path("chatbot", views.chatbot, name="chatbot"),
    path("verifyotp", views.verifyotp, name="verifyotp"),
    path("status", views.status, name="status"),
    path("payhandler", views.payhandler, name="payhandler"),
    path("reg", views.reg, name="reg")
    


]
