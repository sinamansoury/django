import json
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from Ordering.models import Ordering, OrderingItem, OrderingRentItem, OrderingRent
from Rent.models import Rent
from product.models import Product

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "خرید شما"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
CallbackURL = 'http://localhost:8000/order/verify-payment/'  # برای تست به آدرس محلی اشاره می‌کند


@login_required
def send_order_payment(request):
    current_order, created = Ordering.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    if total_price == 0:
        return HttpResponseRedirect(reverse('User-basket'))

    data = {
        "merchant_id": settings.MERCHANT,
        "amount": total_price * 10,  # تبدیل به تومان
        "description": description,
        "phone": phone,
        "callback_url": CallbackURL,
    }
    data = json.dumps(data)
    headers = {'accept': 'application/json', 'content-type': 'application/json'}

    try:
        response = requests.post(url=ZP_API_REQUEST, data=data, headers=headers, timeout=500)

        if response.status_code == 200:
            response_json = response.json()
            if response_json['data']['code'] == 100:
                return JsonResponse({
                    'status': True,
                    'url': ZP_API_STARTPAY + str(response_json['data']['authority']),
                    'authority': response_json['data']['authority']
                })
            else:
                return JsonResponse({'status': False, 'code': str(response_json['errors']['code'])})
        else:
            return JsonResponse({'status': False, 'code': response.status_code, 'message': response.text})

    except requests.exceptions.Timeout:
        return JsonResponse({'status': False, 'code': 'timeout'})
    except requests.exceptions.ConnectionError:
        return JsonResponse({'status': False, 'code': 'connection error'})


@login_required
def verify_payment(request):
    print(request.user.id)
    authority = request.GET.get('Authority')  # دریافت Authority از پارامتر GET
    print(authority)
    data = {
        "merchant_id": merchant_id,
        "amount": amount,
        "authority": authority,
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json'}

    try:
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['data']['code'] == 100:
                return JsonResponse({'status': True, 'RefID': response_json['data']['ref_id']})
            else:

                return JsonResponse({'status': False, 'code': str(response_json['errors']['code'])})
        else:

            return JsonResponse({'status': False, 'code': response.status_code})

    except requests.exceptions.Timeout:

        return JsonResponse({'status': False, 'code': 'timeout'})
    except requests.exceptions.ConnectionError:

        return JsonResponse({'status': False, 'code': 'connection error'})


def add_to_order(request):
    product_id = request.GET.get('product_id')
    count = int(request.GET.get('count'))
    size = request.GET.get('size')
    product = Product.objects.filter(pk=product_id, is_active=True, is_deleted=False).first()
    if count < 1:
        return JsonResponse({
            'status': 'error_min',
            'text': 'تعداد محصول  باید بیشتر از صفر باشد',
            'confirmButtonText': 'باشه',
            'icon': 'error'
        })
    elif count > product.count:
        return JsonResponse({
            'status': 'error_max',
            'text': 'تعداد محصول  بیشتر از موجودی می باشد',
            'confirmButtonText': 'باشه',
            'icon': 'error'
        })
    if size == '':
        return JsonResponse({
            'status': 'error_size',
            'text': 'سایز را انتخاب کنید',
            'confirmButtonText': 'باشه',
            'icon': 'error'
        })
    if request.user.is_authenticated:
        if product is not None:
            current_order, created = Ordering.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_detail = current_order.orderingitem_set.filter(product_id=product_id, size_id=size).first()
            if current_detail is not None:
                current_detail.total_quantity += count
                current_detail.total_price += product.price * count
                current_detail.save()

            else:
                new_item = OrderingItem(product_id=product_id, total_quantity=count,
                                        order_id=current_order.id, size_id=size, total_price=product.price * count)
                new_item.save()
            return JsonResponse({
                'status': 'success',
                'text': 'محصول به سبد خرید اضافه شد',
                'confirmButtonText': 'ادامه خرید',
                'cancelButtonText': 'مشاهده سبد خرید',
                'icon': 'success'
            })
        return JsonResponse({
            'status': 'not_found',
            'text': 'محصول مورد نظر یافت نشد',
            'confirmButtonText': 'باشه',
            'icon': 'error'
        })
    return JsonResponse({
        'status': 'not_authenticated',
        'text': 'برای افزودن به سبد خرید وارد شوید',
        'confirmButtonText': 'باشه',
        'icon': 'error'
    })


def add_to_rent_order(request):
    product_id = request.GET.get('product_id')
    count = int(request.GET.get('count'))
    size = request.GET.get('size')
    day = request.GET.get('day')
    rent = Rent.objects.filter(pk=product_id, is_active=True, is_deleted=False).first()
    if count < 1:
        return JsonResponse({
            'status': 'error_min',
            'text': 'تعداد محصول  باید بیشتر از صفر باشد',
            'confirmButtonText': 'باشه',
            'icon': 'error'
        })
    elif count > rent.count:
        return JsonResponse({
            'status': 'error_max',
            'text': 'تعداد محصول  بیشتر از موجودی می باشد',
            'confirmButtonText': 'باشه',
            'icon': 'error'
        })
    if size == '':
        return JsonResponse({
            'status': 'error_size',
            'text': 'سایز را انتخاب کنید',
            'confirmButtonText': 'باشه',
            'icon': 'error'
        })
    if day == '':
        return JsonResponse({
            'status': 'error_size',
            'text': 'بازه زمانی را انتخاب کنید را انتخاب کنید',
            'confirmButtonText': 'باشه',
            'icon': 'error'
        })
    if request.user.is_authenticated:
        if rent is not None:
            current_order, created = OrderingRent.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_detail = current_order.orderingrentitem_set.filter(product_id=product_id,
                                                                       size_id=size, day=day).first()
            if current_detail is not None:
                current_detail.total_quantity += count
                current_detail.total_price += rent.price * count
                current_detail.save()

            else:
                if day == '1':
                    new_item = OrderingRentItem(product_id=product_id, total_quantity=count,
                                                order_id=current_order.id, size_id=size, total_price=rent.price * count,
                                                day_id=day)
                    new_item.save()
                elif day == '2':
                    new_item = OrderingRentItem(product_id=product_id, total_quantity=count,
                                                order_id=current_order.id, size_id=size, total_price=rent.price * count*5,
                                                day_id=day)
                    new_item.save()
                elif day == '3':
                    new_item = OrderingRentItem(product_id=product_id, total_quantity=count,
                                                order_id=current_order.id, size_id=size,
                                                total_price=rent.price * count * 18,
                                                day_id=day)
                    new_item.save()
                else:
                    new_item = OrderingRentItem(product_id=product_id, total_quantity=count,
                                                order_id=current_order.id, size_id=size,
                                                total_price=rent.price * count * 25,
                                                day_id=day)
                    new_item.save()

            return JsonResponse({
                'status': 'success',
                'text': 'محصول به سبد خرید اضافه شد',
                'confirmButtonText': 'ادامه خرید',
                'cancelButtonText': 'مشاهده سبد خرید',
                'icon': 'success'
            })
        return JsonResponse({
            'status': 'not_found',
            'text': 'محصول مورد نظر یافت نشد',
            'confirmButtonText': 'باشه',
            'icon': 'error'
        })
    return JsonResponse({
        'status': 'not_authenticated',
        'text': 'برای افزودن به سبد خرید وارد شوید',
        'confirmButtonText': 'باشه',
        'icon': 'error'
    })
