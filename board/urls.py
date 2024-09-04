# community/board/urls.py

from django.urls import path
from .views import BoardList, BoardDetail, CommentList, CommentDetail

urlpatterns = [
    path('', BoardList.as_view(), name='board-list'),  # 전체 게시판 게시글 목록 조회 및 생성
    path('<int:post_id>/', BoardDetail.as_view(), name='board-detail'),  # 전체 게시판 특정 게시글 조회, 수정, 삭제
    path('<int:post_id>/comments/', CommentList.as_view(), name='comment-list'),  # 전체 게시판 특정 게시글에 대한 댓글 목록 조회 및 생성
    path('<int:post_id>/comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),  # 전체 게시판 특정 댓글 조회, 수정, 삭제
]
