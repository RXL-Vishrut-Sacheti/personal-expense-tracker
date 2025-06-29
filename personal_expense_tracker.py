from datetime import datetime
import csv
import os

global budget
global budget_start_date, budget_end_date
expense = {}

def createMonthlyBudget(amount):
    if amount <= 0:
        print("Budget must be greater than 0. Please enter a valid amount.")
        amount = int(input("Enter your monthly budget again: "))
        createMonthlyBudget(amount)
    else:
        global budget
        budget = amount
        print("Your monthly budget has been set to: $", budget)
        displayMenu()

# Function to add expense
def addExpense():
    global expense
    expense_date = input("Enter the date of the expense (YYYY-MM-DD): ")
    validateDate(expense_date)
    expense['Date'] = expense_date
    expense_category = input("Enter the category of the expense: ")
    validateCategory(expense_category)
    expense['Category'] = expense_category
    expense_amount = float(input("Enter the expense amount:"))
    validateAmount(expense_amount)
    expense['Amount'] = expense_amount
    expense_description = input("Enter a description for the expense: ")
    validateDescription(expense_description)
    expense['Description'] = expense_description

    print("\n--- Expense added successfully. Please select save expense from Menu to save the expense ---")
    displayMenu()

#Function to save the expenses
def saveExpense():
    global expense
    
    if not expense:
        print("\n--- No expense to save. Please add an expense first. ---")
        displayMenu()
        return
    
    file_exists = os.path.isfile('expenses.csv')
    
    with open('expenses.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=expense.keys())
        
        if not file_exists or os.stat('expenses.csv').st_size == 0:
            writer.writeheader()
        
        writer.writerow(expense)
        
        print("\n--- Expense saved successfully ---")
    
    # after file is closed, clear
    expense.clear()
    displayMenu()

#Function to view the expenses
def viewExpenses():
    if not os.path.isfile('expenses.csv'):
        print("\n--- No expenses recorded yet. Please add an expense first. ---")
        displayMenu()
        return
    
    print("\n--- Your Recorded Expenses ---")
    with open('expenses.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(f"Date: {row['Date']}, Category: {row['Category']}, Amount: ${row['Amount']}, Description: {row['Description']}")
    
    displayMenu()


def trackBudget():
    global budget
    if( not os.path.isfile('expenses.csv')):
        print("\n--- No expenses recorded yet. Please add an expense first. ---")
        displayMenu()
        return

    total_expenses = 0.0
    with open('expenses.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            total_expenses += float(row['Amount'])

    if(total_expenses > budget):
        print(f"\n--- WARNING: You have exceeded your monthly budget! ---")
    else:
        print(f"\n--- You have {budget - total_expenses} left for the month ---")
    displayMenu()

def validateDate(date):
    try:
        # Validate the date format
        parsedDate = datetime.strptime(date, '%Y-%m-%d')

        # Check if the date is in the future
        if parsedDate > datetime.now():
            print("\n--- Date cannot be in the future. Please enter a valid date. ---")
            displayMenu()
        elif parsedDate < budget_start_date or parsedDate > budget_end_date:
            print("\n--- Date is outside the budget period. Please enter a valid date within the budget period. ---")
            displayMenu()
    except ValueError:
        print("\n--- Invalid date format. Please use YYYY-MM-DD ---")
        displayMenu()

def validateCategory(category):
    if(category == ""):
        print("\n--- Expense category cannot be empty. ---")
        displayMenu()


def validateAmount(amount):
    global budget
    
    total_expenses = 0.0
    
    if os.path.isfile('expenses.csv'):
        with open('expenses.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                total_expenses += float(row['Amount'])
    
    total_expenses += amount
    
    if amount <= 0:
        print("\n--- Expense cannot be zero or negative ---")
        displayMenu()
    elif total_expenses > budget:
        print(f"\n--- WARNING: This expense will put you over your monthly budget! ---")
        print(f"Total expenses after adding this: ${total_expenses:.2f}")
        print(f"Your budget is: ${budget:.2f}")
        print("Consider controlling your expenses or increasing your budget.")

def validateDescription(description):
    if description == "":
        print("\n--- Expense description cannot be empty. ---")
        displayMenu()

def displayMenu():
    print("\n--- Personal Expense Tracker Menu ---")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Track Budget")
    print("4. Save Expense")
    print("5. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == '1':
        addExpense()
    elif choice == '2':
        viewExpenses()
    elif choice == '3':
        trackBudget()
    elif choice == '4':
        saveExpense()
    elif choice == '5':
        if(expense):
            save = input("You have unsaved expenses. Do you want to save them before exiting? (yes/no): ").strip().lower()
            if save == 'yes':
                saveExpense()
        print("Thank you for using the Personal Expense Tracker. Goodbye!")
        exit()
    else:
        print("Invalid choice, please try again.")
        displayMenu()

budget_start = input("Enter the budget start date (YYYY-MM-DD): ")
budget_end = input("Enter the budget end date (YYYY-MM-DD): ")
budget_start_date = datetime.strptime(budget_start, "%Y-%m-%d")
budget_end_date = datetime.strptime(budget_end, "%Y-%m-%d")

input_budget = int(input("\n--- Enter your monthly budget: ---\n"))
createMonthlyBudget(input_budget)

