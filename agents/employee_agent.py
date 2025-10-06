from mesa import Agent
from agents.book_agent import BookAgent
import random

class EmployeeAgent(Agent):
    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model)
        self.name = name
        self.restocks_performed = 0

    def step(self):
        books = [a for a in self.model.schedule.agents if isinstance(a, BookAgent)]
        if not books:
            return

        # Choose a random book that is out of stock
        out_of_stock = [b for b in books if b.quantity == 0]
        if out_of_stock:
            book = random.choice(out_of_stock)
            restock_amount = random.randint(5, 15)
            book.quantity += restock_amount
            self.restocks_performed += 1
