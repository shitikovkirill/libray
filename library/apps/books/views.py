from apps.books.models import Book, Loan
from apps.books.serializers import BookSerializer, LoanSerializer
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.booked_objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_permissions(self):
        if self.action in ["list"]:
            permission_classes = [permissions.AllowAny]
            return [permission() for permission in permission_classes]
        return super().get_permissions()
    
    def get_serialilizer_class(self):
        breakpoint()
        if self.action in ["borrow", "return_book"]:
            return None
        return super().get_serializer_class()

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def borrow(self, request, pk=None):
        book = self.get_object()
        if book.need_return:
            return Response(
                {"error": "Book is not available"}, status=status.HTTP_400_BAD_REQUEST
            )

        loan = Loan.objects.create(user=request.user, book=book)
        book.save()

        return Response(LoanSerializer(loan).data)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def return_book(self, request, pk=None):
        book = self.get_object()

        try:
            loan = Loan.objects.who_loan(book).get()
        except Loan.DoesNotExist:
            return Response(
                {"error": "Active loan not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.user != loan.user:
            return Response(
                {
                    "error": "You cannot return this book. The book is registered to another user."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        loan.return_date = timezone.now()
        loan.save()

        return Response(LoanSerializer(loan).data)
