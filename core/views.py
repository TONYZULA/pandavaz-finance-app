# core/views.py
from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Transaction, Partner # Make sure to import Partner
from .forms import TransactionForm

def dashboard(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    form = TransactionForm()
    transactions = Transaction.objects.order_by('-id')

    # --- Overall Financial Calculations ---
    total_income = transactions.filter(transaction_type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = transactions.filter(transaction_type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0
    total_payouts = transactions.filter(transaction_type='PAYOUT').aggregate(total=Sum('amount'))['total'] or 0
    current_balance = total_income - (total_expenses + total_payouts)

    # --- NEW: Partner-specific Payout Calculations ---
    partners = Partner.objects.all()
    partner_payouts_data = []
    for partner in partners:
        payout_sum = transactions.filter(
            transaction_type='PAYOUT',
            partner=partner
        ).aggregate(total=Sum('amount'))['total'] or 0
        partner_payouts_data.append({'partner': partner, 'total': payout_sum})
    # --- End of New Section ---

    context = {
        'form': form,
        'transactions': transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_payouts': total_payouts,
        'current_balance': current_balance,
        'partner_payouts_data': partner_payouts_data, # Add new data to context
    }
    return render(request, 'core/dashboard.html', context)

# core/views.py
# (keep the existing imports and the dashboard function)

# Add these two new functions at the end of the file
def transaction_log_view(request, transaction_type):
    """Displays a full log for a specific transaction type (INCOME, EXPENSE, or PAYOUT)."""
    transaction_type = transaction_type.upper()
    transactions = Transaction.objects.filter(transaction_type=transaction_type).order_by('id')
    context = {
        'transactions': transactions,
        'log_title': f'{transaction_type.capitalize()} Log'
    }
    return render(request, 'core/transaction_log.html', context)

def partner_log_view(request, partner_id):
    """Displays a full payout log for a specific partner."""
    try:
        partner = Partner.objects.get(id=partner_id)
        payouts = Transaction.objects.filter(
            transaction_type='PAYOUT',
            partner=partner
        ).order_by('id')
        context = {
            'transactions': payouts,
            'log_title': f'Payout Log for {partner.name}'
        }
        return render(request, 'core/transaction_log.html', context)
    except Partner.DoesNotExist:
        return redirect('dashboard') # Redirect home if partner doesn't exist