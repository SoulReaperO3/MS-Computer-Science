from django.urls import path
from contactTracer import views

urlpatterns = [
   path('',views.index),
   path('traceContact/<str:subjectID>/<int:date>/',views.traceContact),
]
