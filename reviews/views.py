from django.forms import modelformset_factory
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from books.models import Book
from reviews.forms import ReviewCreateForm, ReviewEditForm, ReviewDeleteForm
from reviews.models import Review


# Create your views here.

def recent_reviews(request: HttpRequest) -> HttpResponse:
    DEFAULT_REVIEWS_COUNT = 5
    reviews_count = int(request.GET.get('count', DEFAULT_REVIEWS_COUNT))
    # from get request take query parameter(?count=5) else default

    reviews = Review.objects.select_related('book')[:reviews_count]

    context = {
        'reviews': reviews,
        'page_title': 'Recent Reviews',
    }

    return render(request, 'reviews/list.html', context)

def review_details(request: HttpRequest, pk: int) -> HttpResponse:
    review = get_object_or_404(
        Review.objects.select_related('book'),
        pk=pk)

    context = {
        'review': review,
        'page_title': f'{review.author}\'s review on {review.book.title}',
    }
    return render(request, 'reviews/detail.html', context)

def review_create(request: HttpRequest) -> HttpResponse:
    form = ReviewCreateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('reviews:list')

    context = {
        'form': form,
    }

    return render(request, 'reviews/create.html', context)

def review_bulk_update(request: HttpRequest, book_slug: str) -> HttpResponse:
    book = get_object_or_404(Book, slug=book_slug) #We take our book
    ReviewFormSet = modelformset_factory(
        Review,
        form=ReviewEditForm, # This is our form
        can_delete=True, # The form can delete records/gives us a delete check
        extra=1, # 1 additional empty form
    )
    formset = ReviewFormSet(
        request.POST or None,
        queryset=Review.objects.filter(book=book), #the queryset that it should fill with
    )

    if request.method == 'POST' and formset.is_valid():
        instances = formset.save(commit=False) # all objects / queryset of all objects of the forms
        for ins in instances:
            ins.book = book
            ins.save()
        for ins in formset.deleted_objects:
            ins.delete()

        return redirect('reviews:list')

    context = {
        'book': book,
        'formset': formset,
    }

    return render(request, 'reviews/formset_edit.html', context)


def review_edit(request: HttpRequest, pk: int) -> HttpResponse:
    review = get_object_or_404(Review, pk=pk)
    form = ReviewEditForm(request.POST or None, instance=review)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('reviews:list')

    context = {
        'form': form,
    }
    return render(request, 'reviews/edit.html', context)

def review_delete(request: HttpRequest, pk: int) -> HttpResponse:
    review = get_object_or_404(Review, pk=pk)
    form = ReviewDeleteForm(request.POST or None, instance=review)

    if request.method == 'POST' and form.is_valid():
        review.delete()
        return redirect('reviews:list')

    context = {
        'form': form,
    }
    return render(request, 'reviews/delete.html', context)