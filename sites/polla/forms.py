from django import forms
from django.forms import ModelForm, ValidationError
from .models import Author, Book, Publisher


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, label='subject info:', initial="hello")
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'title', 'birth_date')

    def clean_name(self):
        name = self.cleaned_date['name']
        if len(name) < 30:
            raise ValidationError("Length must more than 30")
        return name

    def clean(self):
        cleaned_data = super(AuthorForm, self).clean()
        name = cleaned_data.get('name', '')
        title = cleaned_data.get('title')
        if len(name) < 40 and title == 'MR':
            raise ValidationError('xxx')


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'authors']


class PublisherForm(ModelForm):
    class Meta:
        model = Publisher
        fields = '__all__'
