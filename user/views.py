from django.shortcuts import render
from rest_framework.generics import (
                                    CreateAPIView,
                                    ListAPIView,
                                    RetrieveAPIView,
                                    UpdateAPIView
                                    )
from .serializers import UserSerializer, PropertySerializer
from .utils import ( ResponseInfo, CustomPagination)
from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser, Property
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache


# Create your views here.


class UserSignUpAPIView(CreateAPIView):
    """
    Class for creating API view for user signup.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(UserSignUpAPIView, self).__init__(**kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            self.response_format["data"] = serializer.data
            self.response_format["status_code"] = status.HTTP_201_CREATED
            self.response_format["error"] = None
            self.response_format["message"] = "User Created Successfully"
        return Response(self.response_format)


class UserListAPIView(ListAPIView):
    """
    Class for creating API view for user signup.
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(UserListAPIView, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        page = self.paginate_queryset(users)
        user_list = self.get_serializer(page, many = True)

        return self.get_paginated_response(user_list.data)


class AddPropertyView(CreateAPIView):
    """
    class to add a new property
    """
    serializer_class = PropertySerializer
    authentication_classes = ()
    permission_classes = ()

    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(AddPropertyView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        property_listing = PropertySerializer(data=request.data)
        if property_listing.is_valid(raise_exception=True):
            property_listing.save()
            self.response_format['data'] = property_listing.data
            self.response_format['message'] = "Property Add Successfully"
        return Response(self.response_format)


class PropertyDetailView(RetrieveAPIView):
    """
    class to retrieve the details of a property
    """
    serializer_class = PropertySerializer
    authentication_classes = ()
    permission_classes = ()

    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(PropertyDetailView, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        property_id = self.kwargs['id']
        cache_data = cache.get(str(property_id))
        if cache_data:
            data = cache.get(str(property_id))
            self.response_format['data'] = data
            self.response_format['message'] = "From cache"
        else:
            property_model = Property.objects.get(id = property_id)
            property_detail = self.get_serializer(property_model)
            data = property_detail.data
            cache.set(property_id, data)
            self.response_format['data'] = data
            self.response_format['message'] = "From db"

        return Response(self.response_format)


class PropertiesView(ListAPIView):
    """
    class to listing of all properties
    """
    serializer_class = PropertySerializer
    authentication_classes = ()
    permission_classes = ()
    pagination_class = CustomPagination

    def get_queryset(self):
        return Property.objects.all().order_by("id")

    @method_decorator(cache_page(60*60))
    def get(self, request, *args, **kwargs):
        properties = self.get_queryset()
        page = self.paginate_queryset(properties)
        properties_list = PropertySerializer(page, many = True)

        return self.get_paginated_response(properties_list.data)


class UpdatePropertyView(UpdateAPIView):
    """
    class to update the properties details
    """
    serializer_class = PropertySerializer
    authentication_classes = ()
    permission_classes = ()

    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(UpdatePropertyView, self).__init__(**kwargs)

    def update(self, request, *args, **kwargs):
        property_id = self.kwargs['id']
        cache.delete(str(property_id))
        property_info = Property.objects.get(id = property_id)
        property_detail = PropertySerializer(property_info, data= request.data)
        if property_detail.is_valid(raise_exception= True):
            property_detail.save()
            cache.set(property_id, property_detail.data)
            self.response_format['data'] = property_detail.data
            self.response_format['message'] = "Update Success"
        return Response(self.response_format)
