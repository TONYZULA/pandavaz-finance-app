# core/management/commands/import_legacy_data.py
import pandas as pd
from django.core.management.base import BaseCommand
from datetime import datetime
from core.models import Partner, Transaction
import re

class Command(BaseCommand):
    help = 'Imports all legacy data from the PANDAVAZ Cash CSV file.'

    def handle(self, *args, **options):
        Transaction.objects.all().delete()
        self.stdout.write("Wiping old data... Starting fresh import.")

        partner_names = ['Sagar', 'Maulik', 'Tarun', 'Tushar', 'Pravin']
        partners = {name: Partner.objects.get_or_create(name=name)[0] for name in partner_names}

        try:
            df = pd.read_csv('PANDAVAZ Cash - Sheet1.csv', header=None)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("CSV file not found."))
            return

        for index, row in df.iterrows():
            if index == 0: continue

            def get_date_from_string(s):
                if not isinstance(s, str): return None
                match = re.search(r'\((\d{1,2}-\d{1,2}-\d{4})\)', s)
                return datetime.strptime(match.group(1), '%d-%m-%Y').date() if match else None

            # --- Income (Cols 0 & 1) ---
            try:
                amount = float(row[1])
                desc = str(row[0])
                if pd.notna(amount) and pd.notna(desc):
                    Transaction.objects.create(transaction_type='INCOME', date=get_date_from_string(desc), description=desc, amount=amount)
            except (ValueError, TypeError): pass

            # --- Expenses (Cols 2 & 3) ---
            try:
                amount = float(row[3])
                desc = str(row[2])
                if pd.notna(amount) and pd.notna(desc):
                    Transaction.objects.create(transaction_type='EXPENSE', date=get_date_from_string(desc), description=desc, amount=amount)
            except (ValueError, TypeError): pass

            # --- Partner Payouts ---
            payout_cols = {'Sagar': 4, 'Maulik': 6, 'Tarun': 8, 'Tushar': 10, 'Pravin': 12}
            for name, col_idx in payout_cols.items():
                try:
                    amount = float(row[col_idx + 1])
                    desc = str(row[col_idx])
                    if pd.notna(amount) and pd.notna(desc):
                        Transaction.objects.create(
                            transaction_type='PAYOUT', partner=partners[name], date=get_date_from_string(desc), description=f"Payout: {desc}", amount=amount
                        )
                except (ValueError, TypeError): pass

        self.stdout.write(self.style.SUCCESS("Import complete!"))