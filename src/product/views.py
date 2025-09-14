# from rest_framework.generics import GenericAPIView
from django.db.models import OuterRef, Subquery
from rest_framework import status, viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from src.product.models import AttributeProductModel, CategoryModel, PhotoProductModel, ProductModel
from src.product.pagination import ProductPagination
from src.product.permissions import (
    IsOwnerOrStaffOrReadOnlyPermission,
    IsOwnerProductOrStaffPermission,
    SalesManPermission,
)
from src.product.serializers import (
    AttributeProductSerializer,
    CategorySerializer,
    PhotoProductSerializer,
    ProductCreateUpdateSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
)

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


class ProductView(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin):
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    pagination_class = ProductPagination

    def get_queryset(self):
        main_photo = PhotoProductModel.objects.filter(product=OuterRef("pk"), is_main=True).values("image")[
            :1]
        queryset = ProductModel.objects.all().annotate(
            main_photo=Subquery(main_photo)
        ).select_related("user",
                         "category").prefetch_related(
            "photos", "attributes")
        if self.kwargs.get("slug"):
            queryset = queryset.filter(slug=self.kwargs.get("slug"))
        return queryset.filter(is_active=True)

    def get_serializer_class(self):
        serializer_class_slug = {
            "GET": ProductDetailSerializer,
            "PUT": ProductCreateUpdateSerializer,
            "PATCH": ProductCreateUpdateSerializer,
        }
        serializer_class_list = {
            "GET": ProductListSerializer,
            "POST": ProductCreateUpdateSerializer,
        }

        if self.kwargs.get("slug"):
            return serializer_class_slug.get(self.request.method, ProductCreateUpdateSerializer)
        return serializer_class_list.get(self.request.method, ProductCreateUpdateSerializer)

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = (SalesManPermission,)
        else:
            self.permission_classes = (IsOwnerOrStaffOrReadOnlyPermission,)
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoProductView(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin,
                       UpdateModelMixin, DestroyModelMixin):
    serializer_class = PhotoProductSerializer
    permission_classes = (IsOwnerProductOrStaffPermission,)

    def get_queryset(self):
        queryset = PhotoProductModel.objects.filter(product__user=self.request.user)
        if product_slug := self.kwargs.get('product_slug'):
            queryset = queryset.filter(product__slug=product_slug)
        return queryset


class AttributeProductView(viewsets.ModelViewSet):
    serializer_class = AttributeProductSerializer
    permission_classes = (IsOwnerProductOrStaffPermission,)

    def get_queryset(self):
        queryset = AttributeProductModel.objects.filter(product__user=self.request.user)
        if product_slug := self.kwargs.get('product_slug'):
            queryset = queryset.filter(product__slug=product_slug)
        return queryset
