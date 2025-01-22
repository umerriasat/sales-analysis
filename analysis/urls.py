from django.urls import path
from .views import RepPerformance, TeamPerformance, UploadEmployeeData, PerformanceTrends

urlpatterns = [
    path('upload/', UploadEmployeeData.as_view(), name='upload'),
    path('rep/perfomance/', RepPerformance.as_view(), name='RepPerformance'),
    path('team/perfomnce/', TeamPerformance.as_view(), name='TeamPerformance'),
    path('trends/perfomnce/', PerformanceTrends.as_view(), name='TeamPerformance'),

]