from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from src.product.models import CategoryModel, ProductModel
from src.product.serializers import CategorySerializer, ProductSerializer, ProductGetSerializer


# class CategoryView(ListAPIView):
#     queryset = CategoryModel.objects.all()
#     serializer_class = CategorySerializer
#     lookup_url_kwarg = "slug"

class CategoryView(APIView):

    def get_queryset(self):
        if self.kwargs.get("slug"):
            queryset = CategoryModel.objects.filter(slug=self.kwargs.get("slug"))
        else:
            queryset = CategoryModel.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset and self.kwargs.get("slug"):
            return Response(
                {"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductView(GenericAPIView, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
                  DestroyModelMixin):

    def get_queryset(self):
        if self.kwargs.get("slug"):
            return ProductModel.objects.filter(slug=self.kwargs.get("slug"))
        return ProductModel.objects.all()

    def get_serializer_class(self):
        serializer_class_slug = {
            "GET": ProductGetSerializer,
            "PUT": None,
            "PATCH": None,
            "DELETE": None,
        }
        serializer_class_list = {
            "GET": ProductSerializer,
            "POST": None,
        }
        if self.kwargs.get("slug"):
            return serializer_class_slug.get(self.request.method, ProductSerializer)
        else:
            return serializer_class_list.get(self.request.method, ProductGetSerializer)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset or not self.kwargs.get("slug"):
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
