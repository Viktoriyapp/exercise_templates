from django.db.models import Avg
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from books.forms import BookFormBasic
from books.models import Book


# Create your views here.

def landing_page(request: HttpRequest) -> HttpResponse:
    total_books = Book.objects.all().count()
    latest_book = Book.objects.order_by('-publishing_date').first()

    context = {
        'total_books': total_books,
        'latest_book': latest_book,
        'page_title': 'Home',
    }

    return render(request, 'books/landing_page.html', context)

def books_list(request: HttpRequest) -> HttpResponse:
    list_books = Book.objects.annotate(avg_rating=Avg('reviews__rating')
        ).order_by('title')

    context = {
        'books': list_books,
        'page_title': 'Dashboard',
    }
    return render(request, 'books/list.html', context)

def book_detail(request: HttpRequest, slug: str) -> HttpResponse:
    book = get_object_or_404(
        Book.objects.annotate(avg_rating=Avg('reviews__rating')),
        slug=slug,
    )

    context = {
        'book': book,
        'page_title': f'{book.title} details',
    }

    return render(request, 'books/detail.html', context)

def book_create(request: HttpRequest) -> HttpResponse:
    form = BookFormBasic(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # Book.objects.create( # this method for forms.Form
            #     **form.cleaned_data, # unpack and fill the form fields from the cleaned data
            # )
            form.save() # this method for forms.ModelForm; we dont need to create an instance

            return redirect('books:home')

    context = {
        'form': form,
    }
    return render(request, 'books/create.html', context)