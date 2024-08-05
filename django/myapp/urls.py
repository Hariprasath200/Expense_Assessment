from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, ExpenseViewSet, ExpenseListView, UserDetailView, ExpenseCreateView
from django.urls import path
from .views import get_csrf_token

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/expenses/create/', ExpenseCreateView.as_view(), name='create_expense'),
    path('api/expenses/', ExpenseListView.as_view(), name='expense-list'),
    path('api/user/', UserDetailView.as_view(), name='user-detail'),
    path('api/csrf_token/', get_csrf_token, name='csrf_token'),
    # Include the router URLs for CRUD operations on expenses
    path('api/', include(router.urls)),
]
# urls.py


