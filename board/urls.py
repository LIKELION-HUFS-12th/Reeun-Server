# community/board/urls.py

from django.urls import path
from .views import BoardList, BoardDetail, CommentList, CommentDetail

urlpatterns = [
    path('', BoardList.as_view(), name='board-list'),  # 게시판 목록 조회 및 게시글 작성
    path('<int:post_id>/', BoardDetail.as_view(), name='board-detail'),  # 특정 게시글의 상세 조회, 수정, 삭제
    path('<int:post_id>/comment/', CommentList.as_view(), name='comment-list'),  # 특정 게시글에 대한 댓글 목록 조회 및 댓글 작성
    path('<int:post_id>/comment/<int:comment_id>/', CommentDetail.as_view(), name='comment-detail'),  # 특정 게시글에 대한 특정 댓글 삭제
]
