from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Transaction


def get_financial_summary(user):
    total_income = Transaction.objects.filter(
        user=user, type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_expense = Transaction.objects.filter(
        user=user, type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    category_data = Transaction.objects.filter(user=user) \
        .values('category') \
        .annotate(total=Sum('amount'))

    monthly_data = Transaction.objects.filter(user=user) \
        .annotate(month=TruncMonth('date')) \
        .values('month') \
        .annotate(total=Sum('amount'))

    recent = Transaction.objects.filter(user=user) \
        .order_by('-date')[:5]

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense,
        "category_breakdown": list(category_data),
        "monthly_totals": list(monthly_data),
        "recent_activity": list(recent.values())
    }