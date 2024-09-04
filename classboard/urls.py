# community/classboard/urls.py

from django.urls import path
from .views import ClassBoardList, ClassBoardDetail, CommentList, CommentDetail

urlpatterns = [
    path('grade/<int:grade>/', ClassBoardList.as_view(), name='classboard-list'),  # 학급 게시판 게시글 목록 조회 및 생성
    path('grade/<int:grade>/<int:post_id>/', ClassBoardDetail.as_view(), name='classboard-detail'),  # 학급 게시판 게시글 조회, 수정, 삭제
    path('grade/<int:grade>/<int:post_id>/comments/', CommentList.as_view(), name='comment-list'),  # 학급 게시판 댓글 목록 조회 및 생성
    path('grade/<int:grade>/<int:post_id>/comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),  # 학급 게시판 댓글 조회, 수정, 삭제
]
