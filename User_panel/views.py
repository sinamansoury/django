from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View, ListView, CreateView
from Account.models import User, AuthUser
from Ordering.models import Ordering, OrderingItem, OrderingRent, OrderingRentItem
from .forms import EditInfoForm, ChangePasswordForm, AuthenticatedForm


# Create your views here.


@method_decorator(login_required, name='dispatch')
class UserPanelView(TemplateView):
    template_name = 'User_panel/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = User.objects.filter(id=self.request.user.id).first()
        return context


@method_decorator(login_required, name='dispatch')
class EditUserInfo(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditInfoForm(instance=current_user)
        context = {
            'form': edit_form,
            'current_user': current_user
        }
        return render(request, 'User_panel/edit-info-page.html', context)

    def post(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditInfoForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save()
        context = {
            'form': edit_form,
            'current_user': current_user
        }
        return render(request, 'User_panel/edit-info-page.html', context)


@method_decorator(login_required, name='dispatch')
class ChangePassword(View):
    def get(self, request: HttpRequest):
        context = {
            'form': ChangePasswordForm()
        }
        return render(request, 'User_panel/change-password.html', context)

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_user = User.objects.filter(id=request.user.id).first()
            if current_user.check_password(form.cleaned_data.get('current_password')):
                current_user.set_password(form.cleaned_data.get('password'))
                current_user.save()
                return render(request, 'User_panel/dashboard.html')
            else:
                form.add_error('current_password', 'رمز عبور فعلی اشتباه است')

        context = {
            'form': form
        }
        return render(request, 'User_panel/change-password.html', context)


@method_decorator(login_required, name='dispatch')
class Authenticated(CreateView):
    model = AuthUser
    form_class = AuthenticatedForm
    template_name = 'User_panel/authenticated.html'
    success_url = 'authenticated'

    def form_valid(self, form):
        form.instance.user_name = self.request.user  # Set user_id to AuthUser instance
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class UserOrder(ListView):
    model = Ordering
    template_name = 'User_panel/user-orders.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user.id, is_paid=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_order = Ordering.objects.filter(user=self.request.user.id, is_paid=True)
        context['orders'] = current_order
        order_price = {}
        for orders in current_order:
            order_items = orders.orderingitem_set.all()
            prices = [item.total_price for item in order_items]
            order_price[orders.id] = prices
        context['order_price'] = order_price
        return context


@method_decorator(login_required, name='dispatch')
class UserRentOrder(ListView):
    model = OrderingRent
    template_name = 'User_panel/user-orders.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user.id, is_paid=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_order = OrderingRent.objects.filter(user=self.request.user.id, is_paid=True)
        context['order'] = current_order
        order_prices = {}
        for order in current_order:
            order_items = order.orderingrentitem_set.all()
            prices = [item.total_price for item in order_items]
            order_prices[order.id] = prices
        context['order_prices'] = order_prices
        return context


@login_required
def user_detail(request: HttpRequest, order_id):
    current_order = Ordering.objects.filter(id=order_id, user_id=request.user.id).first()
    total_prices = []
    for item in current_order.orderingitem_set.all():
        total_prices.append(item.total_price)
    if current_order is None:
        raise Http404('سبد خرید موجود نمیباشد')

    return render(request, 'User_panel/user-order-detail.html', {
        'order': current_order,
        'total_prices': list(total_prices)
    })


@login_required
def user_rent_detail(request: HttpRequest, order_rent_id):
    current_order = OrderingRent.objects.filter(id=order_rent_id, user_id=request.user.id).first()
    total_prices = []
    for item in current_order.orderingrentitem_set.all():
        total_prices.append(item.total_price)
    if current_order is None:
        raise Http404('سبد خرید موجود نمیباشد')

    return render(request, 'User_panel/user-order-rent-detail.html', {
        'order': current_order,
        'total_prices': list(total_prices)
    })


@login_required
def user_basket_panel(request):
    current_order, created = Ordering.objects.get_or_create(is_paid=False, user_id=request.user.id)
    item_prices, total = current_order.calculate_total_price()
    context = {
        'current_order': current_order,
        'item_prices': item_prices,
        'total': total

    }
    return render(request, 'User_panel/user-basket.html', context)


@login_required
def user_rent_basket_panel(request):
    current_order, created = OrderingRent.objects.get_or_create(is_paid=False, user_id=request.user.id)
    item_prices, total = current_order.calculate_total_rent_price()
    context = {
        'cur_order': current_order,
        'item_prices': item_prices,
        'total': total,

    }
    return render(request, 'User_panel/user-basket.html', context)


@login_required
def user_panel_components(request):
    return render(request, 'components/dashboard_components.html')


@login_required
def user_panel_rent_components(request):
    return render(request, 'components/dashboard_rent_components.html')


@login_required
def remove_order_item(request):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'error_detail_id',
        })
    current_order, created = Ordering.objects.get_or_create(is_paid=False, user_id=request.user.id)
    current_detail = current_order.orderingitem_set.filter(id=detail_id).first()
    if current_detail is None:
        return JsonResponse({
            'status': 'not_detail_found',
        })

    total = current_order.calculate_total_price()
    context = {
        'current_order': current_order,
        'total': total

    }
    current_detail.delete()
    data = render_to_string('User_panel/user-basket-content.html', context)
    return JsonResponse({
        'status': 'success',
        'data': data
    })


