from .views import *
from django.urls import include, path
from .views import SignupViewSet,LoginAPIView,LogoutAPIView,task_list_api,task_create_api,task_delete_api,task_update_api,task_patch_api,change_password_api

urlpatterns = [
    path('api/v1/auth/signup/',SignupViewSet.as_view(),name ='signup'),
    path('api/v1/auth/login/',LoginAPIView.as_view(),name ='login'),
    path('api/v1/auth/logout/',LogoutAPIView.as_view(),name ='logout'),
    path('api/v1/task/list/',task_list_api,name ='tasklist'),
    path('api/v1/task/create/',task_create_api,name ='taskcreate'),
    path('api/v1/task/delete/<int:pk>/',task_delete_api,name ='taskdelete'),
    path('api/v1/task/update/<int:pk>/',task_update_api,name ='taskupdate'),
    path('api/v1/task/patch/<int:pk>/',task_patch_api,name ='taskpatch'),
    path('api/v1/task/change_password/',change_password_api,name ='changepassword'),
]