from django.urls import path

from main.views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, ResponseCreate, ResponseDetail, \
    ResponseUpdate, ResponseDelete, ResponseList

urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('resp/create/', ResponseCreate.as_view(), name='response_create'),
    path('resp/<int:pk>/', ResponseDetail.as_view(), name='response_detail'),
    path('resp/<int:pk>/edit/', ResponseUpdate.as_view(), name='response_update'),
    path('resp/<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),
    path('responses/', ResponseList.as_view(), name='response_list'),
]