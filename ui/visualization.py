import matplotlib.pyplot as plt
import pandas as pd
from agents.customer_agent import CustomerAgent
from agents.employee_agent import EmployeeAgent
from agents.book_agent import BookAgent

class Visualization:
    """Visualization utilities for the bookstore simulation"""
    
    def __init__(self, model):
        self.model = model
    
    def plot_simulation_metrics(self):
        """Plot key simulation metrics over time"""
        # Get data from datacollector
        data = self.model.datacollector.get_model_vars_dataframe()
        
        if data.empty:
            print("No data to plot")
            return
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Bookstore Simulation Metrics', fontsize=16, fontweight='bold')
        
        # Plot 1: Total Sales
        axes[0, 0].plot(data.index, data['Total_Sales'], marker='o', color='green', linewidth=2)
        axes[0, 0].set_title('Total Sales Over Time')
        axes[0, 0].set_xlabel('Step')
        axes[0, 0].set_ylabel('Number of Sales')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Total Restocks
        axes[0, 1].plot(data.index, data['Total_Restocks'], marker='s', color='blue', linewidth=2)
        axes[0, 1].set_title('Total Restocks Over Time')
        axes[0, 1].set_xlabel('Step')
        axes[0, 1].set_ylabel('Number of Restocks')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Active Customers
        axes[0, 2].plot(data.index, data['Active_Customers'], marker='^', color='orange', linewidth=2)
        axes[0, 2].set_title('Active Customers Over Time')
        axes[0, 2].set_xlabel('Step')
        axes[0, 2].set_ylabel('Number of Customers')
        axes[0, 2].grid(True, alpha=0.3)
        
        # Plot 4: Books In Stock
        axes[1, 0].plot(data.index, data['Books_In_Stock'], marker='d', color='purple', linewidth=2)
        axes[1, 0].set_title('Books In Stock Over Time')
        axes[1, 0].set_xlabel('Step')
        axes[1, 0].set_ylabel('Number of Books')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 5: Out of Stock Books
        axes[1, 1].plot(data.index, data['Out_Of_Stock_Books'], marker='x', color='red', linewidth=2)
        axes[1, 1].set_title('Out of Stock Books Over Time')
        axes[1, 1].set_xlabel('Step')
        axes[1, 1].set_ylabel('Number of Books')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Plot 6: Total Messages
        axes[1, 2].plot(data.index, data['Total_Messages'], marker='*', color='teal', linewidth=2)
        axes[1, 2].set_title('Total Messages Over Time')
        axes[1, 2].set_xlabel('Step')
        axes[1, 2].set_ylabel('Number of Messages')
        axes[1, 2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('simulation_metrics.png', dpi=300, bbox_inches='tight')
        print("\n✓ Simulation metrics plot saved as 'simulation_metrics.png'")
        plt.show()
    
    def plot_book_popularity(self):
        """Plot book popularity based on purchases"""
        book_data = []
        
        for agent in self.model.schedule.agents:
            if isinstance(agent, BookAgent):
                book_data.append({
                    'title': agent.title[:20] + '...' if len(agent.title) > 20 else agent.title,
                    'purchases': agent.times_purchased,
                    'revenue': agent.revenue_generated
                })
        
        if not book_data:
            print("No book data available")
            return
        
        df = pd.DataFrame(book_data)
        df = df.sort_values('purchases', ascending=False).head(10)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Top 10 Books Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Purchases
        axes[0].barh(df['title'], df['purchases'], color='skyblue')
        axes[0].set_xlabel('Number of Purchases')
        axes[0].set_title('Most Purchased Books')
        axes[0].grid(True, alpha=0.3, axis='x')
        
        # Plot 2: Revenue
        axes[1].barh(df['title'], df['revenue'], color='lightcoral')
        axes[1].set_xlabel('Revenue Generated ($)')
        axes[1].set_title('Highest Revenue Books')
        axes[1].grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        plt.savefig('book_popularity.png', dpi=300, bbox_inches='tight')
        print("✓ Book popularity plot saved as 'book_popularity.png'")
        plt.show()
    
    def plot_customer_spending(self):
        """Plot customer spending patterns"""
        customer_data = []
        
        for agent in self.model.schedule.agents:
            if isinstance(agent, CustomerAgent):
                customer_data.append({
                    'name': agent.name,
                    'purchases': len(agent.purchases_made),
                    'spent': agent.get_total_spent(),
                    'remaining_budget': agent.budget
                })
        
        if not customer_data:
            print("No customer data available")
            return
        
        df = pd.DataFrame(customer_data)
        df = df.sort_values('spent', ascending=False)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Customer Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Customer Purchases
        axes[0].bar(range(len(df)), df['purchases'], color='mediumseagreen')
        axes[0].set_xlabel('Customer')
        axes[0].set_ylabel('Number of Purchases')
        axes[0].set_title('Purchases per Customer')
        axes[0].set_xticks(range(len(df)))
        axes[0].set_xticklabels(df['name'], rotation=45, ha='right')
        axes[0].grid(True, alpha=0.3, axis='y')
        
        # Plot 2: Customer Spending
        axes[1].bar(range(len(df)), df['spent'], color='coral')
        axes[1].set_xlabel('Customer')
        axes[1].set_ylabel('Amount Spent ($)')
        axes[1].set_title('Spending per Customer')
        axes[1].set_xticks(range(len(df)))
        axes[1].set_xticklabels(df['name'], rotation=45, ha='right')
        axes[1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('customer_spending.png', dpi=300, bbox_inches='tight')
        print("✓ Customer spending plot saved as 'customer_spending.png'")
        plt.show()
    
    def plot_inventory_status(self):
        """Plot current inventory status"""
        inventory_data = {
            'In Stock': 0,
            'Low Stock': 0,
            'Out of Stock': 0
        }
        
        for agent in self.model.schedule.agents:
            if isinstance(agent, BookAgent):
                if agent.quantity == 0:
                    inventory_data['Out of Stock'] += 1
                elif agent.quantity < 5:
                    inventory_data['Low Stock'] += 1
                else:
                    inventory_data['In Stock'] += 1
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(8, 8))
        colors = ['#90EE90', '#FFD700', '#FF6B6B']
        explode = (0.05, 0.05, 0.1)
        
        ax.pie(inventory_data.values(), labels=inventory_data.keys(), autopct='%1.1f%%',
               colors=colors, explode=explode, startangle=90, textprops={'fontsize': 12})
        ax.set_title('Current Inventory Status', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('inventory_status.png', dpi=300, bbox_inches='tight')
        print("✓ Inventory status plot saved as 'inventory_status.png'")
        plt.show()
    
    def generate_all_plots(self):
        """Generate all visualization plots"""
        print("\n" + "="*60)
        print("Generating Visualizations...")
        print("="*60)
        
        self.plot_simulation_metrics()
        self.plot_book_popularity()
        self.plot_customer_spending()
        self.plot_inventory_status()
        
        print("\n✓ All visualizations generated successfully!")
        print("="*60 + "\n")