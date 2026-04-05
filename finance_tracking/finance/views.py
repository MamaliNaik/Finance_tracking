from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from .models import Transaction
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsViewer
from .serializers import TransactionSerializer
from .permissions import IsViewer
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.response import Response


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(category__icontains=search)

        return queryset

    def get_permissions(self):
        permission_classes = [IsAuthenticated]  # ✅ default

        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsViewer]

        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    # ✅ CREATE
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "message": "Transaction created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ✅ READ (LIST)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "count": len(serializer.data),
            "data": serializer.data
        })

    # ✅ READ (SINGLE)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # ✅ UPDATE
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
            "message": "Transaction updated successfully",
            "data": serializer.data
        })
        return Response(serializer.errors, status=400)

    # ✅ DELETE
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "message": "Transaction deleted successfully"
        }, status=204)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsViewer])
def summary(request):
    user = request.user

    # ✅ Total Income
    total_income = Transaction.objects.filter(
        user=user, type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # ✅ Total Expense
    total_expense = Transaction.objects.filter(
        user=user, type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # ✅ Balance
    balance = total_income - total_expense

    # ✅ Category-wise Breakdown
    category_data = Transaction.objects.filter(user=user) \
        .values('category') \
        .annotate(total=Sum('amount'))

    # ✅ Monthly Totals
    monthly_data = Transaction.objects.filter(user=user) \
        .annotate(month=TruncMonth('date')) \
        .values('month') \
        .annotate(total=Sum('amount')) \
        .order_by('month')

    # ✅ Recent Activity (Last 5)
    recent = Transaction.objects.filter(user=user) \
        .order_by('-date')[:5] \
        .values('amount', 'type', 'category', 'date')

    return Response({
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "category_breakdown": category_data,
        "monthly_totals": monthly_data,
        "recent_activity": recent
    })