# community/board/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Board, Comment, School
from .serializers import BoardSerializer, CommentSerializer
from member.models import UserProfile

# 게시글 목록 조회 및 게시글 작성
class BoardList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        school_instance = School.objects.get(id=profile.school.id)

        if not isinstance(school_instance, School):
            return Response({"error": "Invalid school reference"}, status=status.HTTP_400_BAD_REQUEST)

        boards = Board.objects.filter(school=school_instance)
        if not boards.exists():
            return Response({"error": "No boards found for the school"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_school_id = profile.school.id

        data = request.data.copy()
        data['school'] = user_school_id  

        serializer = BoardSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            board = serializer.save(user=request.user)  
            return Response(BoardSerializer(board).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 특정 게시글의 상세 조회, 수정, 삭제
class BoardDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            board = Board.objects.get(pk=post_id)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if board.school.id != profile.school.id:  # 유저의 학교와 게시글의 학교가 일치하는지 확인
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = BoardSerializer(board)
        return Response(serializer.data)

    def put(self, request, post_id):
        try:
            board = Board.objects.get(pk=post_id)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if board.school.id != profile.school.id:  # 유저의 학교와 게시글의 학교가 일치하는지 확인
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = BoardSerializer(board, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        try:
            board = Board.objects.get(pk=post_id)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if board.school.id != profile.school.id:  # 유저의 학교와 게시글의 학교가 일치하는지 확인
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 특정 게시글에 대한 댓글 목록 조회 및 댓글 작성
class CommentList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            board = Board.objects.get(pk=post_id)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if board.school.id != profile.school.id: 
            return Response({"error": "You do not have permission to view comments on this board."}, status=status.HTTP_403_FORBIDDEN)
        
        comments = board.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_id):
        try:
            board = Board.objects.get(pk=post_id)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if board.school.id != profile.school.id:  
            return Response({"error": "You do not have permission to comment on this board."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(user=request.user, board=board)
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 특정 게시글에 대한 특정 댓글 삭제
class CommentDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id, board_id=post_id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if comment.board.school.id != profile.school.id:  # 유저의 학교와 게시글의 학교가 일치하는지 확인
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)