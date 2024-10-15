from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view.as_view(), name='login_view'),
    path('friends', views.friends, name='friends') ,
    path('talk_room/<int:user_id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('name_change', views.name_change, name='name_change'),
    path('email_change', views.email_change, name="email_change"),
    path('image_change', views.image_change, name="image_change"),
    path('password_change', views.password_change, name="password_change"),
    path('logout/', views.Logout.as_view(), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)