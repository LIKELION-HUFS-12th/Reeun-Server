# board/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Board, Comment
from .serializers import BoardSerializer, CommentSerializer

class BoardList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BoardDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            board = Board.objects.get(pk=post_id)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = BoardSerializer(board)
        return Response(serializer.data)

    def put(self, request, post_id):
        try:
            board = Board.objects.get(pk=post_id)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = BoardSerializer(board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        try:
            board = Board.objects.get(pk=post_id)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            board = Board.objects.get(pk=post_id)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        comments = board.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_id):
        try:
            board = Board.objects.get(pk=post_id)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            # 댓글 작성 시 'user'와 'board'를 설정하여 저장
            comment = serializer.save(user=request.user, board=board)
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id, board_id=post_id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
