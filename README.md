# Personal Expense Tracker

A beginner-friendly Python mini project made using **Tkinter**, **lists**, **dictionaries**, and **file handling**.

## Features
- Add an expense with date, category, amount, and description
- View saved expenses in a table
- Delete a selected expense
- Calculate the total expenses
- Display category-wise expense summary
- Store records in a local `expenses.json` file
- Validate date and amount inputs

## Technologies and Python Concepts
- **Tkinter:** GUI window, labels, entry fields, buttons, and table
- **Lists:** Store multiple expense records
- **Dictionaries:** Store each expense as key-value pairs
- **File Handling:** Read and write expense data
- **JSON:** Keep records in a readable file format
- **Functions and Classes:** Organize the application code
- **Exception Handling:** Handle invalid input and file errors

## Requirements
- Python 3
- Tkinter (included with many Python installations)

## How to Run
1. Download or extract the project folder.
2. Open a terminal in the project folder.
3. Run:

   ```bash
   python expense_tracker.py
   ```

   On some systems, use:

   ```bash
   python3 expense_tracker.py
   ```

4. Add expenses using the form. Records are saved automatically in `expenses.json`.

## Project Structure
```text
Personal_Expense_Tracker/
├── expense_tracker.py
├── README.md
└── expenses.json
```

The `expenses.json` file is created automatically after the first expense is added.

## Sample Expense Record
```json
{
    "date": "2026-10-24",
    "category": "Food",
    "amount": 250.0,
    "description": "Lunch"
}
```

## Conclusion
The Personal Expense Tracker provides a simple way to record and review daily expenses. It demonstrates how core Python concepts can be combined with a graphical user interface and persistent file storage.
