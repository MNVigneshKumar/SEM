from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<str:room>/", views.room, name="room"),
    path("checkview", views.checkview, name="checkview"),
    path("checkview_owner", views.checkview_owner, name="checkview_owner"),
    path("send", views.send, name="send"),
    path("getMessages/<str:room>/", views.getMessages, name="getMessages"),
]
