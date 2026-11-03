"""
Restaurant Billing System (PS 43) - Web Application Server
Serves the interactive POS Billing Web App & REST API using Python's built-in http.server.
Zero external dependencies required (no pip install flask required).
Accessible locally or across LAN / Wi-Fi on mobile phones, tablets, and laptops.
"""

import http.server
import json
import os
import socket
import sys
import threading
import time
import webbrowser
from urllib.parse import urlparse

# Ensure UTF-8 output if possible
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PORT = 5000

# Standard PS 43 Menu
MENU = {
    "Dosa": 80.0,
    "Idli": 40.0,
    "Thali": 150.0,
    "Tea": 20.0
}

ORDERS_HISTORY = []


def calculate_subtotal(order, menu_dict=None):
    active_menu = menu_dict if menu_dict is not None else MENU
    return sum(active_menu.get(item, 0.0) * qty for item, qty in order.items())


def calculate_discount(subtotal):
    """PS 43 Rule: 10% discount on orders exceeding 500"""
    if subtotal > 500:
        return subtotal * 0.10
    return 0.0


def calculate_gst(amount):
    """PS 43 Rule: 5% GST on taxable amount"""
    return amount * 0.05


def compute_bill(order, customer="Walk-in Guest", table="Table 1", payment_mode="Cash"):
    subtotal = calculate_subtotal(order)
    discount = calculate_discount(subtotal)
    taxable = subtotal - discount
    gst = calculate_gst(taxable)
    grand_total = taxable + gst

    bill_id = f"INV-{len(ORDERS_HISTORY) + 101}"
    record = {
        "billNo": bill_id,
        "date": time.strftime("%Y-%m-%d %I:%M %p"),
        "customer": customer,
        "table": table,
        "paymentMode": payment_mode,
        "items": [{"item": k, "qty": v, "rate": MENU.get(k, 0.0), "total": MENU.get(k, 0.0) * v} for k, v in order.items()],
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "taxable": round(taxable, 2),
        "gst": round(gst, 2),
        "grandTotal": round(grand_total, 2)
    }
    return record


class RestaurantHttpHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS and caching controls
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            index_path = os.path.join(os.path.dirname(__file__), "index.html")
            if os.path.exists(index_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(index_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_error(404, "index.html not found")
                return

        elif path == "/api/menu":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(MENU).encode("utf-8"))
            return

        elif path == "/api/orders":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(ORDERS_HISTORY).encode("utf-8"))
            return

        # Default static file handling
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        try:
            body = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            body = {}

        if path == "/api/calculate":
            order = body.get("order", {})
            subtotal = calculate_subtotal(order)
            discount = calculate_discount(subtotal)
            taxable = subtotal - discount
            gst = calculate_gst(taxable)
            grand_total = taxable + gst

            resp = {
                "subtotal": round(subtotal, 2),
                "discount": round(discount, 2),
                "taxable": round(taxable, 2),
                "gst": round(gst, 2),
                "grand_total": round(grand_total, 2)
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        elif path == "/api/order":
            order = body.get("order", {})
            customer = body.get("customer", "Walk-in Guest")
            table = body.get("table", "Table 1")
            mode = body.get("payment_mode", "Cash")

            record = compute_bill(order, customer, table, mode)
            ORDERS_HISTORY.insert(0, record)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(record).encode("utf-8"))
            return

        elif path == "/api/add_item":
            item = body.get("name", "").strip().title()
            price = body.get("price", 0.0)
            if item and price > 0:
                MENU[item] = float(price)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "menu": MENU}).encode("utf-8"))
                return
            else:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid item or price"}).encode("utf-8"))
                return

        self.send_error(404, "Endpoint not found")

    def log_message(self, format, *args):
        # Suppress routine GET logging for cleaner terminal
        pass


def get_lan_ip():
    """Detects primary LAN IP for Wi-Fi / local network access."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.3)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except Exception:
            return "127.0.0.1"


def run_server(port=PORT):
    # Bind to 0.0.0.0 so all network devices (phones/laptops) can connect
    server_address = ("0.0.0.0", port)
    
    try:
        httpd = http.server.ThreadingHTTPServer(server_address, RestaurantHttpHandler)
    except OSError:
        # Fallback port if 5000 is occupied
        port = 5050
        server_address = ("0.0.0.0", port)
        httpd = http.server.ThreadingHTTPServer(server_address, RestaurantHttpHandler)

    lan_ip = get_lan_ip()
    local_url = f"http://localhost:{port}"
    lan_url = f"http://{lan_ip}:{port}"

    print("\n" + "=" * 60)
    print("      RESTAURANT BILLING POS SERVER RUNNING (PS 43)      ")
    print("=" * 60)
    print("  * Local Browser URL  :")
    print(f"    --> {local_url}")
    print()
    print("  * Mobile / Wi-Fi Network URL (For Everyone on Same Wi-Fi):")
    print(f"    --> {lan_url}")
    print("=" * 60)
    print("  Press Ctrl+C in this terminal to stop the server.")
    print("=" * 60 + "\n")

    # Automatically open local browser
    def open_browser():
        time.sleep(1.2)
        try:
            webbrowser.open(local_url)
        except Exception:
            pass

    threading.Thread(target=open_browser, daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping restaurant billing server... Goodbye!")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
