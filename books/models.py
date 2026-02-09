from django.db import models
from django.utils.text import slugify

from books.validators import range_validator2, RangeValidator
from common.models import TimeStampModel


# Create your models here.

class Book(TimeStampModel):
    class GenreChoices(models.TextChoices):
        FICTION = 'Fiction', 'Fiction'
        NONFICTION = 'Non-Fiction', 'Non-Fiction'
        FANTASY = 'Fantasy', 'Fantasy'
        SCIENCE = 'Science', 'Science'
        HISTORY = 'History', 'History'
        MYSTERY = 'Mystery', 'Mystery'

    title = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            RangeValidator(0, 1000, 'Price should be in the range 0-1000')
            ],
        )
    isbn = models.CharField(max_length=12, unique=True)
    genre = models.CharField(max_length=50, choices=GenreChoices.choices)
    publishing_date = models.DateField()
    description = models.TextField()
    image_url = models.URLField()
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True, #for our slug on save to allow user to not fill
    )
    pages = models.PositiveIntegerField(null=True, blank=True)
    publisher = models.CharField(max_length=100)
    tags = models.ManyToManyField('Tag')

    #logic for slug we do on saving
    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(f'{self.title}-{self.publisher}')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    # def __repr__(self):
    #     return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50)
    books = models.ManyToManyField(Book)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name