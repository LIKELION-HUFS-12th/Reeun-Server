# board/urls.py

from django.urls import path
from .views import BoardList, BoardDetail, CommentList, CommentDetail

urlpatterns = [
    path('', BoardList.as_view(), name='board-list'),
    path('<int:post_id>/', BoardDetail.as_view(), name='board-detail'),
    path('<int:post_id>/comment/', CommentList.as_view(), name='comment-list'),
    path('<int:post_id>/comment/<int:comment_id>/', CommentDetail.as_view(), name='comment-detail'),
]
