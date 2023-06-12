from django.urls import path
from .views import MainPageView, ProductDetail, order_create, OrdersList, OrderDetail, CategoryDetailView, \
    CommentEditView, IndexView, ProfileUpdate, SupportView
from .views import subscribe_category, unsubscribe_category, subscribe_product, unsubscribe_product

urlpatterns = [
    path('', MainPageView.as_view(), name='base'),
    path('<int:pk>', ProductDetail.as_view(), name='product'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category'),
    path('order/', order_create, name='order_create'),
    path('orders/', OrdersList.as_view(), name='orders'),
    path('order/<int:pk>', OrderDetail.as_view(), name='order'),
    path('comment/<int:pk>', CommentEditView.as_view(), name='com_edit'),
    path('my_page', IndexView.as_view()),
    path('my_page/edit', ProfileUpdate.as_view(), name='profile_edit'),
    path('subscribe/<int:pk>', subscribe_category, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe_category, name='unsubscribe'),
    path('sub/<int:pk>', subscribe_product, name='sub'),
    path('unsub/<int:pk>', unsubscribe_product, name='unsub'),
    path('support', SupportView.as_view(), name='support'),
]
