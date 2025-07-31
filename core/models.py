from django.db import models

# core/models.py
class Partner(models.Model):
    """Represents one of the five partners."""
    name = models.CharField(max_length=100, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    """Represents a single financial transaction."""

    class TransactionType(models.TextChoices):
        INCOME = 'INCOME', 'Income'
        EXPENSE = 'EXPENSE', 'Expense'
        PAYOUT = 'PAYOUT', 'Payout'

    date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=7,
        choices=TransactionType.choices,
    )
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.get_transaction_type_display()} - {self.description} - ₹{self.amount}"