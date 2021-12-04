from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("accounts/login/", views.login_view, name="login_view"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("item/<int:id>", views.open_listing, name="open_listing"),
    path("add_to_watchlist/<int:id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_form_watchlist/<int:id>", views.remove_form_watchlist, name="remove_form_watchlist"),
    path("close_auction/<int:id>", views.close_auction, name="close_auction"),
    path("user/watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:cat>", views.open_category, name="open_category")
    
]
