# community/classboard/views.py

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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ClassBoard, Comment
from .serializers import *
from member.models import CustomUser


# 특정 학급 게시판 게시글 조회 API
class GetClassBoardAPI(APIView):
    @swagger_auto_schema(
        tags=['학급 커뮤니티'],
        operation_summary="학급 커뮤니티 게시글 조회",
        operation_description="특정 학급 커뮤니티에 작성된 게시글을 모두 불러온다.",
        responses={200: openapi.Response(
            description="조회 성공",
            schema=ClassBoardSerializer(many=True)
        )})
    def get(self, request, admission_year, grade, order):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        classBoardList = ClassBoard.objects.filter(grade=grade, order=order, admission_year=admission_year)
        serializer = ClassBoardSerializer(classBoardList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 학급 게시판 게시글 생성 API
class ClassBoardList(APIView):
    @swagger_auto_schema(
        tags=['학급 커뮤니티'],
        operation_summary="학급 커뮤니티 게시글 작성",
        operation_description="특정 학급 커뮤니티에 게시글을 작성한다.",
        request_body=PostClassBoardClientSerializer,
        responses={201: openapi.Response(
            description="작성 성공",
            schema=ClassBoardSerializer()
        )})
    def post(self, request):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        elif user.enrollYear is None:
            return Response({"message": "입학년도가 없는 유저는 글을 작성할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        grade = request.data.get('grade')
        if not grade:
            return Response({"message": "학년을 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        order = request.data.get('order')
        if not order:
            return Response({"message": "반을 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        admission_year = request.data.get('admission_year')
        if not admission_year:
            return Response({"message": "입학년도를 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        title = request.data.get('title')
        if not title:
            return Response({"message": "제목을 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        body = request.data.get('body')
        if not body:
            return Response({"message": "내용을 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)

        newClassBoard = ClassBoard.objects.create(
            user = user,
            title = title,
            body = body,
            school = user.school,
            grade = grade,
            order = order,
            admission_year = admission_year
        )

        serializer = ClassBoardSerializer(newClassBoard)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class GetClassBoardDetail(APIView):
    @swagger_auto_schema(
        tags=['학급 커뮤니티'],
        operation_summary="학급 커뮤니티 게시글 상세 조회",
        operation_description="특정 학급 커뮤니티에 작성된 게시글 하나를 상세 조회한다.",
        responses={200: openapi.Response(
            description="조회 성공",
            schema=ClassBoardSerializer()
        )})
    def get(self, request, classBoardId):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            theClassBoard = ClassBoard.objects.get(pk=classBoardId)
        except ClassBoard.DoesNotExist:
            return Response({"message": "존재하지 않는 게시글 id입니다."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClassBoardSerializer(theClassBoard)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class EditClassBoardDetail(APIView):
    @swagger_auto_schema(
        tags=['학급 커뮤니티'],
        operation_summary="학급 커뮤니티 게시글 수정",
        operation_description="특정 학급 커뮤니티에 작성된 게시글 하나를 수정한다.",
        request_body=EditClassBoardClientSerializer,
        responses={200: openapi.Response(
            description="조회 성공",
            schema=ClassBoardSerializer()
        )})
    def put(self, request):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        classBoardId = request.data.get('classBoardId')
        if not classBoardId:
            return Response({"message": "게시글 id를 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        title = request.data.get('title')
        if not title:
            return Response({"message": "제목을 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        body = request.data.get('body')
        if not body:
            return Response({"message": "내용을 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            theClassBoard = ClassBoard.objects.get(pk=classBoardId)
        except ClassBoard.DoesNotExist:
            return Response({"message": "존재하지 않는 게시글 id입니다."}, status=status.HTTP_404_NOT_FOUND)
        
        theClassBoard.title = title
        theClassBoard.body = body
        theClassBoard.save()
        
        serializer = ClassBoardSerializer(theClassBoard)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class DeleteClassBoardDetail(APIView):
    @swagger_auto_schema(
        tags=['학급 커뮤니티'],
        operation_summary="학급 커뮤니티 게시글 삭제",
        operation_description="특정 학급 커뮤니티에 작성된 게시글 하나를 삭제한다.",
        request_body=DeleteClassBoardClientSerializer,
        responses={204: openapi.Response(
            description="삭제 성공"
        )})
    def delete(self, request):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        classBoardId = request.data.get('classBoardId')
        if not classBoardId:
            return Response({"message": "게시글 id를 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            theClassBoard = ClassBoard.objects.get(pk=classBoardId)
        except ClassBoard.DoesNotExist:
            return Response({"message": "존재하지 않는 게시글 id입니다."}, status=status.HTTP_404_NOT_FOUND)
        
        theClassBoard.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# 학급 게시판 댓글 조회
class GetCommentAPI(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['학급 커뮤니티'],
        operation_summary="학급 커뮤니티 특정 게시글의 댓글 조회",
        operation_description="특정 학급 커뮤니티에 작성된 특정 게시글에 달린 모든 댓글들을 조회한다",
        responses={200: openapi.Response(
            description="조회 성공",
            schema=CommentSerializer(many=True)
        )})
    def get(self, request, classBoardId):
        try:
            thePost = ClassBoard.objects.get(pk=classBoardId)
        except ClassBoard.DoesNotExist:
            return Response({"message": "존재하지 않는 게시글 id입니다."}, status=status.HTTP_404_NOT_FOUND)
        
        commentList = thePost.comments.all()
        serializer = CommentSerializer(commentList, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

# 학급 게시판 댓글 달기
class PostCommentAPI(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['학급 커뮤니티'],
        operation_summary="학급 커뮤니티 게시글에 댓글 작성",
        operation_description="특정 학급 커뮤니티에 작성된 게시글에 댓글을 작성한다",
        request_body=PostCommentClientSerializer,
        responses={201: openapi.Response(
            description="등록 성공",
            schema=CommentSerializer()
        )})
    def post(self, request, *args, **kwargs):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        elif user.enrollYear is None:
            return Response({"message": "입학년도가 없는 유저는 댓글을 작성할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        classBoardId = request.data.get('classBoardId')
        if not classBoardId:
            return Response({"message": "게시글 id를 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            thePost = ClassBoard.objects.get(pk=classBoardId)
        except ClassBoard.DoesNotExist:
            return Response({"message": "존재하지 않는 게시글 id입니다."}, status=status.HTTP_404_NOT_FOUND)
        
        comment = request.data.get('comment')
        if not comment:
            return Response({"message": "댓글 내용을 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        newComment = Comment.objects.create(
            user = user,
            class_board = thePost,
            comment = comment
        )
        serializer = CommentSerializer(newComment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# 댓글 상세 조회
class CommentDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['학급 커뮤니티'],
        operation_summary="학급 커뮤니티 댓글 상세 조회",
        operation_description="특정 학급 커뮤니티에 작성된 댓글 하나를 조회한다",
        responses={200: openapi.Response(
            description="조회 성공",
            schema=CommentSerializer()
        )})
    def get(self, request, commentId):
        try:
            theComment = Comment.objects.get(pk=commentId)
        except Comment.DoesNotExist:
            return Response({"message": "존재하지 않는 댓글 id입니다."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentSerializer(theComment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# 댓글 수정
class EditCommentAPI(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['학급 커뮤니티'],
        operation_summary="학급 커뮤니티 댓글 수정",
        operation_description="특정 학급 커뮤니티에 작성된 댓글 하나를 수정한다",
        request_body=EditCommentClientSerializer,
        responses={201: openapi.Response(
            description="수정 성공",
            schema=CommentSerializer()
        )})
    def put(self, request):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        elif user.enrollYear is None:
            return Response({"message": "입학년도가 없는 유저는 댓글을 수정할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        commentId = request.data.get('commentId')
        if not commentId:
            return Response({"message": "댓글 id를 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            theComment = Comment.objects.get(pk=commentId)
        except Comment.DoesNotExist:
            return Response({"message": "존재하지 않는 댓글 id입니다."}, status=status.HTTP_404_NOT_FOUND)
        
        comment = request.data.get('comment')
        if not comment:
            return Response({"message": "댓글 내용을 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        theComment.comment = comment
        theComment.save()

        serializer = CommentSerializer(theComment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 댓글 삭제
class DeleteCommentAPI(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['학급 커뮤니티'],
        operation_summary="학급 커뮤니티 댓글 삭제",
        operation_description="특정 학급 커뮤니티에 작성된 댓글 하나를 삭제한다",
        request_body=DeleteCommentClientSerializer,
        responses={204: openapi.Response(
            description="삭제 성공"
        )})
    def delete(self, request):
        commentId = request.data.get('commentId')
        if not commentId:
            return Response({"message": "댓글 id를 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            theComment = Comment.objects.get(pk=commentId)
        except Comment.DoesNotExist:
            return Response({"message": "존재하지 않는 댓글 id입니다."}, status=status.HTTP_404_NOT_FOUND)
        
        theComment.delete()
        return Response({"message": "삭제가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT)