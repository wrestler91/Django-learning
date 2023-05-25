from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .form import *
from django.views.generic import ListView, DetailView, CreateView
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.views.generic.edit import FormView
# Create your views here.

class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        cont = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(cont.items()) + list(c_def.items()))
        return context
    
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['cat_selected'] = 0
    #     return context
    
    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')


class WomenCategory(DataMixin, ListView):
    model = Category
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        cont = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name), cat_selected=c.pk)
        context = dict(list(cont.items()) + list(c_def.items()))
        return context
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Категория - ' + str(context['posts'][0].cat)
    #     context['cat_selected'] = context['posts'][0].cat_id
    #     return context
    
    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')
   

# def show_category(request, cat_slug):
#     try:
#         cat = Category.objects.get(slug=cat_slug)
#     except(Exception):
#         raise Http404
#     posts = Women.objects.filter(cat_id=cat.pk)

#     # if len(posts) == 0:
#     #     raise Http404()
#     cont = {
#         'posts': posts, 
#         'title': 'Рубрики',
#         'cat_selected': cat.pk,
#         }
#     return render(request, 'women/index.html', context=cont)
 
 
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    # login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, **kwargs) -> Dict:
        cont = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        context = dict(list(cont.items()) + list(c_def.items()))
        return context
    

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Добавление статьи'
    #     return context



# def add_page(request):
#     '''
#     здесь вначале проверяем, если пришел POST-запрос, значит, пользователем были отправлены данные 
#     (мы будем передавать их именно POST-запросом). В этом случае наполняем форму принятыми значениями из объекта request.POST 
#     и, затем, делаем проверку на корректность заполнения полей (метод is_valid). Если проверка прошла, то в консоли отобразим 
#     словарь form.cleaned_data полученных данных от пользователя. Если же проверка на пройдет, 
#     то пользователь увидит сообщения об ошибках. Ну, а если форма показывается первый раз (идем по else), то она формируется 
#     без параметров и отображается с пустыми полями. 
#     После проверки валидности ввода используем ORM Django для формирования новой записи в таблице women 
#     и передаем методу create распакованный словарь полученных данных. Так как метод create может генерировать исключения, 
#     то помещаем его вызов в блок try и при успешном выполнении, осуществляется перенаправление на главную страницу. 
#     Если же возникли какие-либо ошибки, то попадаем в блок except и формируем общую ошибку для ее отображения в форме.
#     '''
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
        
#         if form.is_valid():
#             if form.is_valid():
#                 # try:
#                 #     # Women.objects.create(**form.cleaned_data)
#                 form.save()
#                 return redirect('home')
#                 # except:
#                 #     form.add_error(None, 'Ошибка добавления поста')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'title': 'Добавление статьи', 'form': form,} )

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        cont = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=cont['post'])
        return dict(list(cont.items()) + list(c_def.items()))
    

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
 
#     context = {
#         'post': post,
#         'title': post.title,
#         # 'cat_selected': post.cat_id,
#     }
 
#     return render(request, 'women/post.html', context=context)


def about(request):
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)
 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'women/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})

    # return render(request, 'women/about.html', {'title': 'О сайте',})


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    # login_url = reverse_lazy('home')
    success_url = reverse_lazy('home')


    def get_context_data(self, **kwargs) -> Dict:
        cont = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        context = dict(list(cont.items()) + list(c_def.items()))
        return context
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        print(form.cleaned_data)
        return redirect('home')

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')
 
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'
 
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_success_url(self):
        return reverse_lazy('home')
    
def logout_user(request):
    logout(request)
    return redirect('login')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
