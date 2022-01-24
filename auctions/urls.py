from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("list/<int:id>", views.list, name="list"),
    path("watch/", views.watch, name="watch"),
    path("watch/add/<int:id>", views.add_watch, name="add"),
    path("watch/delete/<int:id>", views.delete_watch, name="delete")
]
