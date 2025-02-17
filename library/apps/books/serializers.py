from rest_framework import serializers

from .models import Book, Loan


class BookSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()

    def get_is_available(self, obj: Book):
        need_return = getattr(obj, "need_return") or 0
        return not bool(need_return)

    class Meta:
        model = Book
        fields = "__all__"


class LoanSerializer(serializers.ModelSerializer):
    is_returned = serializers.SerializerMethodField()

    def get_is_returned(self, obj: Loan):
        return bool(obj.return_date)

    class Meta:
        model = Loan
        fields = "__all__"
        read_only_fields = ("user", "borrowed_date", "is_returned")
