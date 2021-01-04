from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('graphene_setup_check', views.graphene_setup_check, name='graphene_setup_check'),
    path('graphene_setup', views.setup, name='graphene_setup'),
    path('pub_key', views.download_pubkey, name='pub_key'),
    path('keygen', views.register, name='keygen'),
    path('register_submit', views.register_submit, name='register_submit'),

    # these are for account creation
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/register/', views.registerView, name='register'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.profileView, name='profile'),
    path('accounts/all/', views.usersView, name='users'),
    path('accounts/<str:user>', views.userView, name='user'),
    # path('download/', views.downloadView, name='download'),

    path('upload', views.uploadView, name='upload'),

    path('revoke/view', views.revokeView, name='revoke'),
    path('revoke/save', views.revokeSaveView, name='new_revoked_user'),
    path('revoke/remove', views.revokeRemoveView, name='remove_revoked_user'),

]
