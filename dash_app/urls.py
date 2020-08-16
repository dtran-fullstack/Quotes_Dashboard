from django.urls import path
from . import views

urlpatterns = [
    # Login and Register
    path('',views.render_log_reg),
    path('register',views.register),
    path('login',views.login),
    path('logout',views.logout),
    # Quotes Dashboard
    path('quotes',views.render_dash),
    path('post',views.post),
    path('quotes/<int:id>/delete',views.delete),
    path('like/<int:id>',views.add_like),
    # Account
    path('myaccount/<int:uid>',views.render_account),
    path('myaccount/<int:uid>/edit',views.update_account),
    # Profile
    path('user/<int:uid>',views.render_profile),
]