import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import json
import os

DATA_FILE = "expenses.json"


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("850x570")
        self.root.minsize(760, 500)

        self.expenses = []
        self.load_expenses()

        self.date_var = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        self.category_var = tk.StringVar(value="Food")
        self.amount_var = tk.StringVar()
        self.description_var = tk.StringVar()

        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        heading = tk.Label(
            self.root,
            text="Personal Expense Tracker",
            font=("Arial", 20, "bold"),
            pady=12
        )
        heading.pack()

        form = ttk.LabelFrame(self.root, text="Add New Expense", padding=12)
        form.pack(fill="x", padx=15, pady=5)

        ttk.Label(form, text="Date (YYYY-MM-DD)").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.date_var, width=18).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Category").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        categories = ["Food", "Travel", "Shopping", "Bills", "Education", "Health", "Other"]
        ttk.Combobox(
            form,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            width=16
        ).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Amount (₹)").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.amount_var, width=18).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Description").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(form, textvariable=self.description_var, width=19).grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(form, text="Add Expense", command=self.add_expense).grid(
            row=0, column=4, rowspan=2, padx=12, pady=5
        )

        table_frame = ttk.LabelFrame(self.root, text="Expense Records", padding=10)
        table_frame.pack(fill="both", expand=True, padx=15, pady=8)

        columns = ("date", "category", "amount", "description")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        self.table.heading("date", text="Date")
        self.table.heading("category", text="Category")
        self.table.heading("amount", text="Amount (₹)")
        self.table.heading("description", text="Description")

        self.table.column("date", width=120, anchor="center")
        self.table.column("category", width=140, anchor="center")
        self.table.column("amount", width=130, anchor="e")
        self.table.column("description", width=350, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        bottom = ttk.Frame(self.root, padding=(15, 5, 15, 12))
        bottom.pack(fill="x")

        self.total_label = ttk.Label(bottom, text="Total Expenses: ₹0.00", font=("Arial", 12, "bold"))
        self.total_label.pack(side="left")

        ttk.Button(bottom, text="Delete Selected", command=self.delete_expense).pack(side="right", padx=5)
        ttk.Button(bottom, text="Category Summary", command=self.show_summary).pack(side="right", padx=5)

    def load_expenses(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    self.expenses = json.load(file)
            except (json.JSONDecodeError, OSError):
                self.expenses = []
        else:
            self.expenses = []

    def save_expenses(self):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.expenses, file, indent=4)

    def add_expense(self):
        expense_date = self.date_var.get().strip()
        category = self.category_var.get().strip()
        description = self.description_var.get().strip()
        amount_text = self.amount_var.get().strip()

        if not expense_date or not category or not amount_text:
            messagebox.showwarning("Missing Information", "Please enter the date, category, and amount.")
            return

        try:
            date.fromisoformat(expense_date)
        except ValueError:
            messagebox.showerror("Invalid Date", "Enter the date in YYYY-MM-DD format.")
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Amount", "Enter an amount greater than zero.")
            return

        expense = {
            "date": expense_date,
            "category": category,
            "amount": amount,
            "description": description
        }

        self.expenses.append(expense)
        self.save_expenses()
        self.refresh_table()

        self.amount_var.set("")
        self.description_var.set("")
        messagebox.showinfo("Expense Added", "Your expense has been saved.")

    def refresh_table(self):
        for item in self.table.get_children():
            self.table.delete(item)

        for index, expense in enumerate(self.expenses):
            self.table.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    expense["date"],
                    expense["category"],
                    f'{expense["amount"]:.2f}',
                    expense["description"]
                )
            )

        total = sum(expense["amount"] for expense in self.expenses)
        self.total_label.config(text=f"Total Expenses: ₹{total:.2f}")

    def delete_expense(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning("No Selection", "Select an expense record to delete.")
            return

        index = int(selected[0])
        del self.expenses[index]
        self.save_expenses()
        self.refresh_table()

    def show_summary(self):
        category_totals = {}

        for expense in self.expenses:
            category = expense["category"]
            category_totals[category] = category_totals.get(category, 0) + expense["amount"]

        if not category_totals:
            messagebox.showinfo("Category Summary", "No expenses have been added yet.")
            return

        summary = "\n".join(
            f"{category}: ₹{amount:.2f}"
            for category, amount in sorted(category_totals.items())
        )
        messagebox.showinfo("Category Summary", summary)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
