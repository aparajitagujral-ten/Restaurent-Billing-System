"""
Restaurant Billing System (PS 43)
Core Python Terminal Implementation

Problem Statement 43:
- Menu: Dosa (80), Idli (40), Thali (150), Tea (20)
- Subtotal: Sum of (item price * quantity)
- Discount: 10% on orders where subtotal > 500
- GST: 5% on discounted amount (subtotal - discount)
- Grand Total: (subtotal - discount) + GST
"""

import datetime
import sys

# Ensure UTF-8 output if supported, else fallback gracefully
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Standard Menu as per PS 43
menu = {
    "Dosa": 80,
    "Idli": 40,
    "Thali": 150,
    "Tea": 20
}


def calculate_subtotal(order, current_menu=None):
    """Calculates subtotal by summing (price * quantity) for all ordered items."""
    active_menu = current_menu if current_menu is not None else menu
    total = 0
    for item in order:
        total = total + active_menu[item] * order[item]
    return total


def calculate_discount(subtotal):
    """
    Applies a 10% discount if the subtotal exceeds 500.
    Returns 0 otherwise.
    """
    if subtotal > 500:
        return subtotal * 0.10
    return 0.0


def calculate_gst(amount):
    """Calculates 5% GST on the taxable amount."""
    return amount * 0.05


def print_bill(order, customer_name="Walk-in Customer", table_no="Table 1", current_menu=None):
    """Computes totals and prints a formatted receipt to the terminal."""
    active_menu = current_menu if current_menu is not None else menu
    subtotal = calculate_subtotal(order, active_menu)
    discount = calculate_discount(subtotal)
    discounted_amount = subtotal - discount
    gst = calculate_gst(discounted_amount)
    grand_total = discounted_amount + gst

    now = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")

    print("\n==========================================")
    print("        RESTAURANT BILLING (PS 43)        ")
    print("==========================================")
    print(f" Date & Time: {now}")
    print(f" Customer   : {customer_name}")
    print(f" Table/Order: {table_no}")
    print("------------------------------------------")
    print(f" {'Item':<12} {'Qty':>5} {'Rate':>9} {'Total':>10}")
    print("------------------------------------------")

    for item, qty in order.items():
        rate = active_menu[item]
        item_total = rate * qty
        print(f" {item:<12} {qty:>5} {rate:>9.2f} {item_total:>10.2f}")

    print("------------------------------------------")
    print(f" {'Subtotal:':<26} Rs. {subtotal:>8.2f}")
    if discount > 0:
        print(f" {'Discount (10% > 500):':<26} -Rs. {discount:>7.2f}")
    else:
        print(f" {'Discount (Orders > 500):':<26}  Rs. {0.0:>8.2f}")
    print(f" {'GST (5%):':<26} +Rs. {gst:>8.2f}")
    print("==========================================")
    print(f" {'GRAND TOTAL:':<26} Rs. {grand_total:>8.2f}")
    print("==========================================")
    print("       Thank You for Dining With Us!      ")
    print("==========================================\n")

    return {
        "subtotal": subtotal,
        "discount": discount,
        "gst": gst,
        "grand_total": grand_total
    }


def main():
    order = {}
    print("\n==========================================")
    print("   WELCOME TO RESTAURANT BILLING (PS 43)   ")
    print("==========================================")
    print("Menu Available:")
    for item, price in menu.items():
        print(f"  * {item:<10} : Rs. {price:.2f}")
    print("------------------------------------------")
    print("Commands:")
    print("  * Type an item name to order")
    print("  * Type 'bill' to generate and print receipt")
    print("  * Type 'exit' to quit")
    print("==========================================\n")

    while True:
        try:
            item_input = input("Order item: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting billing system.")
            break

        if not item_input:
            continue

        item = item_input.title()

        if item.lower() == "exit":
            print("Goodbye!")
            break

        if item == "Bill":
            if len(order) == 0:
                print("[!] No items ordered yet. Add items before generating the bill.")
                continue
            print_bill(order)
            break

        # Check menu matching (case-insensitive)
        matched_item = None
        for m_item in menu:
            if m_item.lower() == item.lower():
                matched_item = m_item
                break

        if not matched_item:
            available = ", ".join(menu.keys())
            print(f"[X] '{item_input}' is not on the menu. Available items: {available}")
            continue

        qty_input = input(f"Enter quantity for {matched_item}: ").strip()
        if not qty_input.isdigit():
            print("[X] Invalid quantity. Please enter a positive whole number.")
            continue

        qty = int(qty_input)
        if qty < 1:
            print("[X] Quantity must be at least 1.")
            continue

        if matched_item in order:
            order[matched_item] += qty
        else:
            order[matched_item] = qty

        line_total = menu[matched_item] * qty
        current_subtotal = calculate_subtotal(order)
        print(f"[+] Added {matched_item} x{qty} (Rs. {line_total:.2f}). Running Subtotal: Rs. {current_subtotal:.2f}")
        if current_subtotal <= 500:
            remaining = 500.01 - current_subtotal
            print(f"    Tip: Add Rs. {remaining:.2f} more to unlock 10% discount!")
        else:
            print("    [10% Discount unlocked for this order!]")


if __name__ == "__main__":
    main()
