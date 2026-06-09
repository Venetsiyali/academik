from django.urls import path
from .views import (
    ObservationListView, ObservationCreateView, 
    ResourceListView, ResourceCreateView,
    methodist_dashboard, observation_journal,
    SubjectListView, SubjectCreateView, SubjectUpdateView, SubjectDeleteView
)

urlpatterns = [
    path('methodist/', methodist_dashboard, name='methodist_dashboard'),
    path('observations/', ObservationListView.as_view(), name='observation_list'),
    path('observations/journal/', observation_journal, name='observation_journal'),
    path('observations/new/', ObservationCreateView.as_view(), name='observation_create'),
    path('resources/', ResourceListView.as_view(), name='resource_list'),
    path('resources/new/', ResourceCreateView.as_view(), name='resource_create'),
    
    # Subject URLs
    path('subjects/', SubjectListView.as_view(), name='subject_list'),
    path('subjects/new/', SubjectCreateView.as_view(), name='subject_create'),
    path('subjects/<uuid:pk>/edit/', SubjectUpdateView.as_view(), name='subject_update'),
    path('subjects/<uuid:pk>/delete/', SubjectDeleteView.as_view(), name='subject_delete'),
]
