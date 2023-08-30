from django.contrib import admin
from django.urls import path
from App1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , views.indexPage,name="indexPage" ),
    path('signin/', views.signIn, name='signin'),
    path('main/', views.mainPage, name='main'),
    path('menu/', views.menuPage, name='menu'),
    path('logout/', views.logOut, name='logout'),
    path('statistics/', views.statisticPage, name='statistics'),
    path('statistics2/', views.statisticPage2, name='statistics2'),
    path('statistics3/', views.statisticPage3, name='statistics3'),
    path('setting/', views.settingPage, name='setting'),
    path('pqgSetting/<str:pqg>/', views.pqgSetting, name='pqgsetting'),

]
