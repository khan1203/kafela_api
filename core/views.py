import random
from .models import User, Book, BookRequest, Review, Category
from .filters import BookFilter
from rest_framework import generics, status, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminUser, IsRegularUser
from .serializers import RegisterSerializer, BookSerializer, BookRequestSerializer, ReviewSerializer, CategorySerializer

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author', 'description']  # what user can search by

    def get_permissions(self):
        if self.request.user.is_staff:
            return [IsAdminUser()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        # Allow anyone to read, only admin can create/edit/delete
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

class BookRequestListCreateView(generics.ListCreateAPIView):
    queryset = BookRequest.objects.all()
    serializer_class = BookRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return BookRequest.objects.all()
        return BookRequest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookRequest.objects.all()
    serializer_class = BookRequestSerializer
    permission_classes = [IsAuthenticated]

class BookReviewListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        reviews = Review.objects.filter(book_id=pk)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        book = Book.objects.get(pk=pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RandomReviewList(APIView):
    def get(self, request):
        reviews = list(Review.objects.all())
        random.shuffle(reviews)
        serializer = ReviewSerializer(reviews[:10], many=True)
        return Response(serializer.data)

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        return Response({
            "total_books": Book.objects.count(),
            "total_users": User.objects.filter(is_staff=False).count(),
            "total_requests": BookRequest.objects.count(),
            "total_reviews": Review.objects.count(),
        })

class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsRegularUser]

    def get(self, request):
        user = request.user
        return Response({
            "full_name": user.full_name,
            "total_requested": BookRequest.objects.filter(user=user).count(),
            "total_reviews": Review.objects.filter(user=user).count(),
            "total_book_read": user.total_book_read,
        })















"""
class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"message": "Welcome Admin!"})


class UserDashboardView(APIView):
    permission_classes = [IsRegularUser]

    def get(self, request):
        return Response({"message": "Welcome User!"})

"""