from datetime import date
from typing import Any

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError

from books.models import Book, Tag
from common.mixins import DisableFormFieldsMixin


# class BookFormBasic(forms.Form):
#     title = forms.CharField(
#         max_length=100,
#         widget=forms.TextInput(attrs={'placeholder': 'e.g. Done'}) #the way we visualize the field
#     ) # label shows by default as the name of the field
#
#     price = forms.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         min_value=0,
#         widget=forms.NumberInput(attrs={'step': '0.1'}),
#         label='Price (USD)',
#     )
#
#     isbn = forms.CharField(max_length=12, min_length=10,)
#
#     genre = forms.ChoiceField(
#         choices=Book.GenreChoices.choices,
#         #widget=forms.RadioSelect # changes the choice select with radio choices
#     )
#
#     publishing_date = forms.DateField(
#         initial=date.today() # loads with this initial value inserted
#     )
#
#     description = forms.CharField(
#         widget=forms.Textarea()
#     )
#
#     image_url = forms.URLField()
#
#     publisher = forms.CharField(max_length=100)


class BookFormBasic(forms.ModelForm):
    tags = forms.CheckboxSelectMultiple()

    field_order = [
        'title',
        'pages',
        'price',
    ]

    class Meta:
        exclude = ['slug',]
        model = Book

        error_messages = {
            'title': {
                'max_length': 'Title is way too long.',
                'required': 'Please enter the title.',
            },
        }

    #For 1 field
    def clean_isbn(self) -> None: # we dont need value here next to the self, we take the needed value like this
        #Validators start before the clean method, bcs validators are for logical validations on the fields for users
        #Clean methods are for business logic validations
        if self.cleaned_data['isbn'].startswith('978'):
            raise ValidationError('ISBN cannot start with 978')

    #For more fields
    def clean(self) -> dict:
        cleaned = super().clean()

        genre = cleaned.get('genre')
        pages = cleaned.get('pages')

        if pages < 10 and genre == Book.GenreChoices.FICTION:
            raise ValidationError(f'Book of type {Book.GenreChoices.FICTION} cannot be less than 10 pages')
        return cleaned

    def save(self, commit = True):
        if self.publisher:
            self.publisher = self.publisher.capitalize()

        if commit:
            self.instance.save()
        return self.instance

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all()
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))


class BookCreateForm(BookFormBasic):
    class Meta(BookFormBasic.Meta):
        help_texts = {
            'isbn': 'International Standard Book Number',
        }


class BookEditForm(BookFormBasic):
    pass


class BookDeleteForm(DisableFormFieldsMixin, BookFormBasic):
    class Meta(BookFormBasic.Meta):
    #     widgets = {
    #         'title': forms.TextInput(attrs={'disabled': True}),
    #     }
        labels = {
            'title': 'Book title',
        }


class BookSearchForm(forms.Form): # forms.Form because it is not connected to a model
    query = forms.CharField(max_length=100, label='', required=False)