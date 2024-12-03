import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import bcrypt

# SQLite Database Setup
def create_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Create users table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT NOT NULL,
                      password TEXT NOT NULL)''')
    
    # Create products table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                      product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      price REAL NOT NULL,
                      quantity INTEGER NOT NULL)''')
    
    conn.commit()
    conn.close()

# Call to create the database
create_db()

# User Authentication Functions
def register_user(username, password):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed))
    
    conn.commit()
    conn.close()
    messagebox.showinfo('Registration', 'User registered successfully!')

def login_user(username, password):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
        return True
    else:
        return False

# Inventory Management Functions
def add_product(name, price, quantity):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)', (name, price, quantity))
    conn.commit()
    conn.close()
    messagebox.showinfo('Product Management', 'Product added successfully!')

def edit_product(product_id, name, price, quantity):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('''UPDATE products 
                      SET name = ?, price = ?, quantity = ? 
                      WHERE product_id = ?''', (name, price, quantity, product_id))
    conn.commit()
    conn.close()
    messagebox.showinfo('Product Management', 'Product updated successfully!')

def delete_product(product_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo('Product Management', 'Product deleted successfully!')

# Low stock alert report
def low_stock_alert(threshold=10):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT name, quantity FROM products WHERE quantity < ?', (threshold,))
    low_stock_products = cursor.fetchall()
    
    if low_stock_products:
        alert_message = "\n".join([f"{name}: {quantity} units left" for name, quantity in low_stock_products])
        messagebox.showinfo("Low Stock Alert", alert_message)
    else:
        messagebox.showinfo("Low Stock Alert", "No products below threshold.")
    conn.close()

# GUI Setup
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("400x400")

# Functionality for login window
def login():
    username = simpledialog.askstring("Login", "Enter username")
    password = simpledialog.askstring("Login", "Enter password", show='*')
    
    if login_user(username, password):
        messagebox.showinfo("Login", "Login successful!")
        inventory_management_screen()
    else:
        messagebox.showerror("Login", "Invalid credentials!")

# Functionality for registration window
def register():
    username = simpledialog.askstring("Register", "Enter username")
    password = simpledialog.askstring("Register", "Enter password", show='*')
    
    register_user(username, password)

# Inventory Management Screen
def inventory_management_screen():
    top = tk.Toplevel()
    top.title("Manage Inventory")
    top.geometry("400x400")
    
    # Labels and entry fields for product details
    tk.Label(top, text="Product Name").pack(pady=5)
    product_name = tk.Entry(top)
    product_name.pack(pady=5)

    tk.Label(top, text="Price").pack(pady=5)
    product_price = tk.Entry(top)
    product_price.pack(pady=5)

    tk.Label(top, text="Quantity").pack(pady=5)
    product_quantity = tk.Entry(top)
    product_quantity.pack(pady=5)

    # Add Product button
    def add_product_gui():
        name = product_name.get()
        price = float(product_price.get())
        quantity = int(product_quantity.get())
        add_product(name, price, quantity)
    
    tk.Button(top, text="Add Product", command=add_product_gui).pack(pady=5)

    # Low Stock Alert Button
    tk.Button(top, text="Low Stock Alert", command=low_stock_alert).pack(pady=5)

    # Delete Product Entry and Button
    tk.Label(top, text="Enter Product ID to Delete").pack(pady=5)
    delete_id = tk.Entry(top)
    delete_id.pack(pady=5)
    
    def delete_product_gui():
        product_id = int(delete_id.get())
        delete_product(product_id)
    
    tk.Button(top, text="Delete Product", command=delete_product_gui).pack(pady=5)

    # Edit Product Section
    tk.Label(top, text="Edit Product ID").pack(pady=5)
    edit_id = tk.Entry(top)
    edit_id.pack(pady=5)

    def edit_product_gui():
        product_id = int(edit_id.get())
        name = product_name.get()
        price = float(product_price.get())
        quantity = int(product_quantity.get())
        edit_product(product_id, name, price, quantity)

    tk.Button(top, text="Edit Product", command=edit_product_gui).pack(pady=5)

# Main GUI Buttons for Login and Registration
tk.Button(root, text="Login", command=login).pack(pady=10)
tk.Button(root, text="Register", command=register).pack(pady=10)

root.mainloop()
