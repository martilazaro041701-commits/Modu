from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AnalyticsDashboardView,
    ShopAnalyticsView,
    JobStatusUpdateView,
    JobAnalyticsView,
    JobTransitionUpdateView,
    JobViewSet,
    StatusViewSet,
    RepairJobViewSet,
    UnsyncedCustomerView,
)

# 1. Create a router and register viewsets
router = DefaultRouter()
router.register(r'statuses', StatusViewSet)
router.register(r'jobs', RepairJobViewSet)
router.register(r'tracker-jobs', JobViewSet)

# 2. The API URLs 
urlpatterns = [
    path('', include(router.urls)),
    path('jobs/<int:pk>/status/', JobStatusUpdateView.as_view(), name='bark-job-status-update'),
    path('jobs/<int:pk>/update_status/', JobTransitionUpdateView.as_view(), name='bark-job-transition-update'),
    path('customers/unsynced/', UnsyncedCustomerView.as_view(), name='bark-customers-unsynced'),
    path('analytics/', AnalyticsDashboardView.as_view(), name='bark-analytics-dashboard'),
    path('analytics/jobs/', JobAnalyticsView.as_view(), name='bark-job-analytics'),
    path('analytics/shop/', ShopAnalyticsView.as_view(), name='bark-shop-analytics'),
]
