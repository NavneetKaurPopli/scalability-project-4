from django.urls import path

from . import views


app_name = 'authentication'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('add/', views.add, name='add'),

    path('quote', views.quote),
    path('buy/', views.buy),
    path('commit_buy/', views.commit_buy),
    path('cancel_buy/', views.cancel_buy),
    path('sell/', views.sell),
    path('commit_sell/', views.commit_sell),
    path('cancel_sell/', views.cancel_sell),
    path('set_buy_amount/', views.set_buy_amount),
    path('cancel_set_buy/', views.cancel_set_buy),
    path('set_buy_trigger/', views.set_buy_trigger),
    path('set_sell_amount/', views.set_sell_amount),
    path('set_sell_trigger/', views.set_sell_trigger),
    path('cancel_set_sell/', views.cancel_set_sell),
    path('dumplog', views.dumplog),
    path('display_summary', views.display_summary),


]