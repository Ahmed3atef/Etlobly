from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages

@login_required
def dashboard(request):
    # Retrieve all restaurants for the restaurants tab
    restaurants = Restaurant.objects.all()
    
    # Get orders created by the user
    created_orders = OrderRequest.objects.filter(order_maker=request.user)
    
    # Get orders the user has joined but did not create
    joined_orders = OrderRequest.objects.filter(order_receivers = request.user).exclude(order_maker=request.user)
    
    # Combine these orders under "open_requests"
    open_requests = OrderRequest.objects.all()  # Combines both QuerySets
    
    return render(request, 'core/index.html', {
        "restaurants": restaurants,
        "created_orders": created_orders,
        "joined_orders": joined_orders,
        "open_requests":open_requests
    })

@login_required
def restaurant_menu(request, restaurant_id):
    # Get the restaurant by ID
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    # Fetch the menu for the restaurant and all associated items
    menu_items = MenuItem.objects.filter(menus__restaurant=restaurant)

    context = {
        'restaurant': restaurant,
        'menu_items': menu_items,
    }
    return render(request, 'core/restaurant_menu.html', context)

@login_required
def create_request(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    order_request = OrderRequest.objects.create(
        restaurant=restaurant, 
        order_maker=request.user,
    )
    messages.success(request, "Request created successfully!")
    return redirect('order_request_detail', order_request.id)

@login_required
def join_request(request, request_id):
    order_request = get_object_or_404(OrderRequest, id=request_id, is_closed=False)
    
    if request.user not in order_request.order_receivers.all():
        order_request.order_receivers.add(request.user)
        order_request.save()
    return redirect('order_request_detail', request_id)

@login_required
def order_request_detail(request, request_id):
    order_request = get_object_or_404(OrderRequest, id=request_id)
    menus = order_request.restaurant.menus.all()  # Get the menus for the restaurant
    menu_items = MenuItem.objects.filter(menus__in=menus)  # Get all menu items in these menus
    
    order_items = order_request.order_items.all()
    
    # Calculate the total cost of all items in the order
    items_total_cost = sum(item.item_cost for item in order_items)
    
    # Calculate the overall total cost by adding the full delivery cost once
    overall_order_total_cost = items_total_cost + order_request.restaurant.delivery_cost
    
    # Get unique users who have added items to the order
    users_in_order = {item.user for item in order_items}
    number_of_users = len(users_in_order)

    # Avoid dividing by zero in case there are no items ordered
    if number_of_users > 0:
        delivery_cost_per_user = order_request.restaurant.delivery_cost / number_of_users
    else:
        delivery_cost_per_user = 0

    # Calculate the total cost for the current user including their share of the delivery cost
    user_total_cost = sum(
        item.item_cost for item in order_items if item.user == request.user
    )

    return render(request, 'core/order_request_detail.html', {
        'order_request': order_request,
        'menus': menus,
        'menu_items': menu_items,
        'order_items': order_items,
        'user_total_cost': user_total_cost,
        'delivery_cost_per_user': delivery_cost_per_user,
        'overall_order_total_cost': overall_order_total_cost,  # This includes the full delivery cost
    })

@login_required
def add_item_to_order(request, request_id, menu_item_id):
    order_request = get_object_or_404(OrderRequest, id=request_id)
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)

    if order_request.is_closed:
        messages.error(request, "Cannot add items to a closed request.")
        return redirect('order_request_detail', request_id)

    # Check if the item already exists for the user in this order
    order_item, created = OrderItem.objects.get_or_create(
        order_request=order_request,
        user=request.user,
        menu_item=menu_item,
        defaults={'quantity': 1, 'item_cost': menu_item.price}
    )
    
    if not created:
        # If the item already exists, update the quantity and cost
        order_item.quantity += 1
        order_item.item_cost += menu_item.price
        order_item.save()
    
    # Update the total cost to include the delivery cost
    order_request.total_cost = (
        sum(item.item_cost for item in order_request.order_items.all())
        + order_request.restaurant.delivery_cost
    )
    order_request.save()

    messages.success(request, "Item added to order.")
    return redirect('order_request_detail', request_id)

@login_required
def close_request(request, request_id):
    order_request = get_object_or_404(OrderRequest, id=request_id, order_maker=request.user)
    order_request.is_closed = True
    order_request.save()
    messages.success(request, "Request has been closed.")
    return redirect('order_request_detail', request_id)

@login_required
def finish_request(request, request_id):
    order_request = get_object_or_404(OrderRequest, id=request_id, order_maker=request.user)
    order_request.delete()  # Permanently delete the order after finishing
    messages.success(request, "Request has been completed and removed.")
    return redirect('dashboard')  # Redirect to dashboard or home page

@login_required
def remove_item_from_order(request, request_id, menu_item_id):
    order_request = get_object_or_404(OrderRequest, id=request_id)
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    
    # Get the OrderItem for the user and menu_item
    try:
        order_item = OrderItem.objects.get(order_request=order_request, user=request.user, menu_item=menu_item)
    except OrderItem.DoesNotExist:
        messages.error(request, "Item not found in your order.")
        return redirect('order_request_detail', request_id=request_id)
    
    # Decrease quantity or delete item if quantity is 1
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.item_cost = order_item.menu_item.price * order_item.quantity
        order_item.save()
    else:
        order_item.delete()

    # Update the total cost of the order request
    order_request.total_cost = sum(item.item_cost for item in order_request.order_items.all())
    order_request.save()

    messages.success(request, "Item quantity updated.")
    return redirect('order_request_detail', request_id=request_id)