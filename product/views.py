from django.db.models import Count
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from polls.views import most_visited
from Site_settings.models import BannerSite
from .models import Product, ProductCategory, ProductBrands, ProductVisit, Size, Gallery, ProductComment
from polls.views import grouped_list


# Create your views here.


class ProductListView(ListView):
    model = Product
    products = Product.objects.all().order_by('-price')[:5]
    template_name = 'product/product_list.html'
    paginate_by = 6


    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data()
        query = Product.objects.all()
        products = query.order_by('-price').first()
        db_max_price = products.price if products is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = BannerSite.objects.filter(is_active=True, position=BannerSite.BannerSitePosition.product_list)
        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            query = query.filter(price__gte=start_price)

        if end_price is not None:
            query = query.filter(price__lte=end_price)

        if brand_name is not None:
            query = query.filter(brand__url_title=brand_name)

        if category_name is not None:
            query = query.filter(category__url_title=category_name)
        return query


class ProductDetailView(DetailView):
    template_name = 'product/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        request = self.request.session.get('product_favorite')
        context['is_favorite'] = request == str(loaded_product.id)
        context['banners'] = BannerSite.objects.filter(is_active=True,
                                                       position=BannerSite.BannerSitePosition.product_detail)
        ip_address = most_visited(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user

        has_been_visited = ProductVisit.objects.filter(ip_address=ip_address, product=loaded_product).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip_address=ip_address, user_id=user_id, product=loaded_product)
            new_visit.save()
        context['size'] = Size.objects.filter(product=loaded_product)
        gallery = list(Gallery.objects.filter(is_active=True, product=loaded_product).all())
        gallery.insert(0, loaded_product)
        context['gallery'] = grouped_list(gallery, 3)
        related_products = list(Product.objects.filter(is_active=True, category__product=loaded_product,
                                                       category__parent__product=loaded_product).exclude(
                                                                                        pk=loaded_product.id).all())
        context['related_products'] = grouped_list(related_products, 3)
        context['comments'] = (
            ProductComment.objects.filter(product_id=loaded_product, parent=None)
            .order_by('-date_send'))

        context['comments_count'] = ProductComment.objects.filter(product_id=loaded_product).count()
        return context


class ProductAddFavoriteView(View):
    def post(self, request):
        product_id = request.POST['productid']
        product = Product.objects.get(pk=product_id)
        request.session['product_favorite'] = product_id
        return redirect(product.get_absolute_url())


def product_detail(request, slug):
    products = get_object_or_404(Product, slug=slug)
    return render(request, 'product/product_detail.html', {
        'products': products
    })


def product_category_components(request):
    category = ProductCategory.objects.prefetch_related('productcategory_set').filter(is_active=True, is_deleted=False,
                                                                                      parent=None)
    context = {
        'categories': category,
    }
    return render(request, 'product/components/product_components.html', context)


def product_brands_components(request):
    brands = ProductBrands.objects.annotate(product_count=Count('product')).filter(is_active=True, is_deleted=False)
    context = {
        'brands': brands
    }
    return render(request, 'product/components/product_brands_components.html', context)


def add_product_comment(request):
    if request.user.is_authenticated:
        product_comment = request.GET.get('product_comment')
        product_id = request.GET.get('product_id')
        parent_id = request.GET.get('parent_id')
        comment = ProductComment(product_id=product_id, text=product_comment, parent_id=parent_id,
                                 user_id=request.user.id)
        comment.save()
        context = {
            'comments': ProductComment.objects.filter(product_id=product_id, parent=None).order_by('-date_send'),
            'comments_count': ProductComment.objects.filter(product_id=product_id).count()
        }
        return render(request, 'product/components/product-comment.html', context)
    return HttpResponse(status=404)
