from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from Account.models import User
from Rent.models import Rent, RentVisit, RentSize, Gallery, RentComment, RentCategory, RentDay
from Site_settings.models import BannerSite
from polls.views import most_visited, grouped_list
from product.models import Product


# Create your views here.
class RentListView(ListView):
    model = Rent
    products = Rent.objects.all().order_by('-price')[:5]
    template_name = 'Rent/rent_list.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(RentListView, self).get_context_data()
        query = Rent.objects.all()
        rents = query.order_by('-price').first()
        db_max_price = rents.price if rents is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = BannerSite.objects.filter(is_active=True,
                                                       position=BannerSite.BannerSitePosition.product_list)
        return context

    def get_queryset(self):
        query = super(RentListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        request = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            query = query.filter(price__gte=start_price)
        if end_price is not None:
            query = query.filter(price__lte=end_price)
        if category_name is not None:
            query = query.filter(category__url_title=category_name)
        return query


class RentDetailView(DetailView):
    template_name = 'Rent/rent_detail.html'
    model = Rent

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        context['banners'] = BannerSite.objects.filter(is_active=True,
                                                       position=BannerSite.BannerSitePosition.product_detail)
        ip_address = most_visited(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user

        has_been_visited = RentVisit.objects.filter(ip_address=ip_address, product=loaded_product).exists()
        if not has_been_visited:
            new_visit = RentVisit(ip_address=ip_address, user_id=user_id, product=loaded_product)
            new_visit.save()
        context['size'] = RentSize.objects.filter(rent=loaded_product)
        context['day'] = RentDay.objects.filter(rent=loaded_product)
        gallery = list(Gallery.objects.filter(is_active=True, product=loaded_product).all())
        gallery.insert(0, loaded_product)
        context['gallery'] = grouped_list(gallery, 3)
        related_products = list(Rent.objects.filter(is_active=True, category__rent=loaded_product,
                                                    category__parent__rent=loaded_product).exclude(
                                                                                        pk=loaded_product.id).all())
        context['related_products'] = grouped_list(related_products, 3)
        context['comments'] = (
            RentComment.objects.filter(product_id=loaded_product, parent=None)
            .order_by('-date_send'))

        context['comments_count'] = RentComment.objects.filter(product_id=loaded_product).count()
        context['authenticated'] = User.objects.filter(is_active=True, id=self.request.user.id).first()
        return context

def rent_detail(request, slug):
    products = get_object_or_404(Rent, slug=slug)
    return render(request, 'Rent/rent_detail.html', {
        'products': products
    })

def rent_category_components(request):
    category = RentCategory.objects.prefetch_related('rentcategory_set').filter(is_active=True, is_deleted=False,
                                                                                parent=None)
    context = {
        'categories': category,
    }
    return render(request, 'Rent/rent_components.html', context)

def add_rent_comment(request):
    if request.user.is_authenticated:
        rent_comment = request.GET.get('rent_comment')
        rent_id = request.GET.get('rent_id')
        parent_id = request.GET.get('parent_id')
        comment = RentComment(product_id=rent_id, text=rent_comment, parent_id=parent_id,
                              user_id=request.user.id)
        comment.save()
        context = {
            'comments': RentComment.objects.filter(product_id=rent_id, parent=None).order_by('-date_send'),
            'comments_count': RentComment.objects.filter(product_id=rent_id).count()
        }
        return render(request, 'Rent/rent-comment.html', context)
    return HttpResponse(status=404)
