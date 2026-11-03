"""
Restaurant Billing System (PS 43) - Desktop GUI Application
Built using standard library Tkinter (No external pip dependencies required).
"""

import datetime
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Ensure UTF-8 output if possible
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Default Menu per PS 43
DEFAULT_MENU = {
    "Dosa": 80.0,
    "Idli": 40.0,
    "Thali": 150.0,
    "Tea": 20.0
}


def calculate_subtotal(order, menu_dict):
    return sum(menu_dict[item] * qty for item, qty in order.items())


def calculate_discount(subtotal):
    if subtotal > 500:
        return subtotal * 0.10
    return 0.0


def calculate_gst(amount):
    return amount * 0.05


class RestaurantBillingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Restaurant Billing System (PS 43)")
        self.geometry("980x680")
        self.minsize(880, 580)
        self.configure(bg="#F4F6F9")

        self.menu_data = dict(DEFAULT_MENU)
        self.cart = {}  # {item_name: quantity}
        self.order_counter = 101

        self.setup_styles()
        self.build_ui()
        self.refresh_cart_display()

    def setup_styles(self):
        self.style = ttk.Style(self)
        # Use 'clam' or 'alt' for cleaner look across Windows platforms
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        # Custom treeview styling
        self.style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#E2E8F0",
            foreground="#1E293B",
            relief="flat",
            padding=6
        )
        self.style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=28,
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            relief="flat"
        )
        self.style.map(
            "Treeview",
            background=[("selected", "#3B82F6")],
            foreground=[("selected", "#FFFFFF")]
        )

    def build_ui(self):
        # 1. Header Banner
        header = tk.Frame(self, bg="#1E3A8A", height=70)
        header.pack(fill="x", side="top")

        title_lbl = tk.Label(
            header,
            text="🍽️ Restaurant Billing POS (PS 43)",
            font=("Segoe UI", 18, "bold"),
            fg="#FFFFFF",
            bg="#1E3A8A"
        )
        title_lbl.pack(side="left", padx=20, pady=12)

        subtitle_lbl = tk.Label(
            header,
            text="Menu: Dosa (80) | Idli (40) | Thali (150) | Tea (20)  •  10% Off on > ₹500  •  5% GST",
            font=("Segoe UI", 9),
            fg="#93C5FD",
            bg="#1E3A8A"
        )
        subtitle_lbl.pack(side="right", padx=20, pady=12)

        # 2. Main Content Split
        main_panes = tk.Frame(self, bg="#F4F6F9")
        main_panes.pack(fill="both", expand=True, padx=16, pady=14)

        # Left Column: Menu Items & Quick Add
        left_col = tk.Frame(main_panes, bg="#FFFFFF", bd=1, relief="solid")
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))

        left_header = tk.Frame(left_col, bg="#EEF2FF", height=44)
        left_header.pack(fill="x")
        tk.Label(
            left_header,
            text="📋 Available Menu",
            font=("Segoe UI", 12, "bold"),
            fg="#1E3A8A",
            bg="#EEF2FF"
        ).pack(side="left", padx=12, pady=8)

        # Menu container
        self.menu_frame = tk.Frame(left_col, bg="#FFFFFF")
        self.menu_frame.pack(fill="both", expand=True, padx=14, pady=12)
        self.render_menu_cards()

        # Add custom item expander
        custom_frame = tk.LabelFrame(
            left_col,
            text=" + Add Custom Dish to Menu ",
            font=("Segoe UI", 9, "bold"),
            bg="#FFFFFF",
            fg="#475569",
            padx=10,
            pady=8
        )
        custom_frame.pack(fill="x", padx=14, pady=(0, 12))

        tk.Label(custom_frame, text="Name:", bg="#FFFFFF", font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w")
        self.new_dish_name = tk.Entry(custom_frame, font=("Segoe UI", 9), width=12)
        self.new_dish_name.grid(row=0, column=1, padx=4, pady=4)

        tk.Label(custom_frame, text="Price (Rs):", bg="#FFFFFF", font=("Segoe UI", 9)).grid(row=0, column=2, sticky="w")
        self.new_dish_price = tk.Entry(custom_frame, font=("Segoe UI", 9), width=8)
        self.new_dish_price.grid(row=0, column=3, padx=4, pady=4)

        add_custom_btn = tk.Button(
            custom_frame,
            text="Add Dish",
            command=self.add_custom_dish,
            bg="#3B82F6",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            relief="flat",
            padx=8,
            pady=2
        )
        add_custom_btn.grid(row=0, column=4, padx=6, pady=4)

        # Right Column: Current Order & Billing Summary
        right_col = tk.Frame(main_panes, bg="#FFFFFF", bd=1, relief="solid", width=480)
        right_col.pack(side="right", fill="both", expand=True)

        # Customer Details bar
        cust_bar = tk.Frame(right_col, bg="#F8FAFC", bd=1, relief="groove")
        cust_bar.pack(fill="x", padx=10, pady=10)

        tk.Label(cust_bar, text="Customer:", bg="#F8FAFC", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=6, pady=6, sticky="w")
        self.cust_name_ent = tk.Entry(cust_bar, font=("Segoe UI", 9), width=16)
        self.cust_name_ent.insert(0, "Guest")
        self.cust_name_ent.grid(row=0, column=1, padx=4, pady=6)

        tk.Label(cust_bar, text="Table:", bg="#F8FAFC", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=6, pady=6, sticky="w")
        self.table_ent = tk.Entry(cust_bar, font=("Segoe UI", 9), width=10)
        self.table_ent.insert(0, "Table 1")
        self.table_ent.grid(row=0, column=3, padx=4, pady=6)

        # Cart Table
        cart_frame = tk.Frame(right_col, bg="#FFFFFF")
        cart_frame.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        cols = ("item", "rate", "qty", "total")
        self.tree = ttk.Treeview(cart_frame, columns=cols, show="headings", height=8)
        self.tree.heading("item", text="Item")
        self.tree.heading("rate", text="Rate (Rs.)")
        self.tree.heading("qty", text="Qty")
        self.tree.heading("total", text="Total (Rs.)")

        self.tree.column("item", width=130, anchor="w")
        self.tree.column("rate", width=70, anchor="e")
        self.tree.column("qty", width=55, anchor="center")
        self.tree.column("total", width=85, anchor="e")

        tree_scroll = ttk.Scrollbar(cart_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        # Cart Controls (+, -, Remove)
        ctrl_frame = tk.Frame(right_col, bg="#FFFFFF")
        ctrl_frame.pack(fill="x", padx=10, pady=(0, 8))

        tk.Button(
            ctrl_frame,
            text="➕ Increase Qty",
            command=self.increase_selected_qty,
            bg="#E2E8F0",
            fg="#0F172A",
            font=("Segoe UI", 9),
            relief="flat",
            padx=8,
            pady=3,
            cursor="hand2"
        ).pack(side="left", padx=2)

        tk.Button(
            ctrl_frame,
            text="➖ Decrease Qty",
            command=self.decrease_selected_qty,
            bg="#E2E8F0",
            fg="#0F172A",
            font=("Segoe UI", 9),
            relief="flat",
            padx=8,
            pady=3,
            cursor="hand2"
        ).pack(side="left", padx=2)

        tk.Button(
            ctrl_frame,
            text="🗑️ Remove Item",
            command=self.remove_selected_item,
            bg="#FEE2E2",
            fg="#991B1B",
            font=("Segoe UI", 9),
            relief="flat",
            padx=8,
            pady=3,
            cursor="hand2"
        ).pack(side="left", padx=2)

        tk.Button(
            ctrl_frame,
            text="Clear Order",
            command=self.clear_cart,
            bg="#F1F5F9",
            fg="#64748B",
            font=("Segoe UI", 9),
            relief="flat",
            padx=8,
            pady=3,
            cursor="hand2"
        ).pack(side="right")

        # Live Calculation Summary Card
        summary_card = tk.Frame(right_col, bg="#F8FAFC", bd=1, relief="solid")
        summary_card.pack(fill="x", padx=10, pady=(0, 10))

        # Subtotal Row
        r1 = tk.Frame(summary_card, bg="#F8FAFC")
        r1.pack(fill="x", padx=12, pady=(6, 2))
        tk.Label(r1, text="Subtotal:", font=("Segoe UI", 10), bg="#F8FAFC", fg="#475569").pack(side="left")
        self.subtotal_lbl = tk.Label(r1, text="Rs. 0.00", font=("Segoe UI", 10, "bold"), bg="#F8FAFC", fg="#0F172A")
        self.subtotal_lbl.pack(side="right")

        # Discount Row
        r2 = tk.Frame(summary_card, bg="#F8FAFC")
        r2.pack(fill="x", padx=12, pady=2)
        self.discount_title_lbl = tk.Label(r2, text="Discount (10% if > Rs. 500):", font=("Segoe UI", 10), bg="#F8FAFC", fg="#475569")
        self.discount_title_lbl.pack(side="left")
        self.discount_lbl = tk.Label(r2, text="- Rs. 0.00", font=("Segoe UI", 10, "bold"), bg="#F8FAFC", fg="#16A34A")
        self.discount_lbl.pack(side="right")

        # GST Row
        r3 = tk.Frame(summary_card, bg="#F8FAFC")
        r3.pack(fill="x", padx=12, pady=2)
        tk.Label(r3, text="GST (5% on taxable):", font=("Segoe UI", 10), bg="#F8FAFC", fg="#475569").pack(side="left")
        self.gst_lbl = tk.Label(r3, text="+ Rs. 0.00", font=("Segoe UI", 10, "bold"), bg="#F8FAFC", fg="#0F172A")
        self.gst_lbl.pack(side="right")

        sep = tk.Frame(summary_card, height=1, bg="#CBD5E1")
        sep.pack(fill="x", padx=12, pady=4)

        # Grand Total Row
        r4 = tk.Frame(summary_card, bg="#F8FAFC")
        r4.pack(fill="x", padx=12, pady=(2, 6))
        tk.Label(r4, text="GRAND TOTAL:", font=("Segoe UI", 12, "bold"), bg="#F8FAFC", fg="#1E3A8A").pack(side="left")
        self.grand_total_lbl = tk.Label(r4, text="Rs. 0.00", font=("Segoe UI", 13, "bold"), bg="#F8FAFC", fg="#1E3A8A")
        self.grand_total_lbl.pack(side="right")

        # Tip indicator
        self.tip_lbl = tk.Label(summary_card, text="Tip: Orders over Rs. 500 get flat 10% discount!", font=("Segoe UI", 8, "italic"), bg="#F8FAFC", fg="#64748B")
        self.tip_lbl.pack(fill="x", padx=12, pady=(0, 6))

        # Bottom Action Bar
        action_bar = tk.Frame(right_col, bg="#FFFFFF")
        action_bar.pack(fill="x", padx=10, pady=(0, 10))

        gen_btn = tk.Button(
            action_bar,
            text="🧾 GENERATE & PRINT BILL",
            command=self.generate_bill,
            bg="#16A34A",
            fg="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2",
            pady=8
        )
        gen_btn.pack(fill="x")

    def render_menu_cards(self):
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        item_icons = {
            "Dosa": "🥞",
            "Idli": "🥟",
            "Thali": "🍱",
            "Tea": "☕"
        }

        row = 0
        col = 0
        for item, price in self.menu_data.items():
            icon = item_icons.get(item, "🍛")
            card = tk.Frame(self.menu_frame, bg="#F8FAFC", bd=1, relief="solid", padx=8, pady=8)
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

            tk.Label(card, text=f"{icon} {item}", font=("Segoe UI", 11, "bold"), bg="#F8FAFC", fg="#0F172A").pack(anchor="w")
            tk.Label(card, text=f"Price: Rs. {price:.2f}", font=("Segoe UI", 9), bg="#F8FAFC", fg="#475569").pack(anchor="w", pady=(2, 6))

            btn = tk.Button(
                card,
                text="➕ Add to Order",
                command=lambda name=item: self.add_item_to_cart(name),
                bg="#2563EB",
                fg="#FFFFFF",
                font=("Segoe UI", 9, "bold"),
                relief="flat",
                cursor="hand2",
                pady=3,
                padx=6
            )
            btn.pack(fill="x")

            col += 1
            if col > 1:
                col = 0
                row += 1

        self.menu_frame.columnconfigure(0, weight=1)
        self.menu_frame.columnconfigure(1, weight=1)

    def add_item_to_cart(self, item_name):
        self.cart[item_name] = self.cart.get(item_name, 0) + 1
        self.refresh_cart_display()

    def increase_selected_qty(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Item", "Please select an item from the cart table.")
            return
        item_name = self.tree.item(selected[0])["values"][0]
        if item_name in self.cart:
            self.cart[item_name] += 1
            self.refresh_cart_display()
            # reselect
            for child in self.tree.get_children():
                if self.tree.item(child)["values"][0] == item_name:
                    self.tree.selection_set(child)
                    break

    def decrease_selected_qty(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Item", "Please select an item from the cart table.")
            return
        item_name = self.tree.item(selected[0])["values"][0]
        if item_name in self.cart:
            if self.cart[item_name] > 1:
                self.cart[item_name] -= 1
            else:
                del self.cart[item_name]
            self.refresh_cart_display()
            # reselect if still exists
            if item_name in self.cart:
                for child in self.tree.get_children():
                    if self.tree.item(child)["values"][0] == item_name:
                        self.tree.selection_set(child)
                        break

    def remove_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Item", "Please select an item from the cart table.")
            return
        item_name = self.tree.item(selected[0])["values"][0]
        if item_name in self.cart:
            del self.cart[item_name]
            self.refresh_cart_display()

    def clear_cart(self):
        if not self.cart:
            return
        if messagebox.askyesno("Clear Order", "Are you sure you want to clear the entire order?"):
            self.cart.clear()
            self.refresh_cart_display()

    def add_custom_dish(self):
        name = self.new_dish_name.get().strip().title()
        price_text = self.new_dish_price.get().strip()

        if not name:
            messagebox.showerror("Error", "Please enter a valid dish name.")
            return

        try:
            price = float(price_text)
            if price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive price.")
            return

        self.menu_data[name] = price
        self.new_dish_name.delete(0, tk.END)
        self.new_dish_price.delete(0, tk.END)
        self.render_menu_cards()
        messagebox.showinfo("Success", f"'{name}' added to menu at Rs. {price:.2f}!")

    def refresh_cart_display(self):
        # Clear tree
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item, qty in self.cart.items():
            rate = self.menu_data.get(item, 0.0)
            total = rate * qty
            self.tree.insert("", "end", values=(item, f"{rate:.2f}", qty, f"{total:.2f}"))

        # Calculate totals
        subtotal = calculate_subtotal(self.cart, self.menu_data)
        discount = calculate_discount(subtotal)
        discounted_amount = subtotal - discount
        gst = calculate_gst(discounted_amount)
        grand_total = discounted_amount + gst

        self.subtotal_lbl.config(text=f"Rs. {subtotal:.2f}")
        self.discount_lbl.config(text=f"- Rs. {discount:.2f}")
        self.gst_lbl.config(text=f"+ Rs. {gst:.2f}")
        self.grand_total_lbl.config(text=f"Rs. {grand_total:.2f}")

        if subtotal == 0:
            self.tip_lbl.config(text="Cart is empty. Add dishes to start billing.", fg="#64748B")
        elif subtotal > 500:
            self.tip_lbl.config(text=f"🎉 10% Discount applied! Saved Rs. {discount:.2f}", fg="#16A34A")
        else:
            diff = 500.01 - subtotal
            self.tip_lbl.config(text=f"💡 Add Rs. {diff:.2f} more to unlock 10% Discount!", fg="#D97706")

    def generate_bill(self):
        if not self.cart:
            messagebox.showwarning("Empty Order", "Cannot generate bill: No items in the order!")
            return

        customer = self.cust_name_ent.get().strip() or "Walk-in Guest"
        table = self.table_ent.get().strip() or "Table 1"

        subtotal = calculate_subtotal(self.cart, self.menu_data)
        discount = calculate_discount(subtotal)
        discounted_amount = subtotal - discount
        gst = calculate_gst(discounted_amount)
        grand_total = discounted_amount + gst

        now = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
        bill_no = f"INV-{self.order_counter}"
        self.order_counter += 1

        # Build Bill text
        lines = []
        lines.append("==========================================")
        lines.append("        RESTAURANT BILLING (PS 43)        ")
        lines.append("       Namaste Flavors & Cafe             ")
        lines.append("==========================================")
        lines.append(f" Invoice No : {bill_no}")
        lines.append(f" Date & Time: {now}")
        lines.append(f" Customer   : {customer}")
        lines.append(f" Table/Seat : {table}")
        lines.append("------------------------------------------")
        lines.append(f" {'Item':<12} {'Qty':>5} {'Rate':>9} {'Total':>10}")
        lines.append("------------------------------------------")

        for item, qty in self.cart.items():
            rate = self.menu_data[item]
            item_total = rate * qty
            lines.append(f" {item:<12} {qty:>5} {rate:>9.2f} {item_total:>10.2f}")

        lines.append("------------------------------------------")
        lines.append(f" {'Subtotal:':<26} Rs. {subtotal:>8.2f}")
        if discount > 0:
            lines.append(f" {'Discount (10% > Rs. 500):':<26} -Rs. {discount:>7.2f}")
        else:
            lines.append(f" {'Discount (Orders > 500):':<26}  Rs. {0.0:>8.2f}")
        lines.append(f" {'GST (5% on taxable):':<26} +Rs. {gst:>8.2f}")
        lines.append("==========================================")
        lines.append(f" {'GRAND TOTAL:':<26} Rs. {grand_total:>8.2f}")
        lines.append("==========================================")
        lines.append("       Thank You for Dining With Us!      ")
        lines.append("==========================================")

        receipt_text = "\n".join(lines)

        # Show modal receipt dialog
        self.show_receipt_dialog(bill_no, receipt_text)

    def show_receipt_dialog(self, bill_no, receipt_text):
        dialog = tk.Toplevel(self)
        dialog.title(f"Receipt - {bill_no}")
        dialog.geometry("450x580")
        dialog.configure(bg="#F1F5F9")
        dialog.transient(self)
        dialog.grab_set()

        lbl = tk.Label(
            dialog,
            text=f"🧾 Final Receipt ({bill_no})",
            font=("Segoe UI", 12, "bold"),
            bg="#F1F5F9",
            fg="#1E3A8A"
        )
        lbl.pack(pady=10)

        text_box = tk.Text(dialog, font=("Consolas", 10), bg="#FFFFFF", fg="#0F172A", relief="solid", bd=1)
        text_box.insert("1.0", receipt_text)
        text_box.config(state="disabled")
        text_box.pack(fill="both", expand=True, padx=16, pady=6)

        btn_bar = tk.Frame(dialog, bg="#F1F5F9")
        btn_bar.pack(fill="x", padx=16, pady=10)

        def save_file():
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                initialfile=f"{bill_no}_receipt.txt",
                filetypes=[("Text File", "*.txt"), ("All Files", "*.*")]
            )
            if filename:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(receipt_text)
                messagebox.showinfo("Saved", f"Receipt saved to:\n{filename}")

        def copy_to_clipboard():
            self.clipboard_clear()
            self.clipboard_append(receipt_text)
            messagebox.showinfo("Copied", "Receipt copied to clipboard!")

        save_btn = tk.Button(
            btn_bar,
            text="💾 Save to File",
            command=save_file,
            bg="#3B82F6",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2"
        )
        save_btn.pack(side="left", padx=4)

        copy_btn = tk.Button(
            btn_bar,
            text="📋 Copy",
            command=copy_to_clipboard,
            bg="#E2E8F0",
            fg="#0F172A",
            font=("Segoe UI", 9),
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2"
        )
        copy_btn.pack(side="left", padx=4)

        close_btn = tk.Button(
            btn_bar,
            text="Close & New Order",
            command=lambda: [dialog.destroy(), self.clear_cart()],
            bg="#10B981",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2"
        )
        close_btn.pack(side="right", padx=4)


if __name__ == "__main__":
    app = RestaurantBillingApp()
    app.mainloop()
