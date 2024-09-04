# community/classboard/urls.py

from django.urls import path
from .views import ClassBoardList, ClassBoardDetail, CommentList, CommentDetail

urlpatterns = [
    path('grade/<int:grade>/', ClassBoardList.as_view(), name='classboard-list'),
    path('grade/<int:grade>/<int:post_id>/', ClassBoardDetail.as_view(), name='classboard-detail'),
    path('grade/<int:grade>/<int:post_id>/comment/', CommentList.as_view(), name='comment-list'),
    path('grade/<int:grade>/<int:post_id>/comment/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
]
