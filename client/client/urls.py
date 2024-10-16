from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("vault/", views.vault, name="vault"),
    path("vault-new/", views.vaultNew, name="vaultNew"),
    path("vault-delete/", views.vaultDelete, name="vaultDelete"),
    path("vault-edit/", views.vaultEdit, name="vaultEdit"),
    path("logout/", views.logout, name="logout"),
]
