from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .models import Product, Purchase, Discount

# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)

def discount_update(purchase_object):
    discount_row = Discount.objects.get(person=purchase_object.person)
    price = Product.objects.get(id=purchase_object.product.id).price
    total = discount_row.total + price
    discount_value = min(total/10000.0, 25)
    if discount_value <= 25:
        Discount.objects.filter(person=purchase_object.person).update(total=total,discount=discount_value)


def calculateDiscount(purchase_object):
    price = Product.objects.get(id=purchase_object.product.id).price
    discount = Discount.objects.filter(person=purchase_object.person).get().discount
    return HttpResponse(f'Thanks for the purchase, {purchase_object.person}!'
                        f'\n Your discount on this product: {discount}%'
                        f'\n The total cost of the product: {int(price * (1 - (discount / 100.0)))}')

class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def form_valid(self, form):
        self.object = form.save()
        if Discount.objects.filter(person=self.object.person).exists():
            discount_update(self.object)
            return calculateDiscount(self.object)
        else:
            return HttpResponse(f'Thanks for the purchase, {self.object.person}!\nTo accumulate a discount, sign up for the loyalty program!')

class DiscountCreate(CreateView):
    model = Discount
    fields = ['person', 'total', 'discount']

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse(f'You are registered in the loyalty program, {self.object.person}!')