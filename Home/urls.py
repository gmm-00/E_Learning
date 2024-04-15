from .views import *
from django.urls import path,include

urlpatterns = [
    path('', fst , name='fst'),
    path('home/', home , name='home'),
    path('course/<slug>/', view_course , name='course'),
    path('become_pro/', become_pro , name='become_pro'),
    path('payment/', payment, name='payment'),
    path('success_page/', success_page , name='success_page'),
    path('login/', login_page , name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),
    
]
