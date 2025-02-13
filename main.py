# Implementation for Jewelry Inventory Management System by Jourdyn Lao

import datetime

# ---------------- Global Data Stores ----------------

# Dictionary to store registered user accounts.
# Key: email, Value: dict with user details {"name": ..., "password": ...}
registered_users = {}

# List of inventory items.
# Each item is represented as a dictionary with keys: id, name, category, price, quantity.
inventory_items = []

# List of sales records.
# Each sale is represented as a dictionary with keys: sale_id, customer_name, payment_method,
# repeat_customer, item_name, quantity, total_amount, date.
sales_records = []

# ---------------- Global Counters ----------------

# Counter for the next unique inventory item ID.
next_inventory_item_id = 1

# Counter for the next unique sale record ID.
next_sale_record_id = 1

# ---------------- Preset Items for Inventory ----------------

# Preset items offered as a convenience option when adding new inventory items.
PRESET_ITEMS = [
    {"name": "Rose Gold Morganite Halo Ring", "category": "Ring", "price": 350.0},
    {"name": "White Gold Tennis Bracelet with Cubic Zirconia", "category": "Bracelet", "price": 200.0},
    {"name": "Platinum Princess-Cut Diamond Stud Earrings", "category": "Earrings", "price": 500.0},
    {"name": "Sterling Silver Charm Bracelet with Assorted Charms", "category": "Bracelet", "price": 80.0},
    {"name": "Yellow Gold Infinity Knot Pendant Necklace", "category": "Necklace", "price": 150.0},
    {"name": "Double-Strand Cultured Pearl Choker", "category": "Necklace", "price": 220.0},
    {"name": "Tungsten Carbide Men’s Wedding Band", "category": "Band", "price": 180.0}
]

# ---------------- Custom Exception for Navigation ----------------


class NavigationCommandException(Exception):
    """
    Custom exception to signal that a navigation command has been entered.
    This allows the program to immediately abort the current process and switch pages.
    """
    pass

# ---------------- Navigation Helper Functions ----------------


def execute_navigation_command(command, current_user):
    """
    Handle navigation commands by routing to the corresponding page.
    If a navigation command is entered, the respective function is called.
    """
    if command == 'd':
        display_dashboard(current_user)
    elif command == 'i':
        manage_inventory(current_user)
    elif command == 's':
        manage_sales(current_user)
    elif command == 'h':
        display_help_page(current_user)
    elif command == 'l':
        print("Logging out...\n")
        run_inventory_system()  # Return to the main entry point (login/registration)
    # Raise exception to immediately abort the current process.
    raise NavigationCommandException()


def input_with_nav_check(prompt, current_user):
    """
    Replacement for input() that checks whether the user typed a navigation command.
    If a navigation command is detected, the function immediately calls the corresponding page
    and raises a NavigationCommandException. Otherwise, the user input is returned.
    """
    user_input = input(prompt)
    cmd = user_input.strip().lower()
    if cmd in ['d', 'i', 's', 'h', 'l']:
        execute_navigation_command(cmd, current_user)
    return user_input


def display_navigation_bar():
    """
    Prints a consistent navigation bar with letter codes to help users move between sections.
    """
    print("\n--------------------------------------------")
    print("NAVIGATION: (D)ashboard | (I)nventory | (S)ales Record | (H)elp | (L)ogout")
    print("--------------------------------------------\n")

# ---------------- Main Program Loop ----------------


