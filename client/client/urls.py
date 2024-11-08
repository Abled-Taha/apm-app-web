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
    path("session-edit/", views.sessionEdit, name="sessionEdit"),
    path("session-delete/", views.sessionDelete, name="sessionDelete"),
    path("pp-new/", views.ppNew, name="ppNew"),
    path("export-apm-json-0/", views.exportApmJson0, name="exportApmJson0"),
    path("import-vault/", views.importVault, name="importVault"),
    path("pgconfig/", views.pGConfig, name="pGConfig"),
    path("logout/", views.logout, name="logout"),
]
