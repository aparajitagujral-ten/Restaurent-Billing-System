# PS 43 - Restaurant Billing System
# Language: Python 3
# Concepts: Dictionaries, Loops, Functions, Calculations
# Run with:  python restaurant_billing.py

import csv
import os
from datetime import datetime

# ---------- Menu (dictionary) ----------
MENU = {
    "Dosa": 80,
    "Idli": 40,
    "Thali": 150,
    "Tea": 20,
}

DISCOUNT_LIMIT = 500    # discount only if subtotal is MORE than this
DISCOUNT_RATE = 0.10    # 10 percent
GST_RATE = 0.05         # 5 percent (on amount after discount)
HISTORY_FILE = "bill_history.csv"


# ---------- Functions ----------
def add_item(order, name, qty):
    """Add item to the order dictionary (adds quantity if already ordered)."""
    order[name] = order.get(name, 0) + qty


def calculate_subtotal(order):
    total = 0
    for name, qty in order.items():
        total += MENU[name] * qty
    return total


def calculate_discount(subtotal):
    if subtotal > DISCOUNT_LIMIT:
        return subtotal * DISCOUNT_RATE
    return 0.0


def calculate_gst(amount_after_discount):
    return amount_after_discount * GST_RATE


def calculate_total(order):
    subtotal = calculate_subtotal(order)
    discount = calculate_discount(subtotal)
    gst = calculate_gst(subtotal - discount)
    grand_total = subtotal - discount + gst
    return subtotal, discount, gst, grand_total


def print_bill(order):
    subtotal, discount, gst, grand_total = calculate_total(order)
    print("\n" + "=" * 42)
    print("          RESTAURANT BILL")
    print("=" * 42)
    print(f"{'Item':<12}{'Qty':>5}{'Rate':>10}{'Amount':>12}")
    print("-" * 42)
    for name, qty in order.items():
        print(f"{name:<12}{qty:>5}{MENU[name]:>10}{MENU[name] * qty:>12.2f}")
    print("-" * 42)
    print(f"{'Subtotal:':<30}{subtotal:>12.2f}")
    print(f"{'Discount (10%):':<30}{discount:>12.2f}")
    print(f"{'GST (5%):':<30}{gst:>12.2f}")
    print("=" * 42)
    print(f"{'GRAND TOTAL:':<30}{grand_total:>12.2f}")
    print("=" * 42)
    # Short summary line (matches the expected output format)
    print(f"Subtotal: {subtotal:g} | Discount: {discount:.2f}")
    print(f"GST (5%): {gst:.2f} | Grand Total: {grand_total:.2f}\n")
    return subtotal, discount, gst, grand_total


def save_to_csv(order, subtotal, discount, gst, grand_total):
    """Save each bill into a CSV file (created automatically)."""
    file_exists = os.path.exists(HISTORY_FILE)
    items_text = ", ".join(f"{n} x{q}" for n, q in order.items())
    with open(HISTORY_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Items", "Subtotal", "Discount", "GST", "Grand Total"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), items_text,
                         f"{subtotal:.2f}", f"{discount:.2f}", f"{gst:.2f}", f"{grand_total:.2f}"])


def get_quantity():
    """Ask for quantity and validate it. Returns an int, or None if invalid."""
    try:
        text = input("Quantity: ").strip()
    except EOFError:
        return None
    try:
        qty = int(text)
    except ValueError:
        print("Invalid quantity. Enter a whole number.")
        return None
    if qty < 1:
        print("Quantity must be at least 1.")
        return None
    return qty


# ---------- Main program ----------
def main():
    order = {}
    print("Menu:", ", ".join(f"{n} Rs.{p}" for n, p in MENU.items()))
    print("Type an item name to order, or type 'bill' to generate the bill.\n")

    while True:
        try:
            item = input("Order item: ").strip().title()
        except EOFError:      # input finished (used by the test runner)
            break

        if item == "Bill":
            if not order:
                print("No items ordered yet.")
                continue
            totals = print_bill(order)
            save_to_csv(order, *totals)
            print(f"Bill saved to {HISTORY_FILE}")
            break

        if item not in MENU:
            print("Item not on the menu. Available: " + ", ".join(MENU))
            continue

        qty = get_quantity()
        if qty is None:
            continue

        add_item(order, item, qty)
        print(f"{item} x{qty} added | Amount: {MENU[item] * qty}")


if __name__ == "__main__":
    main()
