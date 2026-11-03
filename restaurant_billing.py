# Restaurant Billing System (PS 43)

menu = {"Dosa": 80, "Idli": 40, "Thali": 150, "Tea": 20}


def calculate_subtotal(order):
    total = 0
    for item in order:
        total = total + menu[item] * order[item]
    return total


def calculate_discount(subtotal):
    if subtotal > 500:
        return subtotal * 0.10
    return 0


def calculate_gst(amount):
    return amount * 0.05


def print_bill(order):
    subtotal = calculate_subtotal(order)
    discount = calculate_discount(subtotal)
    gst = calculate_gst(subtotal - discount)
    grand_total = subtotal - discount + gst

    print("\n------------- BILL -------------")
    for item in order:
        print(f"{item} x{order[item]} = {menu[item] * order[item]}")
    print("--------------------------------")
    print(f"Subtotal: {subtotal:.2f} | Discount: {discount:.2f}")
    print(f"GST (5%): {gst:.2f} | Grand Total: {grand_total:.2f}")
    print("--------------------------------")


def main():
    order = {}
    print("Menu:", menu)
    print("Type 'bill' to generate the bill.")

    while True:
        item = input("Order item: ").strip().title()

        if item == "Bill":
            if len(order) == 0:
                print("No items ordered yet.")
                continue
            print_bill(order)
            break

        if item not in menu:
            print("Item not on the menu. Available: Dosa, Idli, Thali, Tea")
            continue

        qty = input("Quantity: ").strip()
        if not qty.isdigit():
            print("Invalid quantity. Enter a whole number.")
            continue

        qty = int(qty)
        if qty < 1:
            print("Quantity must be at least 1.")
            continue

        if item in order:
            order[item] = order[item] + qty
        else:
            order[item] = qty
        print(f"{item} x{qty} added | Amount: {menu[item] * qty}")


main()
