from datetime import date

from django import forms

from books.models import Book


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
    class Meta:
        exclude = ['slug',]
        model = Book