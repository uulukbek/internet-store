from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet
from applications.product.models import Product, Comment, Like, Rating, Order
from applications.product.serializers import RatingSerializer, CommentSerializer, ProductSerializer
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from applications.product.permissions import IsOwner, IsCommentOwner
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework.pagination import PageNumberPagination


# Пагинация
class LargeResultSetPagination(PageNumberPagination):
    page_size = 4
    page_size_query_parm = 'page_size'
    max_page_size = 10000


#ModelViewSet
class ProductAPIView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwner]
    pagination_class = LargeResultSetPagination
    filterset_fields = ['category', 'owner']
    search_fields = ['title', 'description']
    ordering_fields = ['id']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk, *args, **kwargs):  # post/id/like
        like_obj, _ = Like.objects.get_or_create(post_id=pk, owner=request.user)
        like_obj.like = not like_obj.like
        like_obj.save()
        status = 'liked'
        if not like_obj.like:
            status = 'unliked'
        return Response({'status': status})

    @action(detail=True, methods=['POST'])
    def rating(self, request, pk, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating_obj, _ = Rating.objects.get_or_create(post_id=pk, owner=request.user)
        rating_obj.rating = request.data['rating']
        rating_obj.save()
        return Response({'status': status.HTTP_201_CREATED})


class CommentAPIView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queriset = super().get_queryset()
        queriset = queriset.filter(owner=self.request.user)
        return queriset


class OrderApiView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return Response('We have sent you an order confirmation code to your email!')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response('We have sent you an order confirmation code to your email!')


class OrderActivateApiView(APIView):
    def get(self, request, order_code):
        try:
            order = Order.objects.get(order_code=order_code)
            order.order = True
            order.order_code = ''
            ordered_count = order.amount
            product_obj = order.product_obj
            count = product_obj.amount
            product_obj.amount = count - ordered_count
            product_obj.save()
            order.save()
            return Response({'msg': 'Успешно'})
        except Order.DoesNotExist:
            return Response({'msg': 'Ошибка'})
