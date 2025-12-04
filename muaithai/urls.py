from django.contrib import admin
from django.urls import path, include
from muaithai import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Homepage
    path('', views.fighter_cards_view, name='homepage'),
    path('homepage/', views.fighter_cards_view, name='homepage_alias'),

    # Fighter CRUD
    path('createfighter/', views.CreateFighterView.as_view(), name='createfighter'),
    path('readfighter/', views.ReadFighterView.as_view(), name='readfighter'),
    path('details/<int:pk>/', views.FighterDetailsView.as_view(), name='details'),
    path('updatefighter/<int:pk>/', views.UpdateFighterView.as_view(), name='updatefighter'),
    path('deletefighter/<int:pk>/', views.DeleteFighterView.as_view(), name='deletefighter'),

    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Search
    path('search/', views.search_view, name='search'),

    # AI / Chatbot
    path('ai_page/', views.chatbot_page, name='ai_page'),
    path('chatbot/get_response/', views.chatbot_response, name='chat_response'),

    # API
    path('api/', include('MMA_api.urls'))
]
