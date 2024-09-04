# community/classboard/views.py

from django.http import Http404 
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import ClassBoard, Comment
from .serializers import ClassBoardSerializer, CommentSerializer
from member.models import UserProfile

class ClassBoardList(generics.ListCreateAPIView):
    serializer_class = ClassBoardSerializer
    permission_classes = [IsAuthenticated]

    def get_profile(self):
        user = self.request.user
        try:
            return UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return None

    def get_queryset(self):
        profile = self.get_profile()
        if not profile:
            return ClassBoard.objects.none()

        grade = self.kwargs.get('grade')
        if not grade:
            return ClassBoard.objects.none()

        grade_key = f'grade_{grade}'
        class_number_field = f'class_number_{grade}'
        class_number = profile.grades.get(grade_key, {}).get(class_number_field)

        if class_number is None:
            return ClassBoard.objects.none()

        admission_year = profile.admission_year

        return ClassBoard.objects.filter(
            grade=grade,
            class_number=class_number,
            school=profile.school,
            admission_year=admission_year
        )

    def post(self, request, *args, **kwargs):
        profile = self.get_profile()
        if not profile:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        grade = self.kwargs.get('grade')
        if not grade:
            return Response({"detail": "Grade not provided."}, status=status.HTTP_400_BAD_REQUEST)

        grade_key = f'grade_{grade}'
        class_number_field = f'class_number_{grade}'
        class_number = profile.grades.get(grade_key, {}).get(class_number_field)

        if class_number is None:
            return Response({"detail": "No class number available for the given grade."}, status=status.HTTP_400_BAD_REQUEST)

        admission_year = profile.admission_year

        data = request.data.copy()
        if 'school' in data:
            data.pop('school')

        serializer = self.get_serializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user, school=profile.school, admission_year=admission_year)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClassBoardDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassBoardSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'  

    def get_profile(self):
        user = self.request.user
        try:
            return UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return None

    def get_queryset(self):
        profile = self.get_profile()
        if not profile:
            return ClassBoard.objects.none()

        grade = self.kwargs.get('grade')
        post_id = self.kwargs.get('post_id')
        if not grade or not post_id:
            return ClassBoard.objects.none()

        grade_key = f'grade_{grade}'
        class_number_field = f'class_number_{grade}'
        class_number = profile.grades.get(grade_key, {}).get(class_number_field)

        if class_number is None:
            return ClassBoard.objects.none()

        admission_year = profile.admission_year

        return ClassBoard.objects.filter(
            grade=grade,
            class_number=class_number,
            id=post_id,
            school=profile.school,
            admission_year=admission_year
        )

    def get_object(self):
        queryset = self.get_queryset()
        post_id = self.kwargs.get('post_id')
        try:
            return queryset.get(id=post_id)
        except ClassBoard.DoesNotExist:
            raise Http404
        
class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_profile(self):
        user = self.request.user
        try:
            return UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return None

    def get_queryset(self):
        profile = self.get_profile()
        if not profile:
            return Comment.objects.none()

        grade = self.kwargs.get('grade')
        post_id = self.kwargs.get('post_id')

        if post_id:  
            return Comment.objects.filter(
                class_board__grade=grade,
                class_board__id=post_id,
                class_board__school=profile.school,
                class_board__admission_year=profile.admission_year
            )
        else:  
            return Comment.objects.filter(
                class_board__grade=grade,
                class_board__school=profile.school,
                class_board__admission_year=profile.admission_year
            )

    def post(self, request, *args, **kwargs):
        profile = self.get_profile()
        if not profile:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        grade = self.kwargs.get('grade')
        post_id = self.kwargs.get('post_id')
        if not grade or not post_id:
            return Response({"detail": "Grade or post ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        grade_key = f'grade_{grade}'
        class_number_field = f'class_number_{grade}'
        class_number = profile.grades.get(grade_key, {}).get(class_number_field)

        if class_number is None:
            return Response({"detail": "No class number available for the given grade."}, status=status.HTTP_400_BAD_REQUEST)

        admission_year = profile.admission_year

        data = request.data.copy()
        data['class_board'] = post_id

        serializer = self.get_serializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'  

    def get_profile(self):
        user = self.request.user
        try:
            return UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return None

    def get_queryset(self):
        profile = self.get_profile()
        if not profile:
            return Comment.objects.none()

        grade = self.kwargs.get('grade')
        post_id = self.kwargs.get('post_id')
        comment_id = self.kwargs.get('pk') 
        if not grade or not post_id or not comment_id:
            return Comment.objects.none()

        grade_key = f'grade_{grade}'
        class_number_field = f'class_number_{grade}'
        class_number = profile.grades.get(grade_key, {}).get(class_number_field)

        if class_number is None:
            return Comment.objects.none()

        admission_year = profile.admission_year

        return Comment.objects.filter(
            class_board__grade=grade,
            class_board__class_number=class_number,
            class_board__id=post_id,
            id=comment_id,
            class_board__school=profile.school,
            class_board__admission_year=admission_year
        )
