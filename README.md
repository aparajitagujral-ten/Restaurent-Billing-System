# 🍽️ Restaurant Billing System (Problem Statement 43)

A versatile, multi-format **Restaurant Point of Sale (POS) and Billing System** built according to **Problem Statement 43 (PS 43)**.

Designed so that **anyone**—evaluators, teachers, staff, or customers—can run and access it easily across desktop, mobile, browser, or terminal.

---

## 📋 Problem Statement Specification (PS 43)

| Component | Specification |
|---|---|
| **Menu Items** | • **Dosa**: ₹80<br>• **Idli**: ₹40<br>• **Thali**: ₹150<br>• **Tea**: ₹20 |
| **Subtotal Calculation** | $\sum (\text{item\_price} \times \text{quantity})$ |
| **Discount Rule** | **10% Flat Discount** if $\text{Subtotal} > 500$, otherwise $0$ |
| **GST Calculation** | **5% GST** on taxable amount: $(\text{Subtotal} - \text{Discount}) \times 0.05$ |
| **Grand Total** | $(\text{Subtotal} - \text{Discount}) + \text{GST}$ |

---

## 🚀 Choose How You Want to Run It

| Format | How to Launch | Best For | Requirements |
|---|---|---|---|
| 📁 **Zero-Install Web App** | Double-click `index.html` | Sharing with anyone without Python installed | Any browser (Chrome, Edge, Safari) |
| 💻 **Desktop GUI App** | Double-click `run_desktop_app.bat`<br>*(or `python gui_app.py`)* | Standalone native desktop window | Python 3 (Tkinter built-in) |
| 🌐 **Local Web Server** | Double-click `run_web_app.bat`<br>*(or `python app.py`)* | Interactive browser POS, auto-launches browser | Python 3 (No pip install needed!) |
| 📱 **Mobile & Wi-Fi Sharing** | Open Network URL from `app.py`<br>*(e.g., `http://192.168.x.x:5000`)* | Anyone on same Wi-Fi, phone, or tablet | **No Python on phone!** Just a browser |
| ⌨️ **Terminal / CLI** | Double-click `run_terminal.bat`<br>*(or `python restaurant_billing.py`)* | Viva, grading, quick terminal test | Python 3 |

---

## 🌟 Key Features

1. **Multi-Format Architecture**:
   - **Terminal Core (`restaurant_billing.py`)**: Direct, accurate implementation of PS 43 logic with clean receipt printing.
   - **Desktop GUI (`gui_app.py`)**: Modern Tkinter application with dish cards, live totals, quantity controls, and modal receipt preview.
   - **Web POS App (`index.html`)**: Beautiful, responsive Tailwind CSS interface featuring an interactive cart, visual discount threshold progress bar, thermal receipt styling, print-to-PDF, and order history.
   - **Built-in Server (`app.py`)**: Standard library HTTP server with REST API endpoints (`/api/menu`, `/api/calculate`, `/api/order`).

2. **Accurate PS 43 Calculations**:
   - Dynamic item additions and quantity scaling.
   - Live discount progress indicator showing how much more to add to unlock 10% OFF.
   - Precise 5% GST computation on post-discount amount.

3. **Receipt & Invoice Actions**:
   - Print or save receipt directly to PDF (`window.print()` formatted for 80mm thermal receipt paper).
   - Export receipt as a plain text file (`.txt`).
   - Copy formatted receipt to clipboard.

4. **Extensible Menu**:
   - Add custom dishes and set custom prices on the fly without breaking default PS 43 items.

---

## 📱 How Anyone Can Access from Mobile or Another Computer (LAN)

You do **not** need Python installed on smartphones or other devices:

1. On your host computer, run `run_web_app.bat` (or `python app.py`).
2. The terminal displays your network address, for example:
   ```
   ============================================================
         RESTAURANT BILLING POS SERVER RUNNING (PS 43)      
   ============================================================
     * Local Browser URL  :
       --> http://localhost:5000

     * Mobile / Wi-Fi Network URL (For Everyone on Same Wi-Fi):
       --> http://192.168.29.230:5000
   ============================================================
   ```
3. Any phone, iPad, tablet, or laptop connected to the same Wi-Fi or mobile hotspot can type that URL (`http://192.168.x.x:5000`) into their mobile browser to view and place orders!

---

## 🧮 Calculation Example

**Order:**
- 2 $\times$ Dosa (@ ₹80) = ₹160.00
- 3 $\times$ Thali (@ ₹150) = ₹450.00
- 2 $\times$ Tea (@ ₹20) = ₹40.00

**Computation:**
- **Subtotal**: $160 + 450 + 40 = \text{₹}650.00$
- **Discount (Subtotal > 500)**: $650 \times 0.10 = \text{₹}65.00$
- **Taxable Amount**: $650 - 65 = \text{₹}585.00$
- **GST (5%)**: $585 \times 0.05 = \text{₹}29.25$
- **Grand Total**: $585 + 29.25 = \text{₹}614.25$

---

## 📁 File Structure

```
Project 2/
├── restaurant_billing.py   # Core PS 43 Python CLI script
├── gui_app.py              # Desktop GUI application (Tkinter, zero dependencies)
├── app.py                  # Web POS server & REST API (http.server, zero dependencies)
├── index.html              # Responsive Web POS (Runs standalone or via server)
├── run_desktop_app.bat     # One-click desktop launcher
├── run_web_app.bat         # One-click web server launcher
├── run_terminal.bat        # One-click terminal launcher
└── README.md               # Complete documentation & guide
```
