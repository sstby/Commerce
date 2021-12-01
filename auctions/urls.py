from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("item/<int:id>", views.open_listing, name="open_listing"),
    path("item/<int:id>", views.make_bid, name="make_bid")
    
]
