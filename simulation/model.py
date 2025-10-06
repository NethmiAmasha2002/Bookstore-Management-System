import random
import threading
import time

class Book:
    def __init__(self, title, author, price, quantity):
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity
        self.purchases = 0

class Customer:
    def __init__(self, name, budget):
        self.name = name
        self.budget = budget
        self.purchases = 0
        self.active = True

class Employee:
    def __init__(self, name):
        self.name = name
        self.restocks = 0

class BookstoreModel:
    def __init__(self):
        self.books = []
        self.customers = []
        self.employees = []
        self.step_count = 0
        self.total_sales = 0
        self.total_revenue = 0
        self.total_restocks = 0
        self.running = False
        self.lock = threading.Lock()

        # History for graphs
        self.history_steps = []
        self.history_sales = []
        self.history_active_customers = []
        self.history_books_in_stock = []

    def initialize(self, num_customers, num_employees, num_books):
        sample_books = [
            ("1984", "George Orwell"),
        ("Pride and Prejudice", "Jane Austen"),
        ("To Kill a Mockingbird", "Harper Lee"),
        ("The Hobbit", "J.R.R. Tolkien"),
        ("The Great Gatsby", "F. Scott Fitzgerald"),
        ("Harry Potter and the Sorcerer’s Stone", "J.K. Rowling"),
        ("Moby Dick", "Herman Melville"),
        ("War and Peace", "Leo Tolstoy"),
        ("The Catcher in the Rye", "J.D. Salinger"),
        ("Brave New World", "Aldous Huxley"),
        ("Crime and Punishment", "Fyodor Dostoevsky"),
        ("The Lord of the Rings", "J.R.R. Tolkien"),
        ("Jane Eyre", "Charlotte Brontë"),
        ("The Chronicles of Narnia", "C.S. Lewis"),
        ("Animal Farm", "George Orwell"),
        ("Wuthering Heights", "Emily Brontë"),
        ("The Alchemist", "Paulo Coelho"),
        ("Les Misérables", "Victor Hugo"),
        ("Fahrenheit 451", "Ray Bradbury"),
        ("The Da Vinci Code", "Dan Brown"),
        ("The Kite Runner", "Khaled Hosseini"),
        ("The Shining", "Stephen King"),
        ("A Tale of Two Cities", "Charles Dickens"),
        ("Dracula", "Bram Stoker"),
        ("The Picture of Dorian Gray", "Oscar Wilde"),
        ("The Adventures of Sherlock Holmes", "Arthur Conan Doyle"),
        ("Life of Pi", "Yann Martel"),
        ("The Hunger Games", "Suzanne Collins"),
        ("The Fault in Our Stars", "John Green"),
        ("The Girl with the Dragon Tattoo", "Stieg Larsson")

        ]
        random.shuffle(sample_books)
        self.books = [Book(title, author, random.randint(10, 50), random.randint(5, 15))
                      for title, author in sample_books[:num_books]]

        self.customers = [Customer(f"Customer {i+1}", random.randint(50, 200)) for i in range(num_customers)]
        self.employees = [Employee(f"Employee {i+1}") for i in range(num_employees)]
        self.step_count = 0
        self.total_sales = 0
        self.total_revenue = 0
        self.total_restocks = 0

        # Reset history
        self.history_steps = []
        self.history_sales = []
        self.history_active_customers = []
        self.history_books_in_stock = []

    def step(self):
        with self.lock:
            self.step_count += 1
            for customer in self.customers:
                if not customer.active:
                    continue
                book = random.choice(self.books)
                if book.quantity > 0 and customer.budget >= book.price:
                    book.quantity -= 1
                    book.purchases += 1
                    customer.purchases += 1
                    customer.budget -= book.price
                    self.total_sales += 1
                    self.total_revenue += book.price
                if random.random() < 0.05:  # small chance to deactivate customer
                    customer.active = False

            for employee in self.employees:
                book = random.choice(self.books)
                restock_amount = random.randint(1, 5)
                book.quantity += restock_amount
                employee.restocks += 1
                self.total_restocks += 1

            # Update history for graphs
            self.history_steps.append(self.step_count)
            self.history_sales.append(self.total_sales)
            self.history_active_customers.append(sum(1 for c in self.customers if c.active))
            self.history_books_in_stock.append(sum(b.quantity for b in self.books))

    def get_stats(self):
        return {
        "step": self.step_count,
        "total_sales": self.total_sales,
        "total_revenue": round(self.total_revenue, 2),
        "active_customers": sum(1 for c in self.customers if c.active),
        "total_customers": len(self.customers),
        "books_in_stock": sum(1 for b in self.books if b.quantity > 0),  # ✅ distinct books available
        "total_books": len(self.books),
        "total_restocks": self.total_restocks
        }

    def get_books(self):
        return [{"title": b.title, "author": b.author, "price": b.price, "quantity": b.quantity, "purchases": b.purchases} for b in self.books]

    def get_customers(self):
        return [{"name": c.name, "budget": c.budget, "purchases": c.purchases, "active": c.active} for c in self.customers]

    def get_employees(self):
        return [{"name": e.name, "restocks": e.restocks} for e in self.employees]

    def start(self):
        self.running = True
        def run():
            while self.running:
                self.step()
                time.sleep(1)
        self.thread = threading.Thread(target=run)
        self.thread.start()

    def stop(self):
        self.running = False
        if hasattr(self, "thread"):
            self.thread.join()

    def get_history(self):
        return {
            "steps": self.history_steps,
            "sales": self.history_sales,
            "active_customers": self.history_active_customers,
            "books_in_stock": self.history_books_in_stock
        }
