from django.urls import path
from .views import (home_view, profile_view, setting_view, login_view,
                    register_view, logout_view, upload_view, follow_view, like_view, search_view, delete_view)

urlpatterns = [
    path('', home_view),
    path('profile/<int:pk>/', profile_view),
    path('settings/', setting_view),
    path('login/', login_view),
    path('register/', register_view),
    path('logout/', logout_view),
    path('upload/', upload_view),
    path('follow/', follow_view),
    path('like/', like_view),
    path('search/', search_view),
    path('delete/', delete_view)

]