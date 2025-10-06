from agents.customer_agent import CustomerAgent
from agents.employee_agent import EmployeeAgent
from agents.book_agent import BookAgent

class Dashboard:
    """Dashboard for displaying simulation statistics and reports"""
    
    def __init__(self, model):
        self.model = model
    
    def display_header(self):
        """Display dashboard header"""
        print("\n" + "="*80)
        print(" " * 25 + "BOOKSTORE MANAGEMENT SYSTEM")
        print(" " * 30 + "Live Dashboard")
        print("="*80 + "\n")
    
    def display_overview(self):
        """Display system overview"""
        self.display_header()
        
        total_books = sum(1 for agent in self.model.schedule.agents if isinstance(agent, BookAgent))
        total_customers = sum(1 for agent in self.model.schedule.agents if isinstance(agent, CustomerAgent))
        total_employees = sum(1 for agent in self.model.schedule.agents if isinstance(agent, EmployeeAgent))
        
        print(f"{'System Overview':-^80}")
        print(f"  Current Step: {self.model.current_step}")
        print(f"  Total Books: {total_books}")
        print(f"  Total Customers: {total_customers}")
        print(f"  Total Employees: {total_employees}")
        print(f"  Total Messages: {self.model.message_bus.get_message_count()}")
        print("="*80 + "\n")
    
    def display_book_inventory(self):
        """Display detailed book inventory"""
        print(f"{'Book Inventory':-^80}")
        print(f"{'Title':<30} {'ISBN':<15} {'Qty':<8} {'Price':<10} {'Sold':<8}")
        print("-"*80)
        
        for agent in self.model.schedule.agents:
            if isinstance(agent, BookAgent):
                status = "✓" if agent.quantity > 5 else "⚠" if agent.quantity > 0 else "✗"
                print(f"{status} {agent.title[:28]:<28} {agent.isbn:<15} {agent.quantity:<8} "
                      f"${agent.price:<9.2f} {agent.times_purchased:<8}")
        
        print("="*80 + "\n")
    
    def display_customer_activity(self):
        """Display customer activity"""
        print(f"{'Customer Activity':-^80}")
        print(f"{'Name':<20} {'Budget':<15} {'Purchases':<12} {'Status':<15}")
        print("-"*80)
        
        for agent in self.model.schedule.agents:
            if isinstance(agent, CustomerAgent):
                status = "Active" if agent.active else "Inactive"
                print(f"{agent.name:<20} ${agent.budget:<14.2f} {len(agent.purchases_made):<12} {status:<15}")
        
        print("="*80 + "\n")
    
    def display_employee_performance(self):
        """Display employee performance"""
        print(f"{'Employee Performance':-^80}")
        print(f"{'Name':<30} {'Restocks Performed':<20}")
        print("-"*80)
        
        for agent in self.model.schedule.agents:
            if isinstance(agent, EmployeeAgent):
                print(f"{agent.name:<30} {agent.restocks_performed:<20}")
        
        print("="*80 + "\n")
    
    def display_top_books(self, limit=5):
        """Display top selling books"""
        print(f"{'Top Selling Books':-^80}")
        
        book_agents = [agent for agent in self.model.schedule.agents if isinstance(agent, BookAgent)]
        sorted_books = sorted(book_agents, key=lambda x: x.times_purchased, reverse=True)[:limit]
        
        print(f"{'Rank':<8} {'Title':<35} {'Purchases':<12} {'Revenue':<15}")
        print("-"*80)
        
        for idx, agent in enumerate(sorted_books, 1):
            print(f"{idx:<8} {agent.title[:33]:<35} {agent.times_purchased:<12} "
                  f"${agent.revenue_generated:<14.2f}")
        
        print("="*80 + "\n")
    
    def display_financial_summary(self):
        """Display financial summary"""
        print(f"{'Financial Summary':-^80}")
        
        total_revenue = 0
        total_purchases = 0
        
        for agent in self.model.schedule.agents:
            if isinstance(agent, BookAgent):
                total_revenue += agent.revenue_generated
                total_purchases += agent.times_purchased
        
        avg_transaction = total_revenue / total_purchases if total_purchases > 0 else 0
        
        print(f"  Total Revenue: ${total_revenue:.2f}")
        print(f"  Total Transactions: {total_purchases}")
        print(f"  Average Transaction Value: ${avg_transaction:.2f}")
        print("="*80 + "\n")
    
    def display_message_statistics(self):
        """Display message bus statistics"""
        print(f"{'Message Bus Statistics':-^80}")
        
        stats = self.model.message_bus.get_message_statistics()
        
        print(f"  Total Messages: {stats['total_messages']}")
        print(f"\n  Messages by Type:")
        for msg_type, count in stats['by_type'].items():
            print(f"    {msg_type}: {count}")
        
        print("="*80 + "\n")
    
    def display_stock_alerts(self):
        """Display stock alerts"""
        print(f"{'Stock Alerts':-^80}")
        
        low_stock = []
        out_of_stock = []
        
        for agent in self.model.schedule.agents:
            if isinstance(agent, BookAgent):
                if agent.quantity == 0:
                    out_of_stock.append(agent.title)
                elif agent.quantity < 5:
                    low_stock.append(f"{agent.title} ({agent.quantity} left)")
        
        if out_of_stock:
            print(f"  ⚠ OUT OF STOCK ({len(out_of_stock)}):")
            for book in out_of_stock[:5]:
                print(f"    • {book}")
        
        if low_stock:
            print(f"\n  ⚠ LOW STOCK ({len(low_stock)}):")
            for book in low_stock[:5]:
                print(f"    • {book}")
        
        if not out_of_stock and not low_stock:
            print("  ✓ All books are adequately stocked")
        
        print("="*80 + "\n")
    
    def display_full_dashboard(self):
        """Display complete dashboard"""
        self.display_overview()
        self.display_financial_summary()
        self.display_top_books()
        self.display_stock_alerts()
        self.display_customer_activity()
        self.display_employee_performance()
        self.display_message_statistics()
    
    def display_compact_summary(self):
        """Display compact summary for step updates"""
        sales = self.model.get_total_sales()
        restocks = self.model.get_total_restocks()
        active = self.model.get_active_customers()
        in_stock = self.model.get_books_in_stock()
        
        print(f"Step {self.model.current_step}: Sales={sales}, Restocks={restocks}, "
              f"Active Customers={active}, Books In Stock={in_stock}")