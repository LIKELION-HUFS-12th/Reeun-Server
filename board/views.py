from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Board, Comment
from .serializers import BoardSerializer, CommentSerializer

# 게시판 목록 조회 및 게시글 작성
class BoardList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # 게시판 목록 조회
    def get(self, request):
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    # 게시글 작성
    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 게시글 상세 조회, 수정, 삭제
class BoardDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # 게시글 상세 조회
    def get(self, request, post_id):
        try:
            board = Board.objects.get(pk=post_id)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = BoardSerializer(board)
        return Response(serializer.data)

    # 게시글 수정
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

    # 게시글 삭제
    def delete(self, request, post_id):
        try:
            board = Board.objects.get(pk=post_id)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 댓글 목록 조회 및 댓글 작성
class CommentList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # 게시글에 대한 댓글 목록 조회
    def get(self, request, post_id):
        try:
            board = Board.objects.get(pk=post_id)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        comments = board.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    # 댓글 작성
    def post(self, request, post_id):
        try:
            board = Board.objects.get(pk=post_id)
        except Board.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(user=request.user, board=board)
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 댓글 삭제
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
