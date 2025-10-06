from mesa import Agent

class BookAgent(Agent):
    def __init__(self, unique_id, model, title, author, price, quantity):
        super().__init__(unique_id, model)
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity
        self.times_purchased = 0
        self.revenue_generated = 0

    def sell(self):
        if self.quantity > 0:
            self.quantity -= 1
            self.times_purchased += 1
            self.revenue_generated += self.price
            return True
        return False

    def step(self):
        # Books themselves don’t act
        pass
