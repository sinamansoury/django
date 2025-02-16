from django.db.models import Count, Sum
from django.shortcuts import render
from django.views.generic import TemplateView
from Home_module.models import Sliders
from Site_settings.models import SiteSettings, FooterLinkBox
from polls.views import grouped_list
from product.models import Product,  ProductCategory
from tracking.mixins import LoggingMixins

# Create your views here.


class HomeView(LoggingMixins, TemplateView):
    template_name = 'shared/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sliders: Sliders = Sliders.objects.filter(is_active=True).all()
        context['sliders'] = grouped_list(sliders, 2)
        newest_product = Product.objects.filter(is_active=True, is_deleted=False).order_by('-id')[:12]
        context['newest_product'] = grouped_list(newest_product)
        most_visited = Product.objects.filter(is_active=True, is_deleted=False).annotate(
            visit_count=Count('productvisit')).order_by('-visit_count')[:12]
        context['most_visited'] = grouped_list(most_visited)
        most_bought = (Product.objects.filter(orderingitem__order__is_paid=True, is_active=True, is_deleted=False).
                       annotate(count_of_bought=Sum('orderingitem__total_quantity')).order_by('-count_of_bought'))[:12]
        context['most_bought'] = grouped_list(most_bought)
        categories = ProductCategory.objects.annotate(
            category_count=Count('product')).filter(is_active=True, parent=None, category_count__gt=0)
        products_categories = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products': list(category.product_set.all())[:4]
            }
            products_categories.append(item)
        context['product_categories'] = products_categories
        return context


def site_header_component(request):
    header_component: SiteSettings = SiteSettings.objects.filter(is_main_settings=True).first()
    return render(request, 'shared/site_header_component.html', {
        'site_setting_logo': header_component
    })


def site_footer_component(request):
    footer_component: SiteSettings = SiteSettings.objects.filter(is_main_settings=True).first()
    footer_link_box = FooterLinkBox.objects.all()
    for item in footer_link_box:
        item.footerlink_set
    return render(request, 'shared/site_footer_component.html', {
        'footer_settings': footer_component,
        'footer_link_box': footer_link_box,
    })
