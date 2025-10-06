class BookstoreOntology:
    def __init__(self):
        self.books = []
        self.customers = []
        self.employees = []

    def add_book(self, isbn, title, author, genre, price, quantity):
        book = {
            "isbn": isbn,
            "title": title,
            "author": author,
            "genre": genre,
            "price": price,
            "quantity": quantity
        }
        self.books.append(book)
        return book

    def add_customer(self, name, budget):
        customer = {
            "name": name,
            "budget": budget
        }
        self.customers.append(customer)
        return customer

    def add_employee(self, name):
        employee = {
            "name": name
        }
        self.employees.append(employee)
        return employee
