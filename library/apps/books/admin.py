from django.contrib import admin

from .models import Book, Loan


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "isbn",
    )
    search_fields = ("title", "author", "isbn")
    # list_filter = ('is_available',)


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "user",
        "borrowed_date",
    )
    # list_filter = ('is_returned',)
    search_fields = ("book__title", "user__username")
