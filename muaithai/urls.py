from django.urls import path
from . import views

urlpatterns = [
    path('homepage', views.fighterCards_view, name = 'homepage'),
    # path('homepage', views.fighterCards_view.as_view(), name = 'homepage'),

    # path('createfighter', views.CreateFighter_view, name = 'createfighter'),
    path('createfighter', views.CreateFighter_view.as_view(), name = 'createfighter'),

    # path('readfighter', views.ReadFighter_view, name = 'readfighter'),
    path('readfighter', views.ReadFighter_view.as_view(), name='readfighter'),

    # path('details/<int:pk>', views.fighterDetailsView, name='details'),
    path('details/<int:pk>', views.fighterDetailsView.as_view(), name='details'),

    # path('updatefighter/<int:pk>', views.UpdateFighter_view, name ='updatefighter'),
    path('updatefighter/<int:pk>', views.UpdateFighter_view.as_view(), name ='updatefighter'),

    # path('deletefighter/<int:pk>', views.deleteFighter_view, name ='deletefighter'),
    path('deletefighter/<int:pk>', views.deleteFighter_view.as_view(), name ='deletefighter'),

    path("signup", views.signup_view, name="signup"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),

    path('search/', views.search_view, name='search'),

    path("ai_page/", views.chatbot_page, name="ai_page"),
    path("chatbot/get_response/", views.chatbot_response, name="chat_response"),

]





