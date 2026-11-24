from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .models import Product, Purchase

# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)

def checkout(request):
    if request.method == 'POST':
        person = request.POST.get('person')
        address = request.POST.get('address')
        
        total_price = 0
        different_products_count = 0
        purchases_to_create = []
        
        
        for key, value in request.POST.items():
            if key.startswith('product_'):
                product_id = key.split('_')[1]
                quantity = int(value)
                if quantity > 0:
                    product = Product.objects.get(id=product_id)
                    total_price += product.price * quantity
                    different_products_count += 1 # Считаем, сколько РАЗНЫХ видов товара
                    purchases_to_create.append((product, quantity))
        
        if different_products_count == 0:
            return HttpResponse("Вы не выбрали ни одного товара. <a href='/'>Вернуться</a>")
        
        
        discount_applied = False
        if different_products_count > 1:
            total_price = total_price * 0.9
            discount_applied = True
            
        for product, quantity in purchases_to_create:
            for _ in range(quantity):
                Purchase.objects.create(
                    product=product,
                    person=person,
                    address=address
                )
                
        response = f"Спасибо за покупку, {person}!<br>"
        response += f"Итоговая сумма: {int(total_price)} руб.<br>"
        if discount_applied:
            response += "<b style='color:green;'>Применена скидка 10% за покупку разных видов товаров!</b><br>"
            
        return HttpResponse(response + "<br><a href='/'>Вернуться в магазин</a>")
    
    return HttpResponse("Ошибка: неверный метод запроса.")
    
class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse(f'Спасибо за покупку, {self.object.person}!')

