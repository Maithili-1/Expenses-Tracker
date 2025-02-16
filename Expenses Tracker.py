#!/usr/bin/env python
# coding: utf-8

# In[18]:


import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from datetime import datetime

# Data file to store expense data
EXPENSE_FILE = 'expenses.csv'

# Load expenses from CSV file
def load_expenses():
    expenses = {}
    try:
        with open(EXPENSE_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                date = row['date']
                if date not in expenses:
                    expenses[date] = []
                expenses[date].append({
                    'amount': float(row['amount']),
                    'description': row['description'],
                    'category': row['category'],
                    'date': date
                })
    except FileNotFoundError:
        pass
    return expenses

# Save expenses to CSV file
def save_expenses(expenses):
    with open(EXPENSE_FILE, mode='w', newline='') as file:
        fieldnames = ['date', 'amount', 'description', 'category']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for date, entries in expenses.items():
            for entry in entries:
                writer.writerow(entry)

# Add an expense entry
def add_expense():
    try:
        amount = float(entry_amount.get())
        description = entry_description.get()
        category = combo_category.get()
        date = cal.get_date()

        if amount <= 0:
            raise ValueError("Amount should be greater than zero")

        expense = {
            'amount': amount,
            'description': description,
            'category': category,
            'date': date
        }

        expenses = load_expenses()

        if date not in expenses:
            expenses[date] = []
        expenses[date].append(expense)

        save_expenses(expenses)

        messagebox.showinfo("Success", "Expense added successfully!")
        clear_fields()
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))

# View monthly summary
def view_monthly_summary():
    expenses = load_expenses()
    monthly_expenses = {}

    for date, entries in expenses.items():
        month = date[:7]
        if month not in monthly_expenses:
            monthly_expenses[month] = 0
        for entry in entries:
            monthly_expenses[month] += entry['amount']

    months = list(monthly_expenses.keys())
    amounts = list(monthly_expenses.values())

    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 4))  # Adjusted size of the chart
    ax.bar(months, amounts)
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Expense')
    ax.set_title('Monthly Expenses Summary')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Clear previous chart if any
    for widget in chart_frame.winfo_children():
        widget.destroy()

    # Display the chart in the UI
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# View category-wise summary
def view_category_summary():
    expenses = load_expenses()
    category_expenses = {}

    for date, entries in expenses.items():
        for entry in entries:
            category = entry['category']
            if category not in category_expenses:
                category_expenses[category] = 0
            category_expenses[category] += entry['amount']

    categories = list(category_expenses.keys())
    amounts = list(category_expenses.values())

    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 4))  # Adjusted size of the chart
    ax.bar(categories, amounts)
    ax.set_xlabel('Category')
    ax.set_ylabel('Total Expense')
    ax.set_title('Category-wise Expenses Summary')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Clear previous chart if any
    for widget in chart_frame.winfo_children():
        widget.destroy()

    # Display the chart in the UI
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Clear input fields
def clear_fields():
    entry_amount.delete(0, tk.END)
    entry_description.delete(0, tk.END)

# Set up the main window
window = tk.Tk()
window.title("Expense Tracker")

# Set window size and position (increased height for better display)
window.geometry("1000x600")  # Increased size for a bigger window
window.resizable(True, True)

# Create a PanedWindow widget to divide the screen into two sections
paned_window = tk.PanedWindow(window, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=True)

# Frame for the entry fields (left side)
frame_left = tk.Frame(paned_window, width=500, height=600)
frame_left.pack_propagate(False)  # Prevent the frame from shrinking to its content
paned_window.add(frame_left)

# Frame for the chart (right side)
chart_frame = tk.Frame(paned_window, width=500, height=600)
chart_frame.pack_propagate(False)  # Prevent the frame from shrinking to its content
paned_window.add(chart_frame)

# Amount Input
tk.Label(frame_left, text="Amount:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
entry_amount = tk.Entry(frame_left, font=("Arial", 12))
entry_amount.grid(row=0, column=1, padx=10, pady=10)

# Description Input
tk.Label(frame_left, text="Description:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
entry_description = tk.Entry(frame_left, font=("Arial", 12))
entry_description.grid(row=1, column=1, padx=10, pady=10)

# Category Dropdown
tk.Label(frame_left, text="Category:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
combo_category = tk.StringVar(window)
combo_category.set("Food")  # default category
category_options = ["Food", "Transportation", "Entertainment", "Bills", "Others"]
category_menu = tk.OptionMenu(frame_left, combo_category, *category_options)
category_menu.config(font=("Arial", 12))
category_menu.grid(row=2, column=1, padx=10, pady=10)

# Calendar for date selection
tk.Label(frame_left, text="Select Date:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10)
cal = Calendar(frame_left, font=("Arial", 12), selectmode='day', date_pattern='yyyy-mm-dd')
cal.grid(row=3, column=1, padx=10, pady=10)

# Add Expense Button
btn_add_expense = tk.Button(frame_left, text="Add Expense", font=("Arial", 12), command=add_expense)
btn_add_expense.grid(row=4, column=0, columnspan=2, pady=20)

# View Monthly Summary Button
btn_monthly_summary = tk.Button(frame_left, text="View Monthly Summary", font=("Arial", 12), command=view_monthly_summary)
btn_monthly_summary.grid(row=5, column=0, columnspan=2, pady=10)

# View Category Summary Button
btn_category_summary = tk.Button(frame_left, text="View Category Summary", font=("Arial", 12), command=view_category_summary)
btn_category_summary.grid(row=6, column=0, columnspan=2, pady=10)

# Start the application
window.mainloop()


# In[ ]:




