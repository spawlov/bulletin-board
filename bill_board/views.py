from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin

from .form import AdvertForm, RespForm
from .models import Advert, Resp
from .permissions import AdvertOwnerRequiredMixin


class AdvertView(ListView):
    model = Advert
    ordering = '-pk'
    context_object_name = 'advert'
    template_name = 'advertising.html'
    paginate_by = 10


class AdvertDetail(FormMixin, DetailView):
    model = Advert
    form_class = RespForm
    context_object_name = 'content'
    template_name = 'advertising_detail.html'


class AdvertCreate(LoginRequiredMixin, CreateView):
    model = Advert
    form_class = AdvertForm
    template_name = 'create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = User.objects.get(id=self.request.user.id)
        self.object.save()
        return super().form_valid(form)


class AdvertEdit(AdvertOwnerRequiredMixin, UpdateView):
    model = Advert
    form_class = AdvertForm
    template_name = 'edit.html'


class AdvertDelete(AdvertOwnerRequiredMixin, DeleteView):
    model = Advert
    success_url = reverse_lazy('bill_board:advert')


class RespCreate(LoginRequiredMixin, CreateView):
    model = Resp
    form_class = RespForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = User.objects.get(id=self.request.user.id)
        self.object.post = get_object_or_404(Advert, pk=self.request.POST.get('advertId'))
        self.object.save()
        return super().form_valid(form)


class UserAdvert(ListView):
    template_name = 'advertising.html'
    context_object_name = 'advert'
    # paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)
        queryset = Advert.objects.filter(author=user)
        return queryset


class RespList(ListView):
    context_object_name = 'responses'
    template_name = 'response_list.html'

    def get_queryset(self):
        """Получаем Queryset с возможностью фильтрации по объявлениям"""
        try:
            self.adv = int(self.request.GET.get('adv', 0))
        except ValueError:
            self.adv = 0
        self.user = get_object_or_404(User, id=self.request.user.id)
        queryset = Resp.objects.filter(
            post__in=Advert.objects.filter(author=self.user, pk=self.adv)
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['adverts'] = Advert.objects.filter(author=self.user)
        context['advert_list'] = Advert.objects.filter(author=self.user, pk=self.adv)
        context['adv'] = self.adv
        return context


@login_required
def resp_change_status(request):
    if request.method == 'POST':
        response = Resp.objects.get(pk=request.POST.get('respId'))
        response.status = True
        response.save(update_fields=['status'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_response(request):
    if request.method == 'POST':
        response = Resp.objects.get(pk=request.POST.get('respId'))
        response.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
