from mesa import Agent
from agents.book_agent import BookAgent
import random

class CustomerAgent(Agent):
    def __init__(self, unique_id, model, name, budget):
        super().__init__(unique_id, model)
        self.name = name
        self.budget = budget
        self.purchases_made = []
        self.active = True

    def get_total_spent(self):
        return sum(p["price"] for p in self.purchases_made)
def step(self):
    if not self.active:
        return

    # Only choose books that still have stock
    books = [a for a in self.model.schedule.agents if isinstance(a, BookAgent) and a.quantity > 0]

    # If no books or none affordable → stop being active
    affordable_books = [b for b in books if b.price <= self.budget]
    if not affordable_books:
        self.active = False
        return

    book = random.choice(affordable_books)
    self.budget -= book.price
    self.purchases_made.append({
        "title": book.title,
        "price": book.price
    })
    book.sell()

       