@login_required
def change_product_number(request):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'error_detail_id_or_state',
        })
    current_detail = OrderingItem.objects.filter(id=detail_id, order__user_id=request.user.id,
                                                 order__is_paid=False).first()

    if current_detail is None:
        return JsonResponse({
            'status': 'not_detail_found',
        })

    if state == 'increase':
        current_detail.total_quantity += 1
        if current_detail.total_quantity <= current_detail.product.count:
            current_detail.save()
        else:
            return JsonResponse({
                'status': 'error_product_number',
                'text': 'تعداد انتخاب شده بیشتر از موجودی است',
                'confirmButtonText': 'باشه',
                'icon': 'error'
            })
    elif state == 'decrease':
        if current_detail.total_quantity == 1:
            current_detail.delete()
            current_order, created = Ordering.objects.get_or_create(is_paid=False, user_id=request.user.id)
            item_prices, total = current_order.calculate_total_price()
            context = {
                'current_order': current_order,
                'item_prices': item_prices,
                'total': total
            }
            data = render_to_string('User_panel/user-basket-content.html', context)
            return JsonResponse({
                'status': 'success',
                'data': data
            })
        else:
            current_detail.total_quantity -= 1
            current_detail.save()
    else:
        return JsonResponse({
            'status': 'error_state',
        })

    current_order, created = Ordering.objects.get_or_create(is_paid=False, user_id=request.user.id)
    item_prices, total = current_order.calculate_total_price()
    current_detail.total_price = item_prices[current_detail.id]
    current_detail.save()
    context = {
        'current_order': current_order,
        'item_prices': item_prices,
        'total': total

    }
    data = render_to_string('User_panel/user-basket-content.html', context)
    return JsonResponse({
        'status': 'success',
        'data': data
    })


@login_required
def remove_rent_order_item(request):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'error_detail_id',
        })
    current_order, created = OrderingRent.objects.get_or_create(is_paid=False, user_id=request.user.id)
    current_detail = current_order.orderingrentitem_set.filter(id=detail_id).first()
    if current_detail is None:
        return JsonResponse({
            'status': 'not_detail_found',
        })

    current_detail.delete()
    item_prices, total = current_order.calculate_total_rent_price()
    context = {
        'cur_order': current_order,
        'item_prices': item_prices,
        'total': total

    }
    data = render_to_string('User_panel/user-basket-rent-content.html', context)
    return JsonResponse({
        'status': 'success',
        'data': data
    })


@login_required
def change_rent_product_number(request):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'error_detail_id_or_state',
        })

    current_detail = OrderingRentItem.objects.filter(id=detail_id, order__user_id=request.user.id,
                                                     order__is_paid=False).first()
    if current_detail is None:
        return JsonResponse({
            'status': 'not_detail_found',
        })

    if state == 'increase':
        current_detail.total_quantity += 1
        if current_detail.total_quantity <= current_detail.product.count:
            current_detail.save()
        else:
            return JsonResponse({
                'status': 'error_product_number',
                'text': 'تعداد انتخاب شده بیشتر از موجودی است',
                'confirmButtonText': 'باشه',
                'icon': 'error'
            })
    elif state == 'decrease':
        if current_detail.total_quantity == 1:
            current_detail.delete()
            # بعد از حذف آیتم نیازی به ادامه اجرای کد نیست
            current_order, created = OrderingRent.objects.get_or_create(is_paid=False, user_id=request.user.id)
            item_prices, total = current_order.calculate_total_rent_price()
            context = {
                'cur_order': current_order,
                'item_prices': item_prices,
                'total': total
            }
            data = render_to_string('User_panel/user-basket-rent-content.html', context)
            return JsonResponse({
                'status': 'success',
                'data': data
            })
        else:
            current_detail.total_quantity -= 1
            current_detail.save()
    else:
        return JsonResponse({
            'status': 'error_state',
        })

    current_order, created = OrderingRent.objects.get_or_create(is_paid=False, user_id=request.user.id)
    item_prices, total = current_order.calculate_total_rent_price()
    current_detail.total_price = item_prices[current_detail.id]
    current_detail.save()
    context = {
        'cur_order': current_order,
        'item_prices': item_prices,
        'total': total
    }
    data = render_to_string('User_panel/user-basket-rent-content.html', context)
    return JsonResponse({
        'status': 'success',
        'data': data
    })


