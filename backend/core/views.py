from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import ContactForm
from .utils import _send_mail


class HomeView(View):
    form = ContactForm
    template_name = 'templates/index.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            _send_mail(
                subject=form.cleaned_data['subject'],
                from_=settings.DEFAULT_FROM_EMAIL,
                to=form.cleaned_data['email'],
                template_name='contact_email.txt',
                context={'contact': form.cleaned_data}
            )

            messages.success(request, 'A mensagem foi enviada com sucesso! Muito obrigado.')
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form})