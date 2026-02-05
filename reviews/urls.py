from django.urls import path, include

from reviews.views import recent_reviews, review_details, review_create, review_delete, review_edit

app_name = 'reviews'

reviews_patterns = [
    path('recent/', recent_reviews, name='recent'),
    path('<int:pk>/', review_details, name='details'),
    path('', recent_reviews, name='list'),
    path('create/', review_create, name='create'),
    path('<int:pk>/', include([
        path('', review_details, name='details'),
        path('edit/', review_edit, name='edit'),
        path('delete/', review_delete, name='delete'),
    ]))
]

urlpatterns = [
    path('', include(reviews_patterns)),
]