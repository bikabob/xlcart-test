from django.shortcuts import render
import json
# Create your views here.
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import Product, Cart, CartItem,Categories
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.core.mail import send_mail

def index(request):
    products = Product.objects.all()
    categories = Categories.objects.filter(parent__isnull=True)  # Fetch all categories
    subcategories = categories.filter(parent__isnull=False)  # Fetch subcategories
    
    context = {
        "instance": products,
        "categories": categories,
        "subcategories": subcategories,
    }
    return render(request, 'index.html', context=context)

def search_results(request):
    search_title = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=search_title) if search_title else Product.objects.none()
    categories = Categories.objects.filter(parent__isnull=True)
    
    context = {
        "instance": products,
        "categories": categories,
    }
    return render(request, 'products.html', context)

def category_view(request, pk):
    category = get_object_or_404(Categories, pk=pk)
    products = Product.objects.filter(category=category)  # Adjust if you have category-product relation
    categories = Categories.objects.filter(parent__isnull=True)  # Fetch all categories
    subcategories = categories.filter(parent__isnull=False)  
    context = {
        "category": category,
        "instance": products,
        "categories": categories,
        "subcategories": subcategories,
    }
    return render(request, 'products.html', context=context)


def detail_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Categories.objects.filter(parent__isnull=True)  # Fetch all categories
    subcategories = categories.filter(parent__isnull=False)  
    gallery_images = product.galleries.all()
    search_title = request.GET.get("q")
    if search_title:
        product=product.filter(name__icontains=search_title)
    context={
        'instance': product,
        'gallery_img': gallery_images,
        "categories": categories,
        "subcategories": subcategories,
    }
    return render(request, 'product_details.html',context=context)

@login_required(login_url="Users:login")
@csrf_exempt
def add_cart(request, pk):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=pk)
        quantity = int(request.POST.get("quantity", 1))
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=product)
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            "title": "Successfully submitted",
            "message": "Successfully submitted",
            "status": "success",
            "redirect": "yes",
            "redirect_url": "/"
        })
    else:
        return JsonResponse({
            "message": "GET method not allowed"
        }, status=405)
    


@login_required(login_url="/users/login")
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_items_list = []
    subtotal = 0

    for cart_item in cart_items:
        item_price = cart_item.item.offer_price if cart_item.item.offer_price else cart_item.item.price
        item_subtotal = cart_item.quantity * item_price
        cart_items_list.append({
            'cart_item': cart_item,
            'image_url': cart_item.item.image.url,
            'product_name': cart_item.item.name,
            'price': item_price,
            'quantity': cart_item.quantity,
            'subtotal': item_subtotal,
        })
        subtotal += item_subtotal

    context = {
        "cart_items": cart_items_list,
        "subtotal": subtotal,
        "tax": 35,  # Assuming tax is a fixed value for simplicity
        "total": subtotal + 35,
    }
    
    return render(request, "cart.html", context=context)

@login_required(login_url="furniture:remove_product")
@csrf_exempt
@login_required(login_url="/users/login")
def remove_product(request, pk):
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, id=pk)
        cart_item.delete()
        return JsonResponse({'status': 'success', 'message': 'Item removed successfully!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


def about(request):
    return render(request,"about.html")





@csrf_exempt
def send_order_email(request):
    email_subject = 'New Order Received'
    email_message = 'A new order has been received. Please check the admin panel for details.'
    recipient_email = 'ijazijuz66@gmail.com'  # Replace with the recipient email address
    from_email = 'ijastklm786@gmail.com'  # Replace with the sender email address
    
    # Send email to the specified email address
    send_mail(
        subject=email_subject,
        message=email_message,
        from_email=from_email,
        recipient_list=[recipient_email]
    )
    return HttpResponse('Order confirmation email sent to admin.')


