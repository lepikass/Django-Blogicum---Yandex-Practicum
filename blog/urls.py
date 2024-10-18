from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('profile/edit/',
         views.EditProfileView.as_view(),
         name='edit_profile'),
    path('profile/<str:username>/',
         views.ProfileView.as_view(),
         name='profile'),
    path('posts/create/',
         views.CreatePostView.as_view(),
         name='create_post'),
    path('posts/<int:post_id>/edit/',
         views.EditPostView.as_view(),
         name='edit_post'),
    path('posts/<int:post_id>/delete/',
         views.DeletePostView.as_view(),
         name='delete_post'),
    path('posts/<int:post_id>/comment/',
         views.add_comment,
         name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.edit_comment,
         name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.delete_comment,
         name='delete_comment'),
]


handler404 = 'blog.views.page_not_found'
handler500 = 'blog.views.server_error'
