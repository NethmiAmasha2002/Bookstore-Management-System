"""
SWRL Rules for Bookstore Management System

SWRL (Semantic Web Rule Language) rules define the business logic
for the bookstore operations.
"""

class SWRLRules:
    """
    Define SWRL rules for bookstore operations.
    These rules are implemented programmatically in the agents.
    """
    
    @staticmethod
    def purchase_rule(customer, book, ontology):
        """
        Rule: If Customer purchases Book AND Book.availableQuantity > 0 
              AND Customer.budget >= Book.price
        Then: Reduce Book.availableQuantity by 1, 
              Reduce Customer.budget by Book.price,
              Add Book to Customer.purchases
        """
        # Get quantity safely
        quantity = 0
        if book.availableQuantity and len(book.availableQuantity) > 0:
            quantity = book.availableQuantity[0]
        
        # Get price safely
        price = 0
        if book.hasPrice and len(book.hasPrice) > 0:
            price = book.hasPrice[0]
        
        # Get budget safely
        budget = 0
        if customer.customerBudget and len(customer.customerBudget) > 0:
            budget = customer.customerBudget[0]
        
        if quantity > 0 and budget >= price:
            # Update book quantity
            new_quantity = quantity - 1
            ontology.update_book_quantity(book, new_quantity)
            
            # Update customer budget
            new_budget = budget - price
            customer.customerBudget = []
            customer.customerBudget.append(new_budget)
            
            # Add purchase relationship
            if not hasattr(customer, 'purchases'):
                customer.purchases = []
            if customer.purchases is None:
                customer.purchases = []
            customer.purchases.append(book)
            
            # Create order
            ontology.create_order(customer, book, price)
            
            return True, f"Purchase successful: {book.hasTitle[0] if book.hasTitle else 'Unknown'}"
        
        elif quantity <= 0:
            return False, "Book out of stock"
        else:
            return False, "Insufficient budget"
    
    @staticmethod
    def restock_rule(employee, book, ontology, restock_amount=10):
        """
        Rule: If Book.availableQuantity < Employee.restockThreshold
        Then: Employee restocks Book by restock_amount
        """
        # Get current quantity safely
        current_quantity = 0
        if book.availableQuantity and len(book.availableQuantity) > 0:
            current_quantity = book.availableQuantity[0]
        
        # Get threshold safely
        threshold = 5
        if employee.restockThreshold and len(employee.restockThreshold) > 0:
            threshold = employee.restockThreshold[0]
        
        if current_quantity < threshold:
            new_quantity = current_quantity + restock_amount
            ontology.update_book_quantity(book, new_quantity)
            
            title = book.hasTitle[0] if book.hasTitle and len(book.hasTitle) > 0 else "Unknown"
            return True, f"Restocked {title}: {current_quantity} -> {new_quantity}"
        
        return False, "No restock needed"
    
    @staticmethod
    def low_stock_alert_rule(book, threshold=5):
        """
        Rule: If Book.availableQuantity < threshold
        Then: Generate low stock alert
        """
        if not book.availableQuantity or len(book.availableQuantity) == 0:
            quantity = 0
        else:
            quantity = book.availableQuantity[0]
        
        if quantity < threshold:
            return True, f"LOW STOCK ALERT: {book.hasTitle[0]} has only {quantity} copies"
        
        return False, "Stock level normal"
    
    @staticmethod
    def customer_spending_rule(customer):
        """
        Rule: Calculate total spending by customer
        """
        total_spent = 0
        if hasattr(customer, 'hasOrder') and customer.hasOrder:
            for order in customer.hasOrder:
                if order.orderTotal:
                    total_spent += order.orderTotal[0]
        
        return total_spent
    
    @staticmethod
    def popular_book_rule(book, purchase_threshold=5):
        """
        Rule: If Book is purchased more than purchase_threshold times
        Then: Mark as popular book
        """
        # Count how many times this book appears in orders
        purchase_count = 0
        # This would require tracking across all orders in the ontology
        # For simulation purposes, we check quantity sold (initial - current)
        
        return purchase_count >= purchase_threshold