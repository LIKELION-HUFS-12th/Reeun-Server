# community/board/views.py

from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from .models import Board, Comment
from .serializers import *

# 전체 게시판 게시글 목록 조회 및 생성
class BoardList(generics.ListCreateAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['학교 커뮤니티'],
        operation_summary="학교 커뮤니티 게시글 조회",
        operation_description="특정 학교 커뮤니티에 작성된 게시글을 모두 불러온다.",
        responses={200: openapi.Response(
            description="조회 성공",
            schema=BoardSerializer(many=True)
        )})
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        school = user.school
        admission_year = user.enrollYear

        boards = Board.objects.filter(school=school, admission_year=admission_year)
        serializer = BoardSerializer(boards, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
            tags=['학교 커뮤니티'],
            operation_summary="학교 커뮤니티 게시글 생성",
            operation_description="특정 학교 커뮤니티에 게시글을 작성한다.",
            request_body=PostBoardListSerializer,
            responses={201: openapi.Response(
                description="등록 성공",
                schema=BoardSerializer()
            )})
    def post(self, request, *args, **kwargs):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        admission_year = user.enrollYear
        if admission_year is None:
            return Response({"message": "입학년도가 없는 유저는 글을 작성할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

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
            school=user.school
        )

    def get_object(self):
        queryset = self.get_queryset()
        post_id = self.kwargs.get('post_id')
        try:
            return queryset.get(id=post_id)
        except Board.DoesNotExist:
            raise Http404("게시글을 찾을 수 없습니다.")
        
    @swagger_auto_schema(
        tags=['학교 커뮤니티'],
        operation_summary="학교 커뮤니티 특정 게시글 조회",
        operation_description="학교 커뮤니티에 작성된 특정 게시글을 조회한다.",
        responses={200: openapi.Response(
            description="조회 성공",
            schema=BoardSerializer()
        )})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
        
    @swagger_auto_schema(
        tags=['학교 커뮤니티'],
        operation_summary="학교 커뮤니티 특정 게시글 수정",
        operation_description="학교 커뮤니티에 작성된 특정 게시글을 수정한다.",
        request_body=PostBoardListSerializer,
        responses={200: openapi.Response(
            description="조회 성공",
            schema=BoardSerializer()
        )})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
        
        
    @swagger_auto_schema(
        tags=['학교 커뮤니티'],
        operation_summary="학교 커뮤니티 특정 게시글 삭제",
        operation_description="학교 커뮤니티에 작성된 특정 게시글을 삭제한다.",
        responses={204: openapi.Response(
            description="삭제 성공"
        )})
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    # PATCH는 비활성화한다.
    @swagger_auto_schema(
        tags=['사용되지 않는 API'],
        operation_summary="사용X",
        operation_description="사용X"
        )
    def patch(self, request, *args, **kwargs):
        return Response({"detail": "PATCH 메서드는 지원되지 않습니다."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# 전체 게시판 댓글 목록 조회 및 생성
class CommentList(generics.ListCreateAPIView):
    serializer_class = BoardCommentSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
            tags=['학교 커뮤니티'],
            operation_summary="학교 커뮤니티 게시글에 달린 댓글 조회",
            operation_description="특정 학교 커뮤니티에 작성된 게시글에 달린 댓글을 모두 조회한다.",
            responses={200: openapi.Response(
                description="등록 성공",
                schema=BoardCommentSerializer(many=True)
            )})
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        admission_year = user.enrollYear
        if admission_year is None:
            return Response({"message": "입학년도가 없는 유저는 댓글을 조회할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        post_id = self.kwargs.get('post_id')
        if post_id:
            comments = Comment.objects.filter(
                board__id=post_id,
                board__school=user.school,
                board__admission_year=admission_year
            )
        else:
            comments = Comment.objects.filter(
                board__school=user.school,
                board__admission_year=admission_year
            )

        serializer = BoardCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
            tags=['학교 커뮤니티'],
            operation_summary="학교 커뮤니티 게시글에 댓글 작성",
            operation_description="특정 학교 커뮤니티에 작성된 게시글에 댓글을 작성한다.",
            request_body=PostCommentListSerializer,
            responses={201: openapi.Response(
                description="등록 성공",
                schema=BoardCommentSerializer()
            )})
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
            board__school=user.school
        )

    @swagger_auto_schema(
        tags=['학교 커뮤니티'],
        operation_summary="학교 커뮤니티 게시글에 달린 특정 댓글 하나 조회",
        operation_description="학교 커뮤니티 게시글에 달린 특정 댓글 하나를 조회한다.",
        responses={200: openapi.Response(
            description="조회 성공",
            schema=BoardCommentSerializer()
        )})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        tags=['학교 커뮤니티'],
        operation_summary="학교 커뮤니티 게시글에 달린 특정 댓글 하나 수정",
        operation_description="학교 커뮤니티 게시글에 달린 특정 댓글 하나를 수정한다.",
        request_body=PostCommentListSerializer,
        responses={201: openapi.Response(
            description="조회 성공",
            schema=BoardCommentSerializer()
        )})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(
        tags=['학교 커뮤니티'],
        operation_summary="학교 커뮤니티 게시글에 달린 특정 댓글 하나 삭제",
        operation_description="학교 커뮤니티 게시글에 달린 특정 댓글 하나를 삭제한다.",
        responses={204: openapi.Response(
            description="삭제 성공"
        )})
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    # PATCH는 비활성화한다.
    @swagger_auto_schema(
        tags=['사용되지 않는 API'],
        operation_summary="사용X",
        operation_description="사용X"
        )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
