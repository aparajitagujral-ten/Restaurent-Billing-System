# Restaurant Billing System

**PS No. 43** | Rungta International Skills University | B.Tech CSE Core

A console billing program written in Python 3. The cashier enters the customer's items and quantities, and the program prints a neat bill with subtotal, discount, GST and grand total.

**Concepts used:** Dictionaries, Loops, Functions, Calculations

## Author

- **Name:** Aparajita Gujral
- **ERP ID:** RU-26-02378
- **Course:** B.Tech CSE Core

## Menu

| Item  | Price   |
|-------|---------|
| Dosa  | Rs. 80  |
| Idli  | Rs. 40  |
| Thali | Rs. 150 |
| Tea   | Rs. 20  |

## Billing Rules

- **Discount:** 10% of the subtotal, only if the subtotal is **more than Rs. 500**.
- **GST:** 5% of the amount **after** discount.
- **Grand Total** = Subtotal - Discount + GST

## Features

- Menu stored in a dictionary
- Loop takes many items until the cashier types `bill`
- Separate functions for subtotal, discount, GST and total
- Input validation for item name and quantity
- Neat formatted bill
- Every bill is saved to `bill_history.csv`

## How to Run

```
python restaurant_billing.py
```

Type an item name, then its quantity. Type `bill` to generate the bill.

### Example

```
Order item: Thali
Quantity: 4
Thali x4 added | Amount: 600
Order item: Dosa
Quantity: 2
Dosa x2 added | Amount: 160
Order item: Tea
Quantity: 2
Tea x2 added | Amount: 40
Order item: bill

Subtotal: 800 | Discount: 80.00
GST (5%): 36.00 | Grand Total: 756.00

Bill saved to bill_history.csv
```

## Test Cases

| #  | Scenario                  | Input                              | Result                                                      |
|----|---------------------------|------------------------------------|-------------------------------------------------------------|
| 1  | Normal input              | Dosa, quantity 2                   | `Dosa x2 added \| Amount: 160`                              |
| 2  | Boundary / minimum input  | Tea, quantity 1, generate bill     | Subtotal 20, Discount 0.00, GST 1.00, Grand Total 21.00     |
| 3a | Invalid item              | Pizza                              | "Item not on the menu. Available: Dosa, Idli, Thali, Tea"   |
| 3b | Quantity is zero          | Quantity 0                         | "Quantity must be at least 1."                              |
| 3c | Quantity is not a number  | Quantity abc                       | "Invalid quantity. Enter a whole number."                   |
| 4  | Different valid scenario  | Thali x4, Dosa x2, Tea x2          | Subtotal 800, Discount 80.00, GST 36.00, Grand Total 756.00 |

Full outputs are in `Test_Cases_Aparajita_Gujral.pdf`.

### Run all test cases automatically

```
python run_tests.py
```

This reads each CSV file in the `test_cases` folder, runs the program with the input and checks the expected output.

## Project Files

```
restaurant_billing/
├── restaurant_billing.py    main program
├── run_tests.py             automatic test runner
├── menu.csv                 menu prices
├── bill_history.csv         created automatically when a bill is generated
├── README.md
└── test_cases/
    ├── test_case_1_normal_input.csv
    ├── test_case_2_boundary_input.csv
    ├── test_case_3_invalid_input.csv
    └── test_case_4_different_valid_scenario.csv
```

## Project Mentor

**Mentored by:** Mr. Satyaprakash Sethy

**GitHub:** [@SATYAPRAKASHSETHY](https://github.com/SATYAPRAKASHSETHY)

**Role:** Python Mentor / Technical Guide
