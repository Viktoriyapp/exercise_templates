from datetime import date
from typing import Any

from django import forms

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

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all()


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