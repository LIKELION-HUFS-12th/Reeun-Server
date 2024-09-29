# community/board/views.py

from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Board, Comment
from .serializers import BoardSerializer, BoardCommentSerializer

# 전체 게시판 게시글 목록 조회 및 생성
class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        school = user.school
        admission_year = user.enrollYear

        return Board.objects.filter(
            school=school,
            admission_year=admission_year
        )

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        admission_year = user.enrollYear

        data = request.data.copy()
        if 'school' in data:
            data.pop('school')

        serializer = self.get_serializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user, school=user.school, admission_year=admission_year)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 전체 게시판 특정 게시글 조회, 수정, 삭제
class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        post_id = self.kwargs.get('post_id')
        if not post_id:
            return Board.objects.none()

        return Board.objects.filter(
            id=post_id,
            school=user.school,
            admission_year=user.enrollYear
        )

    def get_object(self):
        queryset = self.get_queryset()
        post_id = self.kwargs.get('post_id')
        try:
            return queryset.get(id=post_id)
        except Board.DoesNotExist:
            raise Http404("게시글을 찾을 수 없습니다.")

# 전체 게시판 댓글 목록 조회 및 생성
class CommentList(generics.ListCreateAPIView):
    serializer_class = BoardCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        post_id = self.kwargs.get('post_id')
        if post_id:
            return Comment.objects.filter(
                board__id=post_id,
                board__school=user.school,
                board__admission_year=user.admission_year
            )
        else:
            return Comment.objects.filter(
                board__school=user.school,
                board__admission_year=user.admission_year
            )

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        post_id = self.kwargs.get('post_id')
        if not post_id:
            return Response({"detail": "게시글 ID가 제공되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['board'] = post_id

        serializer = self.get_serializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 전체 게시판 특정 댓글 조회, 수정, 삭제
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BoardCommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        post_id = self.kwargs.get('post_id')
        comment_id = self.kwargs.get('pk')
        if not post_id or not comment_id:
            return Comment.objects.none()

        return Comment.objects.filter(
            board__id=post_id,
            id=comment_id,
            board__school=user.school,
            board__admission_year=user.enrollYear
        )
