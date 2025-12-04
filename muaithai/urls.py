from django.urls import path
from . import views

urlpatterns = [
    # Root URL points to homepage
    path('', views.homepage, name='homepage'),

    # Optional: /homepage can show the same or a different page
    path('homepage/', views.fighterCards_view.as_view(), name='fightercards'),

    # Fighter CRUD
    path('createfighter/', views.CreateFighter_view.as_view(), name='createfighter'),
    path('readfighter/', views.ReadFighter_view.as_view(), name='readfighter'),
    path('details/<int:pk>/', views.fighterDetailsView.as_view(), name='details'),
    path('updatefighter/<int:pk>/', views.UpdateFighter_view.as_view(), name='updatefighter'),
    path('deletefighter/<int:pk>/', views.deleteFighter_view.as_view(), name='deletefighter'),

    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Search
    path('search/', views.search_view, name='search'),

    # AI/Chatbot
    path('ai_page/', views.chatbot_page, name='ai_page'), 
    path('chatbot/get_response/', views.chatbot_response, name='chat_response'),
