from django.conf import settings
from django.db import models
from django.db.models import Count, Q


class BookedManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                need_return=Count("loan", filter=Q(loan__return_date__isnull=True))
            )
        )


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    page_count = models.PositiveIntegerField()
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    booked_objects = BookedManager()

    def __str__(self):
        return f"{self.title} by {self.author}"


class LibraryManager(models.Manager):
    def who_loan(self, book: Book):
        return self.filter(return_date__isnull=True, book=book)


class Loan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    objects = LibraryManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["book", "return_date"],
                name="prohibition of creation of double loan",
            )
        ]

    def __str__(self):
        return f"{self.book} borrowed by {self.user}"
