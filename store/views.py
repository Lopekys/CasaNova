from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse
from django.shortcuts import (
    render, redirect, get_object_or_404
)
from django.views.decorators.http import require_POST

from .forms import CustomerUpdateForm, UserUpdateForm
from .models import (
    BlogPost,
    ContactMessage,
    Customer,
    Order,
    OrderItem,
    Product,
    Subscribe,
    Testimonial,
)


def home(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'store/index.html', {'testimonials': testimonials})


def about(request):
    return render(request, 'store/about.html')


def blog(request):
    posts = BlogPost.objects.order_by('-date')
    return render(request, 'store/blog.html', {"posts": posts})


def cart(request):
    cart_data = request.session.get('cart', {})
    cart_items = []
    cart_subtotal = 0

    for product_id, item in cart_data.items():
        item_total = item['price'] * item['quantity']
        cart_items.append({
            'id': product_id,
            'image': item['image_url'],
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'total': item_total
        })
        cart_subtotal += item_total

    cart_total = cart_subtotal

    return render(request, 'store/cart.html', {
        "cart_items": cart_items,
        "cart_subtotal": cart_subtotal,
        "cart_total": cart_total
    })


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    quantity = int(request.POST.get('quantity', 1))
    product_id_str = str(product.id)

    if product_id_str in cart:
        cart[product_id_str]['quantity'] += quantity
    else:
        cart[product_id_str] = {
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': quantity,
            'image_url': product.image.url if product.image else '',
        }

    request.session['cart'] = cart
    return redirect('shop')


@require_POST
def cart_remove(request, product_id):
    if 'cart' in request.session:
        cart = request.session['cart']
        product_id_str = str(product_id)

        if product_id_str in cart:
            del cart[product_id_str]

            if not cart:
                del request.session['cart']
            else:
                request.session['cart'] = cart

            request.session.modified = True

    return redirect('cart')


@require_POST
def cart_update(request, product_id):
    product_id_str = str(product_id)
    new_quantity = int(request.POST.get('quantity', 1))

    if 'cart' in request.session:
        cart = request.session['cart']
        if product_id_str in cart:
            cart[product_id_str]['quantity'] = new_quantity
            request.session['cart'] = cart
            request.session.modified = True

    return redirect('cart')


@login_required
def checkout(request):
    cart_data = request.session.get('cart', {})
    cart_items = []
    cart_subtotal = 0

    for product_id, item in cart_data.items():
        item_total = item['price'] * item['quantity']
        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'total': item_total
        })
        cart_subtotal += item_total

    cart_total = cart_subtotal
    user = request.user
    customer = Customer.objects.get(user=user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        c_form = CustomerUpdateForm(request.POST, instance=customer)

        if u_form.is_valid() and c_form.is_valid():
            u_form.save()
            c_form.save()

            order = Order.objects.create(customer=customer)
            for item in cart_items:
                product = Product.objects.get(id=item['id'])
                OrderItem.objects.create(order=order, product=product, quantity=item['quantity'])

            request.session.pop('cart', None)
            messages.success(request, "Order placed successfully!")
            return redirect('thankyou')
    else:
        u_form = UserUpdateForm(instance=user)
        c_form = CustomerUpdateForm(instance=customer)

    return render(request, 'store/checkout.html', {
        "cart_items": cart_items,
        "cart_subtotal": cart_subtotal,
        "cart_total": cart_total,
        "u_form": u_form,
        "c_form": c_form,
    })


def thankyou(request):
    return render(request, 'store/thankyou.html')


def contact(request):
    success = False
    error = None
    if request.method == 'POST':
        fname = request.POST.get('fname', '').strip()
        lname = request.POST.get('lname', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        if not fname or not lname or not email or not message:
            error = "Please fill in all fields."
        else:
            ContactMessage.objects.create(
                first_name=fname,
                last_name=lname,
                email=email,
                message=message
            )
            success = True
    return render(request, 'store/contact.html', {
        'success': success,
        'error': error
    })


def services(request):
    features = [
        ('truck.svg', 'Fast & Free Shipping'),
        ('bag.svg', 'Easy to Shop'),
        ('support.svg', '24/7 Support'),
        ('return.svg', 'Hassle Free Returns'),
        ('truck.svg', 'Fast & Free Shipping'),
        ('bag.svg', 'Easy to Shop'),
        ('support.svg', '24/7 Support'),
        ('return.svg', 'Hassle Free Returns')
    ]
    return render(request, 'store/services.html', {'features': features})


def shop(request):
    products = Product.objects.all()
    return render(request, 'store/shop.html', {'products': products})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            Customer.objects.create(
                user=user,
                country='',
                company_name='',
                address='',
                address2='',
                state_or_country='',
                postal_code='',
                phone=''
            )

            auth_login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'store/register.html', {'form': form})


@login_required
def account_view(request):
    user = request.user
    customer = Customer.objects.get(user=user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        c_form = CustomerUpdateForm(request.POST, instance=customer)

        if u_form.is_valid() and c_form.is_valid():
            u_form.save()
            c_form.save()
            return redirect('account')
    else:
        u_form = UserUpdateForm(instance=user)
        c_form = CustomerUpdateForm(instance=customer)

    orders = Order.objects.filter(customer=customer).order_by('-created_at')

    return render(request, 'store/account.html', {
        'u_form': u_form,
        'p_form': c_form,
        'orders': orders,
    })


def subscribe_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        if not name or not email:
            return JsonResponse({'success': False, 'error': 'Please fill in all fields.'})
        Subscribe.objects.create(name=name, email=email)
        return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})
