# community/classboard/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('', ClassBoardList.as_view(), name='classboard-list'),  # 학급 게시판 게시글 생성
    path('<int:admission_year>/<int:grade>/<int:order>/', GetClassBoardAPI.as_view(), name='getclassboard'), # 학급 게시판 게시글 조회
    path('detail/<int:classBoardId>/', GetClassBoardDetail.as_view(), name='getclassboarddetail'), # 학급 게시판 게시글 상세 조회
    path('edit/', EditClassBoardDetail.as_view(), name='editclassboarddetail'), # 학급 게시판 게시글 수정
    path('delete/', DeleteClassBoardDetail.as_view(), name='deleteclassboarddetail'), # 학급 게시판 게시글 삭제
    path('comment/<int:classBoardId>/', GetCommentAPI.as_view(), name='getcomment'), # 학급 게시판 댓글 조회
    path('comment/detail/<int:commentId>/', CommentDetailAPI.as_view(), name='commentdetail'), # 학급 게시판 댓글 상세 조회
    path('comment/write/', PostCommentAPI.as_view(), name='postcomment'), # 학급 게시판 댓글 작성
    path('comment/edit/', EditCommentAPI.as_view(), name='editcomment'), # 학급 게시판 댓글 수정
    path('comment/delete/', DeleteCommentAPI.as_view(), name='deletecomment'), # 학급 게시판 댓글 삭제
]