def run_inventory_system():
    """
    The main loop of the Jewelry Inventory Management System.
    Displays the welcome screen and prompts the user to register, log in, or exit.
    """
    while True:
        print("\n============================================")
        print("Welcome to the Jewelry Inventory Management System")
        print("============================================")
        print("Please choose an option:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            current_user = login_user()
            if current_user:
                display_main_menu(current_user)
        elif choice == "3":
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

# ---------------- User Registration & Login ----------------


def register_user():
    """
    Registration page UI:
      - Displays a header and instructions.
      - Checks for duplicate email addresses.
      - Allows cancellation by entering 'B' at any prompt.
    """
    print("\n================================")
    print("         REGISTRATION           ")
    print("================================")
    print("Welcome to the Jewelry Inventory System!")
    print("Creating an account allows you to easily manage your jewelry store inventory and sales data all in one place.")
    print("Enter 'B' at any prompt to cancel and return to the main menu.\n")

    # Get the user's name.
    user_name = input("Name: ").strip()
    if user_name.lower() == "b":
        print("Registration cancelled. Returning to main menu.")
        return

    # Loop to ensure the email is not already registered.
    while True:
        user_email = input("Email Address: ").strip()
        if user_email.lower() == "b":
            print("Registration cancelled. Returning to main menu.")
            return
        if user_email in registered_users:
            print("Error: This email is already in use. Please try a different email.")
        else:
            break

    user_password = input("Password: ").strip()
    if user_password.lower() == "b":
        print("Registration cancelled. Returning to main menu.")
        return
    confirm_password = input("Confirm Password: ").strip()
    while confirm_password != user_password:
        print("Error: Passwords do not match. Please try again.")
        confirm_password = input("Confirm Password (or enter 'B' to cancel): ").strip()
        if confirm_password.lower() == "b":
            print("Registration cancelled. Returning to main menu.")
            return

    # Save the new user in the global registered_users dictionary.
    registered_users[user_email] = {"name": user_name, "password": user_password}
    print("\nAccount created successfully! Please proceed to login.\n")


def login_user():
    """
    Login page UI:
      - Displays a login screen and prompts for user credentials.
      - Allows cancellation by entering 'B' at any prompt.
    """
    print("\n================================")
    print("             LOGIN              ")
    print("================================")
    print("Welcome back to the Jewelry Inventory System!")
    print("Please enter your account credentials below.")
    print("Enter 'B' at any prompt to cancel and return to the main menu.\n")

    user_email = input("Email Address: ").strip()
    if user_email.lower() == "b":
        print("Login cancelled. Returning to main menu.")
        return None
    user_password = input("Password: ").strip()
    if user_password.lower() == "b":
        print("Login cancelled. Returning to main menu.")
        return None

    if user_email in registered_users and registered_users[user_email]["password"] == user_password:
        print("\nLogin successful!\n")
        return {"email": user_email, "name": registered_users[user_email]["name"]}
    else:
        print("Invalid email or password. Please try again.\n")
        return None

# ---------------- Main Navigation Menu ----------------


def display_main_menu(current_user):
    """
    Main Navigation Menu for logged-in users.
    Provides options to navigate to the Dashboard, Inventory, Sales, Help pages, or logout.
    """
    while True:
        display_navigation_bar()
        nav_choice = input("Enter navigation option (e.g., D for Dashboard): ").strip().lower()
        if nav_choice == "d":
            display_dashboard(current_user)
        elif nav_choice == "i":
            manage_inventory(current_user)
        elif nav_choice == "s":
            manage_sales(current_user)
        elif nav_choice == "h":
            display_help_page(current_user)
        elif nav_choice == "l":
            print("Logging out...\n")
            break
        else:
            print("Invalid navigation choice. Please try again.")

# ---------------- Dashboard ----------------


def display_dashboard(current_user):
    """
    Dashboard page UI:
      - Displays a header, a welcome message, and quick statistics about inventory and sales.
      - Uses the navigation bar to allow immediate routing to other sections.
    """
    print("\n================================")
    print("            DASHBOARD           ")
    print("================================")
    display_navigation_bar()
    print(f"HELLO, {current_user['name'].upper()}!")
    print("Quick Stats:")
    print(f"- Total Items in Inventory: {len(inventory_items)}")
    print(f"- Total Sales Recorded: {len(sales_records)}")
    # Prompt the user for a navigation option.
    nav_choice = input("\nEnter navigation option (D, I, S, H, L): ").strip().lower()
    if nav_choice in ['d', 'i', 's', 'h', 'l']:
        execute_navigation_command(nav_choice, current_user)
    else:
        display_main_menu(current_user)

# ---------------- Inventory Management ----------------


def manage_inventory(current_user):
    """
    Inventory Management page UI:
      - Displays the current list of inventory items.
      - Offers options to add a new item, update an existing item, or remove an item.
      - Recognizes navigation commands at any prompt.
    """
    global next_inventory_item_id
    while True:
        print("\n================================")
        print("      INVENTORY MANAGEMENT      ")
        print("================================")
        display_navigation_bar()
        print("\nCurrent Inventory List:")
        if not inventory_items:
            print("Your inventory is empty.")
        else:
            for item in inventory_items:
                print(f"ID: {item['id']} | {item['name']} ({item['category']}) - Price: ${item['price']:.2f}, Qty: {item['quantity']}")
        print("\nSelect an option (1-4) or enter a navigation option (D, I, S, H, L):")
        print("1. Add New Item")
        print("2. Update Item")
        print("3. Remove Item")
        print("4. Back to Navigation Menu")
        user_choice = input("Enter your choice (1-4 or D/I/S/H/L): ").strip()
        if user_choice.lower() in ['d', 'i', 's', 'h', 'l']:
            execute_navigation_command(user_choice.lower(), current_user)
            return
        if user_choice == "1":
            try:
                add_inventory_item(current_user)
            except NavigationCommandException:
                continue
        elif user_choice == "2":
            try:
                update_inventory_item(current_user)
            except NavigationCommandException:
                continue
        elif user_choice == "3":
            try:
                delete_inventory_item(current_user)
            except NavigationCommandException:
                continue
        elif user_choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")


def add_inventory_item(current_user):
    """
    Add Item page UI:
      - Allows users to add a new inventory item either manually or by selecting from preset items.
      - Uses input_with_nav_check so that any navigation command is immediately handled.
      - Provides prompts for item name, category, cost, and quantity.
    """
    global next_inventory_item_id
    try:
        print("\n================================")
        print("             ADD ITEM           ")
        print("================================")
        display_navigation_bar()
        print("Fill in the details below to add a new inventory item.")
        print("Enter 'B' at any prompt to cancel and return to Inventory Management, or enter a navigation option (D, I, S, H, L).\n")

        # Ask whether to select a preset item.
        preset_choice = input_with_nav_check("Would you like to select from preset items? (Y/N): ", current_user)
        if preset_choice is None:
            return
        preset_choice = preset_choice.strip().lower()
        if preset_choice == "y":
            print("\nPreset Items:")
            for idx, preset in enumerate(PRESET_ITEMS, 1):
                print(f"{idx}. {preset['name']} ({preset['category']}) - Price: ${preset['price']:.2f}")
            try:
                preset_index = int(input_with_nav_check("Select a preset item by number (or 0 to cancel): ", current_user).strip())
                if preset_index == 0:
                    print("Preset selection cancelled. Proceeding with manual entry.\n")
                    preset_choice = "n"
                elif 1 <= preset_index <= len(PRESET_ITEMS):
                    selected_item = PRESET_ITEMS[preset_index - 1]
                    item_name = selected_item["name"]
                    item_category = selected_item["category"]
                    item_price = selected_item["price"]
                    print(f"Preset '{item_name}' selected. You can modify details later using the Update Item option.")
                else:
                    print("Invalid selection. Proceeding with manual entry.\n")
                    preset_choice = "n"
            except ValueError:
                print("Invalid input. Proceeding with manual entry.\n")
                preset_choice = "n"
        if preset_choice != "y":
            item_name = input_with_nav_check("Item Name: ", current_user)
            if item_name is None or item_name.strip().lower() == "b":
                print("Add Item cancelled. Returning to Inventory Management.")
                return
            item_name = item_name.strip()
            item_category = input_with_nav_check("Category: ", current_user)
            if item_category is None or item_category.strip().lower() == "b":
                print("Add Item cancelled. Returning to Inventory Management.")
                return
            item_category = item_category.strip()
            while True:
                cost_input = input_with_nav_check("Cost: ", current_user)
                if cost_input is None or cost_input.strip().lower() == "b":
                    print("Add Item cancelled. Returning to Inventory Management.")
                    return
                try:
                    item_price = float(cost_input.strip())
                    break
                except ValueError:
                    print("Invalid input. Please enter a numeric value for cost.")
        while True:
            quantity_input = input_with_nav_check("Quantity: ", current_user)
            if quantity_input is None or quantity_input.strip().lower() == "b":
                print("Add Item cancelled. Returning to Inventory Management.")
                return
            try:
                item_quantity = int(quantity_input.strip())
                break
            except ValueError:
                print("Invalid input. Please enter an integer for quantity.")

        # Create and add the new inventory item.
        new_item = {
            "id": next_inventory_item_id,
            "name": item_name,
            "category": item_category,
            "price": item_price,
            "quantity": item_quantity
        }
        inventory_items.append(new_item)
        next_inventory_item_id += 1
        print("\nItem added successfully!")
        nav_choice = input("Enter navigation option (D, I, S, H, L): ").strip().lower()
        if nav_choice in ['d', 'i', 's', 'h', 'l']:
            execute_navigation_command(nav_choice, current_user)
        else:
            display_main_menu(current_user)
    except NavigationCommandException:
        return


def update_inventory_item(current_user):
    """
    Update Item page UI:
      - Displays the current inventory items.
      - Prompts the user to select an item to update.
      - Provides pre-filled fields for the selected item that the user can modify.
      - Navigation commands are recognized at any prompt.
    """
    if not inventory_items:
        print("Inventory is empty. Nothing to update.")
        return
    try:
        print("\n================================")
        print("            UPDATE ITEM         ")
        print("================================")
        display_navigation_bar()
        print("\nCurrent Inventory List:")
        for item in inventory_items:
            print(f"ID: {item['id']} | {item['name']} ({item['category']}) - Price: ${item['price']:.2f}, Qty: {item['quantity']}")
        try:
            item_id = int(input_with_nav_check("\nEnter the ID of the item you wish to update (or 0 to cancel): ", current_user).strip())
        except ValueError:
            print("Invalid input. Returning to Inventory Management.")
            return
        if item_id == 0:
            print("Update cancelled. Returning to Inventory Management.")
            return
        selected_item = next((item for item in inventory_items if item["id"] == item_id), None)
        if selected_item is None:
            print("Item not found.")
            return

        print(f"\nUpdating item: {selected_item['name']}")
        new_name = input_with_nav_check(f"Item Name [{selected_item['name']}]: ", current_user)
        if new_name is None:
            return
        new_name = new_name.strip() or selected_item['name']
        new_category = input_with_nav_check(f"Category [{selected_item['category']}]: ", current_user)
        if new_category is None:
            return
        new_category = new_category.strip() or selected_item['category']

        while True:
            try:
                new_price_input = input_with_nav_check(f"Cost [{selected_item['price']:.2f}]: ", current_user)
                if new_price_input is None or new_price_input.strip().lower() == "b" or new_price_input.strip() == "":
                    new_price = selected_item['price']
                    break
                new_price = float(new_price_input.strip())
                break
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
        while True:
            try:
                new_quantity_input = input_with_nav_check(f"Quantity [{selected_item['quantity']}]: ", current_user)
                if new_quantity_input is None or new_quantity_input.strip().lower() == "b" or new_quantity_input.strip() == "":
                    new_quantity = selected_item['quantity']
                    break
                new_quantity = int(new_quantity_input.strip())
                break
            except ValueError:
                print("Invalid input. Please enter an integer.")

        # Update the selected inventory item with new details.
        selected_item["name"] = new_name
        selected_item["category"] = new_category
        selected_item["price"] = new_price
        selected_item["quantity"] = new_quantity
        print("\nItem updated successfully!")
        nav_choice = input("Enter navigation option (D, I, S, H, L): ").strip().lower()
        if nav_choice in ['d', 'i', 's', 'h', 'l']:
            execute_navigation_command(nav_choice, current_user)
        else:
            display_main_menu(current_user)
    except NavigationCommandException:
        return


def delete_inventory_item(current_user):
    """
    Removes an item from the inventory:
      - Displays the current inventory and prompts the user to select an item to delete.
      - Provides a confirmation prompt that warns the user of permanent deletion.
      - Recognizes navigation commands.
    """
    if not inventory_items:
        print("Inventory is empty. Nothing to remove.")
        return
    try:
        display_navigation_bar()
        print("\n================================")
        print("          REMOVE ITEM           ")
        print("================================")
        print("\nCurrent Inventory List:")
        for item in inventory_items:
            print(f"ID: {item['id']} | {item['name']} ({item['category']}) - Price: ${item['price']:.2f}, Qty: {item['quantity']}")
        try:
            item_id = int(input_with_nav_check("\nEnter the ID of the item to remove (or 0 to cancel): ", current_user).strip())
        except ValueError:
            print("Invalid input. Returning to Inventory Management.")
            return
        if item_id == 0:
            print("Removal cancelled.")
            return
        selected_item = next((item for item in inventory_items if item["id"] == item_id), None)
        if selected_item is None:
            print("Item not found.")
            return

        print(f"\nAre you sure you want to delete '{selected_item['name']}'?")
        print("Warning: Removing this item will permanently delete it from your inventory. You will have to re-add it if needed.")
        confirmation = input("Type 'Y' to confirm deletion, or any other key to cancel: ").strip()
        if confirmation.lower() == "y":
            inventory_items.remove(selected_item)
            print("Item removed successfully!")
        else:
            print("Deletion cancelled.")
        nav_choice = input("Enter navigation option (D, I, S, H, L): ").strip().lower()
        if nav_choice in ['d', 'i', 's', 'h', 'l']:
            execute_navigation_command(nav_choice, current_user)
        else:
            display_main_menu(current_user)
    except NavigationCommandException:
        return

# ---------------- Sales Recording ----------------


def manage_sales(current_user):
    """
    Sales Recording page UI:
      - Offers options to record a new sale or view the sales history.
      - Recognizes navigation commands.
    """
    global next_sale_record_id
    while True:
        print("\n================================")
        print("           SALES RECORD         ")
        print("================================")
        display_navigation_bar()
        print("\nSelect an option (1-3) or enter a navigation option (D, I, S, H, L):")
        print("1. Record a New Sale")
        print("2. View Sales History")
        print("3. Back to Navigation Menu")
        user_choice = input("Enter your choice (1-3 or D/I/S/H/L): ").strip()
        if user_choice.lower() in ['d', 'i', 's', 'h', 'l']:
            execute_navigation_command(user_choice.lower(), current_user)
            return
        if user_choice == "1":
            try:
                record_sale_transaction(current_user)
            except NavigationCommandException:
                continue
        elif user_choice == "2":
            try:
                display_sales_history(current_user)
            except NavigationCommandException:
                continue
        elif user_choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


def record_sale_transaction(current_user):
    """
    Records a sale transaction:
      - Captures customer details, payment method, and whether the customer is a repeat customer.
      - Displays available inventory and prompts the user to select the sold item and quantity.
      - Validates that the quantity sold does not exceed available stock.
      - Updates inventory and records the sale with the current date.
      - Uses input_with_nav_check to handle navigation commands.
    """
    global next_sale_record_id
    if not inventory_items:
        print("No inventory available to sell.")
        return
    try:
        print("\n--- Record a Sale ---")
        display_navigation_bar()
        customer_name = input_with_nav_check("Customer Name (or enter 'B' to cancel): ", current_user)
        if customer_name is None or customer_name.strip().lower() == "b":
            print("Sale recording cancelled. Returning to Sales Record.")
            return
        payment_method = input_with_nav_check("Payment Method (e.g., Cash, Card) (or enter 'B' to cancel): ", current_user)
        if payment_method is None or payment_method.strip().lower() == "b":
            print("Sale recording cancelled. Returning to Sales Record.")
            return
        repeat_input = input_with_nav_check("Is this a repeat customer? (Y/N) (or enter 'B' to cancel): ", current_user)
        if repeat_input is None or repeat_input.strip().lower() == "b":
            print("Sale recording cancelled. Returning to Sales Record.")
            return
        repeat_customer = "Yes" if repeat_input.strip().lower() == "y" else "No"

        print("\nAvailable Inventory:")
        for item in inventory_items:
            print(f"ID: {item['id']} | {item['name']} ({item['category']}) - Price: ${item['price']:.2f}, Qty: {item['quantity']}")
        try:
            item_id = int(input_with_nav_check("\nEnter the ID of the item sold (or 0 to cancel): ", current_user).strip())
        except ValueError:
            print("Invalid input. Returning to Sales Record.")
            return
        if item_id == 0:
            print("Sale recording cancelled. Returning to Sales Record.")
            return
        selected_item = next((item for item in inventory_items if item["id"] == item_id), None)
        if selected_item is None:
            print("Item not found.")
            return

        while True:
            try:
                quantity_sold = int(input_with_nav_check("Quantity Sold (or 0 to cancel): ", current_user).strip())
                if quantity_sold == 0:
                    print("Sale recording cancelled. Returning to Sales Record.")
                    return
                if quantity_sold < 0:
                    print("Quantity sold must be positive.")
                    continue
                if quantity_sold > selected_item["quantity"]:
                    print(f"Insufficient stock. Only {selected_item['quantity']} available.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter an integer.")
        total_sale_amount = selected_item["price"] * quantity_sold
        sale_date = datetime.date.today().strftime("%Y-%m-%d")
        confirmation = input(f"\nConfirm sale of {quantity_sold} '{selected_item['name']}' for {customer_name} "
                               f"(Payment: {payment_method}, Repeat: {repeat_customer}) at total ${total_sale_amount:.2f} on {sale_date}? (Y/N): ").strip()
        if confirmation.lower() != "y":
            print("Sale cancelled.")
            return
        # Create and record the sale.
        sale_record = {
            "sale_id": next_sale_record_id,
            "customer_name": customer_name,
            "payment_method": payment_method,
            "repeat_customer": repeat_customer,
            "item_name": selected_item["name"],
            "quantity": quantity_sold,
            "total_amount": total_sale_amount,
            "date": sale_date
        }
        sales_records.append(sale_record)
        next_sale_record_id += 1
        # Update the inventory by reducing the quantity of the sold item.
        selected_item["quantity"] -= quantity_sold
        print("Sale recorded successfully! Inventory updated.")
        nav_choice = input("Enter navigation option (D, I, S, H, L): ").strip().lower()
        if nav_choice in ['d', 'i', 's', 'h', 'l']:
            execute_navigation_command(nav_choice, current_user)
        else:
            display_main_menu(current_user)
    except NavigationCommandException:
        return


def display_sales_history(current_user):
    """
    Displays the sales history:
      - Initially shows minimal details (item name, quantity, and date) for each sale.
      - Optionally expands to show detailed information upon user request.
    """
    print("\n===== Minimal Sales History =====")
    display_navigation_bar()
    if not sales_records:
        print("No sales recorded yet.")
    else:
        for sale in sales_records:
            print(f"Item: {sale['item_name']} | Qty: {sale['quantity']} | Date: {sale['date']}")
    user_choice = input("\nWould you like to expand the details? (Y/N or enter a navigation option): ").strip().lower()
    if user_choice in ['d', 'i', 's', 'h', 'l']:
        execute_navigation_command(user_choice, current_user)
        return
    elif user_choice == "y":
        print("\n===== Expanded Sales History =====")
        for sale in sales_records:
            print(f"Sale ID: {sale['sale_id']} | Customer: {sale['customer_name']} | Payment: {sale['payment_method']} | "
                  f"Repeat: {sale['repeat_customer']} | Item: {sale['item_name']} | Qty: {sale['quantity']} | "
                  f"Total: ${sale['total_amount']:.2f} | Date: {sale['date']}")
    nav_choice = input("\nEnter navigation option (D, I, S, H, L): ").strip().lower()
    if nav_choice in ['d', 'i', 's', 'h', 'l']:
        execute_navigation_command(nav_choice, current_user)
    else:
        display_main_menu(current_user)

# ---------------- Help Page ----------------


def display_help_page(current_user):
    """
    Help page UI:
      - Provides step-by-step instructions on how to use the system.
      - Includes contact information for further assistance.
      - Prompts the user to choose a navigation option to return to the main menu.
    """
    print("\n================================")
    print("              HELP              ")
    print("================================")
    display_navigation_bar()
    print("\nHaving Trouble? Here’s How to Get Started:")
    print("1. To register an account, select 'Register' from the main menu and fill in your details.")
    print("2. To log in, select 'Login' and enter your email and password.")
    print("3. Select (D) Dashboard to view quick stats about your inventory and sales.")
    print("4. Select (I) Inventory to add, update, or remove items in your inventory.")
    print("5. Select (S) Sales Record to record sales transactions and view sales history.")
    print("6. Select (L) Logout to log out from the system and return to the Welcome Menu")
    print("7. For any questions, email support@jewelryinventorysystem.com or call (123) 456-7890.")
    nav_choice = input("\nEnter navigation option (D, I, S, H, L): ").strip().lower()
    if nav_choice in ['d', 'i', 's', 'h', 'l']:
        execute_navigation_command(nav_choice, current_user)
    else:
        display_main_menu(current_user)

# ---------------- Program Entry Point ----------------


if __name__ == "__main__":
    run_inventory_system()
