
from django.urls import path, include
from tracker.views import *
urlpatterns = [
    path("", index, name='index'),
    path('delete-trans/<uid>', del_transaction,name= 'del_transaction'),
    path('register/', registration, name = "register"),
    path('login/', login_page, name = "login"),
    path('logout/', logout_page, name = "logout")



]
