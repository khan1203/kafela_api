from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterView, 
    AdminDashboardView, 
    UserDashboardView, 
    BookViewSet, 
    BookRequestListCreateView,
    BookRequestDetailView,
    BookReviewListCreate,
    RandomReviewList,
    CategoryViewSet
)

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet) 

urlpatterns = [

    path('', include(router.urls)),

    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Book Requests
    path('book_requests/', BookRequestListCreateView.as_view(), name='book-request-list'),
    path('book_requests/<int:pk>/', BookRequestDetailView.as_view(), name='book-request-detail'),

    # Book Reviews
    path('books/<int:pk>/reviews/', BookReviewListCreate.as_view(), name='book-reviews'),
    path('random_reviews/', RandomReviewList.as_view(), name='random-reviews'),

    # Dashboard
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('dashboard/', UserDashboardView.as_view(), name='user-dashboard'),
]
