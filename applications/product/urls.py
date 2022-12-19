from django.urls import path, include
from applications.product.views import ProductAPIView, CommentAPIView, OrderActivateApiView, \
    OrderApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('comment', CommentAPIView)
router.register('buy', OrderApiView)


router.register('', ProductAPIView)

urlpatterns = [
    # path('', PostAPIView.as_view({'get': 'list', 'post': 'create'})),
    # path('', include(router.urls))
    path('buy/<uuid:order_code>/', OrderActivateApiView.as_view())
]

#* способ написания
urlpatterns += router.urls