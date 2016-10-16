from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='Nome Completo', max_length=150, required=True)
    email = forms.EmailField(label='Email', required=True)
    subject = forms.CharField(label='Assunto', max_length=100, required=True)
    message = forms.CharField(label='Mensagem', widget=forms.Textarea, required=True)