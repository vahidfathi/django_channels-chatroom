from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='log_out'),
    path('signup/', views.sign_up, name='sign_up'),
    path('chatrooms/uploadfile/', login_required(views.upload_file), name='upload_file'),
    path('chatrooms/', login_required(views.ChatroomLists.as_view()), name='all-chatrooms'),
    path('chatrooms/create/', login_required(views.ChatroomCreate.as_view()), name='chatroom-create'),
    path('chatrooms/<str:room_id>/', login_required(views.room), name='chatroom'),
    path('chatrooms/<str:pk>/edit/', login_required(views.ChatroomEdit.as_view()), name='chatroom-edit'),
    path('chatrooms/<str:pk>/delete/', login_required(views.ChatroomDelete.as_view()), name='chatroom-delete'),
    path('room/<str:room_id>/', login_required(views.room), name='room'),
]

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
