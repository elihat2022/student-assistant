from django.urls import path
from .views import Record_View, Transcription_List, Transcription_Detail, home, UpdateTranscriptionDetail, DeleteTranscription

urlpatterns = [
    path('recording', Record_View, name='recording'),
    path('', home, name='home'),
    path('transcriptions', Transcription_List.as_view(), name='transcriptions'),
    path('transcription/<int:pk>/', Transcription_Detail.as_view(), name='transcription_detail'),
    path('transcription_update/<int:pk>/', UpdateTranscriptionDetail.as_view(), name='transcription_update'),
    path('transcription_delete/<int:pk>/',DeleteTranscription.as_view(), name='transcription_delete'),
    
]