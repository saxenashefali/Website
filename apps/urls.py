from django.urls import path
from apps.views import docTypeView

urlpatterns = [
    path('', docTypeView.as_view()),
]
