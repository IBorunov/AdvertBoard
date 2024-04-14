from django.urls import path

from main.views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, ResponseList, accept_response, \
    ProfileUpdate, CategoryView, MyPostsList, ResponseCreate, delete_response, ConfirmUser

urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),
    path('my_posts/', MyPostsList.as_view(), name='my_posts'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('my_responses/', ResponseList.as_view(), name='my_responses'),
    path('<int:pk>/respond/', ResponseCreate.as_view(), name='respond'),
    path('resp/<int:pk>/delete/', delete_response, name='delete_response'),
    path('resp/<int:pk>/accept/', accept_response, name='accept_response'),

    path('profile/<int:pk>/', ProfileUpdate.as_view(), name='profile_edit'),

    path('category/<str:category>', CategoryView.as_view(), name='category_list'),

    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
]