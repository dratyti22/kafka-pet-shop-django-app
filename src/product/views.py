from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.product.models import CategoryModel
from src.product.serializers import CategorySerializer


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
