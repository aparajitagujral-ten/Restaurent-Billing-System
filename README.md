# Restaurant Billing System (PS 43)

A simple command-line Python program that takes a customer's food order and prints a bill with discount and GST.

> **Submitted by:** <Your Name> | **Roll No:** <Your Roll No>
> **Tagging:** @<instructor-github-username>

## Project Image

![Project Image](project_image.png)

## Problem Statement

Build a billing system for a small restaurant that accepts items and quantities, then generates a bill showing subtotal, discount, GST and grand total.

## Features

- Fixed menu: Dosa (80), Idli (40), Thali (150), Tea (20)
- Add multiple items; repeated items are merged into one line
- Item names are case-insensitive (`dosa`, `DOSA`, `Dosa`)
- Input validation: unknown items, non-numeric / negative / decimal / zero quantities
- 10% discount if subtotal is above 500
- 5% GST on the amount after discount
- Prevents generating a bill for an empty order

## Billing Logic

```
Subtotal    = sum(price x quantity)
Discount    = 10% of Subtotal   (only if Subtotal > 500, else 0)
GST         = 5% of (Subtotal - Discount)
Grand Total = Subtotal - Discount + GST
```

## Requirements

- Python 3.x (no external libraries needed)

## How to Run

1. Clone the repository:
   ```
   git clone <your-repo-url>
   cd <repo-folder>
   ```
2. Run the program:
   ```
   python restaurant_billing.py
   ```
3. Enter an item name, then its quantity. Repeat for more items.
4. Type `bill` to generate the bill.

## Sample Run

```
Menu: {'Dosa': 80, 'Idli': 40, 'Thali': 150, 'Tea': 20}
Type 'bill' to generate the bill.
Order item: thali
Quantity: 4
Thali x4 added | Amount: 600
Order item: bill

------------- BILL -------------
Thali x4 = 600
--------------------------------
Subtotal: 600.00 | Discount: 60.00
GST (5%): 27.00 | Grand Total: 567.00
--------------------------------
```

## Repository Contents

| File | Description |
|------|-------------|
| `restaurant_billing.py` | Main code file |
| `testcase.pdf` | Test cases with inputs and expected results |
| `project_image.png` | Project image from the Project Allocation PDF |
| `README.md` | Project documentation |

No CSV/TXT data file is needed; the menu is stored inside the program.

## Test Cases

See `testcase.pdf` for 11 test cases covering normal orders, discount boundary (500), merging, and invalid inputs.
