from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('restaurant/<int:restaurant_id>/menu/', restaurant_menu, name='restaurant_menu'),
    path('restaurant/<int:restaurant_id>/create_request/', create_request, name='create_request'),
    path('order_request/<int:request_id>/', order_request_detail, name='order_request_detail'),
    path('order_request/<int:request_id>/join/', join_request, name='join_request'),
    path('order_request/<int:request_id>/add_item/<int:menu_item_id>/', add_item_to_order, name='add_item_to_order'),
    path('order_request/<int:request_id>/close/', close_request, name='close_request'),
    path('order_request/<int:request_id>/finish/', finish_request, name='finish_request'),
    path('order/<int:request_id>/remove-item/<int:menu_item_id>/', remove_item_from_order, name='remove_item_from_order'),

]
