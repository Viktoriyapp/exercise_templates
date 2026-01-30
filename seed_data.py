import os
import django
from decimal import Decimal
from datetime import date

# Django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exercise_templates.settings")
django.setup()

from books.models import Book
from reviews.models import Review


def seed_data():
    books = [
        {
            "title": "The Silent Forest",
            "price": Decimal("18.99"),
            "isbn": "978100000001",
            "genre": Book.GenreChoices.FICTION,
            "publishing_date": date(2021, 5, 10),
            "description": "A slow-burning novel about grief, memory, and secrets hidden in a remote forest.",
            "image_url": "https://example.com/images/silent_forest.jpg",
            "pages": 318,
            "publisher": "Green Leaf Press",
            "reviews": [
                ("Anna Collins", "Very atmospheric and emotional.", Decimal("4.40"), False),
                ("Mark Peterson", "A bit slow, but beautifully written.", Decimal("3.90"), False),
                ("Laura Finch", "The final chapters were devastating.", Decimal("4.60"), True),
            ],
        },
        {
            "title": "Science Explained",
            "price": Decimal("31.50"),
            "isbn": "978100000002",
            "genre": Book.GenreChoices.SCIENCE,
            "publishing_date": date(2020, 9, 1),
            "description": "An accessible overview of modern scientific ideas, from physics to biology.",
            "image_url": "https://example.com/images/science_explained.jpg",
            "pages": 412,
            "publisher": "Nova Publishing",
            "reviews": [
                ("Daniel Green", "Very clear explanations.", Decimal("4.80"), False),
                ("Sofia Martin", "Great for non-scientists.", Decimal("4.30"), False),
                ("Ivan Petrov", "Some chapters were quite dense.", Decimal("3.70"), False),
            ],
        },
        {
            "title": "Dragons of the North",
            "price": Decimal("26.00"),
            "isbn": "978100000003",
            "genre": Book.GenreChoices.FANTASY,
            "publishing_date": date(2022, 3, 18),
            "description": "An epic fantasy saga filled with dragons, betrayal, and ancient magic.",
            "image_url": "https://example.com/images/dragons_north.jpg",
            "pages": 540,
            "publisher": "Iron Crown",
            "reviews": [
                ("Peter Black", "Amazing world-building!", Decimal("4.90"), False),
                ("Emily Rose", "Loved the dragons and lore.", Decimal("4.70"), False),
                ("George Knight", "The death of the king shocked me.", Decimal("4.30"), True),
            ],
        },
        {
            "title": "Mystery at River Town",
            "price": Decimal("16.75"),
            "isbn": "978100000004",
            "genre": Book.GenreChoices.MYSTERY,
            "publishing_date": date(2019, 11, 25),
            "description": "A small-town mystery where everyone has something to hide.",
            "image_url": "https://example.com/images/river_town.jpg",
            "pages": 284,
            "publisher": "Shadow Ink",
            "reviews": [
                ("Natalie Fox", "Kept me guessing until the end.", Decimal("4.60"), False),
                ("Tom Harris", "Classic mystery vibes.", Decimal("4.20"), False),
                ("Olga Ivanova", "The reveal was a bit predictable.", Decimal("3.80"), True),
            ],
        },
        {
            "title": "A Brief History of Empires",
            "price": Decimal("34.90"),
            "isbn": "978100000005",
            "genre": Book.GenreChoices.HISTORY,
            "publishing_date": date(2018, 6, 14),
            "description": "A concise but thorough overview of the greatest empires in human history.",
            "image_url": "https://example.com/images/history_empires.jpg",
            "pages": 468,
            "publisher": "Academic World",
            "reviews": [
                ("Dr. Helen Moore", "Well researched and balanced.", Decimal("4.80"), False),
                ("Samuel Lee", "A bit academic, but rewarding.", Decimal("4.10"), False),
                ("Chris Martin", "Great overview, but lacks depth in places.", Decimal("4.00"), False),
            ],
        },
        {
            "title": "Mindset Reset",
            "price": Decimal("21.25"),
            "isbn": "978100000006",
            "genre": Book.GenreChoices.NONFICTION,
            "publishing_date": date(2023, 1, 9),
            "description": "A practical guide to building better habits and mental resilience.",
            "image_url": "https://example.com/images/mindset_reset.jpg",
            "pages": 256,
            "publisher": "Bright Path",
            "reviews": [
                ("Jessica Moore", "Motivating and practical.", Decimal("4.50"), False),
                ("Alex Turner", "Some advice felt repetitive.", Decimal("3.60"), False),
                ("Nina Lopez", "The final chapter really helped me.", Decimal("4.40"), True),
            ],
        },
    ]

    for book_data in books:
        reviews = book_data.pop("reviews")

        book, created = Book.objects.get_or_create(
            title=book_data["title"],
            defaults=book_data,
        )

        for author, body, rating, is_spoiler in reviews:
            Review.objects.get_or_create(
                book=book,
                author=author,
                body=body,
                rating=rating,
                is_spoiler=is_spoiler,
            )


# if __name__ == "__main__":
#     seed_data()
#     print("✅ Database successfully seeded with books and reviews.")
