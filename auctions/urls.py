from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("auctions/login", views.login_view, name="login"),
    path("auctions/logout", views.logout_view, name="logout"),
    path("auctions/register", views.register, name="register"),
    path("auctions/category/", views.category, name="category"),
    path("auctions/categories/", views.categories, name="categories"),
    path("auctions/watchlist/", views.watchlist, name="watchlist"),
    path("auctions/create_listing/", views.create_listing, name="create_listing"),
    path("auctions/<str:title>/", views.listing, name="listing"),
]
