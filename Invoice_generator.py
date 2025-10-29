"""
Automated Invoice Generator using Python & ReportLab
Author: Saumya Shah
"""

import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

# === 1️⃣ Database Setup ===
DB_NAME = "invoices.db"
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL
)
""")
conn.commit()


# === 2️⃣ Sample Data Insert (only if DB is empty) ===
cursor.execute("SELECT COUNT(*) FROM invoices")
if cursor.fetchone()[0] == 0:
    sample_data = [
        ("ABC Traders", 4520.75, datetime.now().strftime("%Y-%m-%d")),
        ("Bright Solutions", 7899.50, datetime.now().strftime("%Y-%m-%d")),
        ("Evergreen Store", 3200.00, datetime.now().strftime("%Y-%m-%d")),
    ]
    cursor.executemany("INSERT INTO invoices (customer, amount, date) VALUES (?, ?, ?)", sample_data)
    conn.commit()


# === 3️⃣ PDF Generation Function ===
def generate_invoice(invoice_id, customer, amount, date):
    file_name = f"Invoice_{invoice_id}.pdf"
    pdf = canvas.Canvas(file_name, pagesize=A4)
    pdf.setTitle("Invoice")

    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(220, 800, "INVOICE")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 760, f"Invoice ID: {invoice_id}")
    pdf.drawString(50, 740, f"Customer: {customer}")
    pdf.drawString(50, 720, f"Amount: ₹{amount:.2f}")
    pdf.drawString(50, 700, f"Date: {date}")
    pdf.line(50, 690, 550, 690)
    pdf.drawString(50, 670, "Thank you for your business!")
    pdf.save()

    print(f"✅ Generated: {file_name}")


# === 4️⃣ Fetch all invoices and generate PDFs ===
cursor.execute("SELECT * FROM invoices")
invoices = cursor.fetchall()

if not os.path.exists("generated_invoices"):
    os.makedirs("generated_invoices")

os.chdir("generated_invoices")

for inv in invoices:
    generate_invoice(inv[0], inv[1], inv[2], inv[3])

print("\n🎉 All invoices have been successfully generated!")

conn.close()
