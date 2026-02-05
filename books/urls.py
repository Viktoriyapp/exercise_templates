from django.urls import path, include

import books
from books.views import landing_page, books_list, book_detail, book_create

app_name = 'books'

books_patterns = [
    path('', books_list, name='list'),
    path('<slug:slug>/', book_detail, name='details'),
]

urlpatterns = [
    path('', landing_page, name='home'),
    path('create/', book_create, name='create'),
    path('books/', include(books_patterns)),

]
