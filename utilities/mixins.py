from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

class CustomResponseMixin:
    def create_response(self, request, data=None, message=None, status_code=status.HTTP_200_OK):
        view_name = self.__class__.__name__
        if hasattr(self, 'get_view_name'):
            view_name = self.get_view_name()

        response_data = {
            'status': status_code,
            'data': data if data is not None else {},
            'message': f"{message} - Processing request for {view_name}." if message else f"Processing request for {view_name}."
        }
        return Response(response_data, status=status_code)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
            return self.create_response(request, data=paginated_data, message="List retrieved successfully")

        serializer = self.get_serializer(queryset, many=True)
        return self.create_response(request, data=serializer.data, message="List retrieved successfully")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.create_response(request, data=serializer.data, message="Detail retrieved successfully")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.create_response(request, data=serializer.data, message="Created successfully", status_code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.create_response(request, data=serializer.data, message="Updated successfully")