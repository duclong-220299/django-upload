from django.urls import path, include
from . import views

app_name = "api"

urlpatterns = [
    path(
        "photo/upload/",
        views.PhotoModelViewSet.as_view({"post": "create"}),
        name="photo-upload",
    ),
    path("photo/delete/<pk>/", views.PhotoDeleteView.as_view(), name="delete_photo"),
]
