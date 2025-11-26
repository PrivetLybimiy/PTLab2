from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView

from .models import Product, Purchase
from .services import price_with_birthday_discount


def index(request):
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['person', 'birthday', 'address']
    template_name = 'shop/purchase_form.html'

    def get_product(self):
        return get_object_or_404(Product, id=self.kwargs['product_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_product()
        context['product'] = product
        context['price'] = product.price  
        return context

    def form_valid(self, form):
        form.instance.product = self.get_product()
        self.object = form.save()

        price = price_with_birthday_discount(self.object.birthday, self.object.product.price)
        discount_status = price != self.object.product.price

        return render(self.request, 'shop/purchase_success.html', {
            'person': self.object.person,
            'price': price,
            'discount_status': discount_status,
        })
