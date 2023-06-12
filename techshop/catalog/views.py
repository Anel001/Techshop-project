from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Product, Category, Comment, Order, ProductOrder, UserProfile, UserCategory, UserProduct, Producer
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin
from .forms import ComForm, OrderForm, UserForm
from .filters import ProductFilter, ProductFilterset
from cart.forms import CartAddProductForm
from django.utils import timezone
from cart.cart import Cart
from django.views import View
from django.core.mail import send_mail


class MainPageView(ListView):
    model = Product
    template_name = 'default.html'
    context_object_name = 'products'
    queryset = Product.objects.order_by('-rating')

    def get_queryset(self):
        queryset = super(MainPageView, self).get_queryset().order_by('-rating')
        sort = self.request.GET.get('sorting')
        if sort == ('price'):
            return queryset.order_by('price')
        if sort == ('-price'):
            return queryset.order_by('-price')
        else:
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        filterset = ProductFilterset(self.request.GET, queryset=self.get_queryset()).qs
        context['filter'] = ProductFilter(self.request.GET, queryset=filterset)
        context['filterset'] = ProductFilterset(self.request.GET, queryset=self.get_queryset())
        context['product1'] = Product.objects.get(id=1)
        context['product2'] = Product.objects.get(id=2)
        context['product3'] = Product.objects.get(id=3)
        context['brands'] = [Producer.objects.get(id=1), Producer.objects.get(id=4),
                             Producer.objects.get(id=3), Producer.objects.get(id=2)]
        context['topProducts'] = Product.objects.order_by('-rating')[:3]
        return context


class ProductDetail(FormMixin, DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    form_class = ComForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('product', kwargs={'pk': self.get_object().id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        coms = Comment.objects.filter(product=product).count()
        context['truecount'] = coms
        context['cart_product_form'] = CartAddProductForm()
        pas = product.product_filials.all()
        t = 0
        for a in pas:
            t = t + a.amount
        context['amount'] = t
        context['all_rating'] = product.rating
        if self.request.user.is_authenticated:
            if self.request.user.user_comments.exists():
                if self.request.user.user_comments.filter(product=product).exists():
                    context['sended'] = True
                else:
                    context['sended'] = False
            else:
                context['sended'] = False

            context['is_subscribed'] = UserProduct.objects.filter(user=self.request.user,
                                                                  product=self.get_object()).exists()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.product = self.get_object()
        self.object.user = self.request.user
        self.object.rating = self.request.POST['rating']
        self.object.save()
        return super().form_valid(form)


class CommentEditView(LoginRequiredMixin, UpdateView):
    template_name = 'com_edit.html'
    context_object_name = 'comment'
    form_class = ComForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('product', kwargs={'pk': self.get_object().product.id})

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Comment.objects.get(pk=id)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.com_date = timezone.now()
        self.object.rating = self.request.POST['rating']
        self.object.save()
        return super(CommentEditView, self).post(request, **kwargs)


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.first_name = request.POST['first_name']
            order.last_name = request.POST['last_name']
            order.address = request.POST['address']
            order.paymentMethod = request.POST['payment']
            order.user = request.user
            order = form.save()
            for item in cart:
                ProductOrder.objects.create(order=order,
                                            product=item['product'],
                                            price=item['price'],
                                            amount=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'order_created.html',
                          {'order': order})
    else:
        form = OrderForm
    return render(request, 'order_create.html',
                  {'cart': cart, 'form': form})


class OrdersList(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'
    paginate_by = 5


class OrderDetail(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = ProductOrder.objects.filter(order=self.get_object())
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(category=self.get_object())
        context['products'] = products
        context['filterset'] = ProductFilterset(self.request.GET, queryset=products)
        context['categories'] = Category.objects.all()
        if self.request.user.is_authenticated:
            context['is_subscribed'] = UserCategory.objects.filter(user=self.request.user,
                                                                   category=self.get_object()).exists()
        return context


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'my_page.html'


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'edit_account.html'
    success_url = "/my_page"
    form_class = UserForm

    def get_object(self, **kwargs):
        return self.request.user

    def post(self, request, **kwargs):
        self.object = self.get_object()
        if UserProfile.objects.filter(user=self.get_object()).exists():
            profile = UserProfile.objects.get(user=self.get_object())
            profile.address = self.request.POST['address']
            profile.save()
        else:
            UserProfile.objects.create(user=self.get_object(), address="не указано")
        self.object.save()
        return super(ProfileUpdate, self).post(request, **kwargs)


class SupportView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'support.html', {})

    def post(self, request, *args, **kwargs):
        name = request.POST['first_name'],
        email = request.POST['email'],
        text = request.POST['text']

        # отправляем письмо
        send_mail(
            subject=f'!Техническая поддержка ',
            message=f"Запрос от пользователя {name}.\n"
                    f" Электронная почта пользователя для дальнейшей координации: {email} \n"
                    f" Описание проблемы: \n {text}",
            from_email='anel031@yandex.ru',
            recipient_list=['techshopassistant@gmail.com']
        )

        return redirect(f'/my_page')

@login_required()
def subscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    subscriber = UserCategory(user_id=user.id, category_id=category.id)
    subscriber.save()
    return redirect(f'/category/{category.id}')


@login_required()
def unsubscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    subscriber = UserCategory.objects.get(user_id=user.id, category_id=category.id)
    subscriber.delete()
    return redirect(f'/category/{category.id}')


@login_required()
def subscribe_product(request, pk):
    user = request.user
    product = Product.objects.get(id=pk)
    subscriber = UserProduct(user_id=user.id, product_id=product.id)
    subscriber.save()
    return redirect(f'/{product.id}')


@login_required()
def unsubscribe_product(request, pk):
    user = request.user
    product = Product.objects.get(id=pk)
    subscriber = UserProduct.objects.get(user_id=user.id, product_id=product.id)
    subscriber.delete()
    return redirect(f'/{product.id}')


