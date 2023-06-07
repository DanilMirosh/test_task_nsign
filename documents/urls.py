from django.urls import path
from .views import (
    CreateDocumentView,
    EditDocumentView,
    ViewDocumentView,
    DeleteDocumentView,
    CompareVersionsView,
    DocumentListView,
)

app_name = 'documents'

urlpatterns = [
    path('create/', CreateDocumentView.as_view(), name='create_document'),
    path('edit/<int:document_id>/', EditDocumentView.as_view(), name='edit_document'),
    path('view/<int:document_id>/', ViewDocumentView.as_view(), name='view_document'),
    path('delete/<int:document_id>/', DeleteDocumentView.as_view(), name='delete_document'),
    path('compare/<int:document_id>/', CompareVersionsView.as_view(), name='compare_versions'),
    path('', DocumentListView.as_view(), name='document_list'),
]
