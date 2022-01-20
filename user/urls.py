from django.contrib import admin
from django.urls import path
from .views import (UserSignUpAPIView,
                    UserListAPIView,
                    AddPropertyView,
                    PropertiesView,
                    PropertyDetailView,
                    UpdatePropertyView,
                    )

urlpatterns = [
    path('signUp/', UserSignUpAPIView.as_view(), name="sign-up"),
    path('userList/', UserListAPIView.as_view(), name="user-list"),
    path('addProperty/', AddPropertyView.as_view(), name="add-property"),
    path('propertyList/', PropertiesView.as_view(), name="properties"),
    path('propertyDetail/<int:id>/', PropertyDetailView.as_view(), name="user-list"),
    path('updateProperty/<int:id>/', UpdatePropertyView.as_view(), name="update-property"),
]