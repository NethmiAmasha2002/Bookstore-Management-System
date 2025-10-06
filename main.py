"""
Bookstore Management System - Main Entry Point
Multi-Agent System with Ontology-based Knowledge Representation
"""

import os
import sys
from ontology.bookstore_ontology import BookstoreOntology
from simulation.model import BookstoreModel
from ui.dashboard import Dashboard
from ui.visualization import Visualization

def setup_environment():
    """Setup necessary directories"""
    directories = ['ontology', 'agents', 'simulation', 'ui', 'utils']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✓ Environment setup complete")

def print_banner():
    """Print application banner"""
    banner = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║         BOOKSTORE MANAGEMENT SYSTEM (BMS)                      ║
    ║         Ontology-Based Multi-Agent Simulation                  ║
    ║                                                                ║
    ║         Using: Owlready2 + Mesa Framework                      ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def run_simulation(num_steps=50, num_customers=10, num_employees=3, num_books=20):
    """Run the bookstore simulation"""
    
    print("\n" + "="*70)
    print("STEP 1: Creating Ontology")
    print("="*70)
    
    # Create ontology
    ontology = BookstoreOntology()
    print("✓ Ontology created successfully")
    
    print("\n" + "="*70)
    print("STEP 2: Initializing Multi-Agent System")
    print("="*70)
    
    # Create model
    model = BookstoreModel(
        ontology=ontology,
        num_customers=num_customers,
        num_employees=num_employees,
        num_books=num_books
    )
    print("✓ Multi-agent system initialized")
    
    # Create dashboard and visualization
    dashboard = Dashboard(model)
    visualization = Visualization(model)
    
    print("\n" + "="*70)
    print("STEP 3: Running Simulation")
    print("="*70)
    print(f"Running for {num_steps} steps...\n")
    
    # Run simulation
    try:
        for step in range(num_steps):
            model.step()
            
            # Display compact summary every 10 steps
            if (step + 1) % 10 == 0:
                print(f"\n{'─'*70}")
                dashboard.display_compact_summary()
                print(f"{'─'*70}\n")
        
        print("\n✓ Simulation completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⚠ Simulation interrupted by user")
    except Exception as e:
        print(f"\n\n✗ Error during simulation: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None, None
    
    print("\n" + "="*70)
    print("STEP 4: Saving Ontology")
    print("="*70)
    
    # Save final ontology state
    ontology.save()
    print("✓ Ontology saved to ontology/bookstore.owl")
    
    return model, dashboard, visualization

def display_results(model, dashboard, visualization):
    """Display simulation results and generate reports"""
    
    if model is None:
        print("No results to display")
        return
    
    print("\n" + "="*70)
    print("STEP 5: Generating Results and Reports")
    print("="*70)
    
    # Generate simulation summary
    model.generate_summary()
    
    # Display full dashboard
    print("\n" + "="*70)
    print("Detailed Dashboard")
    print("="*70)
    dashboard.display_full_dashboard()
    
    # Generate visualizations
    try:
        visualization.generate_all_plots()
    except Exception as e:
        print(f"⚠ Could not generate visualizations: {str(e)}")
        print("  (This may be due to missing display or matplotlib configuration)")

def inspect_ontology(ontology):
    """Inspect and display ontology contents"""
    
    print("\n" + "="*70)
    print("ONTOLOGY INSPECTION")
    print("="*70)
    
    books = ontology.get_all_books()
    customers = ontology.get_all_customers()
    employees = ontology.get_all_employees()
    
    print(f"\n📚 Total Books in Ontology: {len(books)}")
    print(f"👥 Total Customers in Ontology: {len(customers)}")
    print(f"👷 Total Employees in Ontology: {len(employees)}")
    
    # Display sample book details
    if books:
        print(f"\n{'Sample Book Details:':-^70}")
        sample_book = books[0]
        print(f"  Title: {sample_book.hasTitle[0] if sample_book.hasTitle else 'N/A'}")
        print(f"  ISBN: {sample_book.hasISBN[0] if sample_book.hasISBN else 'N/A'}")
        print(f"  Author: {sample_book.hasAuthor[0] if sample_book.hasAuthor else 'N/A'}")
        print(f"  Price: ${sample_book.hasPrice[0] if sample_book.hasPrice else 0:.2f}")
        print(f"  Quantity: {sample_book.availableQuantity[0] if sample_book.availableQuantity else 0}")
    
    # Display sample customer details
    if customers:
        print(f"\n{'Sample Customer Details:':-^70}")
        sample_customer = customers[0]
        print(f"  Name: {sample_customer.customerName[0] if sample_customer.customerName else 'N/A'}")
        print(f"  Budget: ${sample_customer.customerBudget[0] if sample_customer.customerBudget else 0:.2f}")
        print(f"  Purchases: {len(sample_customer.purchases) if hasattr(sample_customer, 'purchases') and sample_customer.purchases else 0}")
    
    print("="*70 + "\n")

def interactive_menu():
    """Display interactive menu for simulation control"""
    
    print("\n" + "="*70)
    print("SIMULATION CONFIGURATION")
    print("="*70)
    
    try:
        num_steps = int(input("Enter number of simulation steps (default 50): ") or "50")
        num_customers = int(input("Enter number of customers (default 10): ") or "10")
        num_employees = int(input("Enter number of employees (default 3): ") or "3")
        num_books = int(input("Enter number of books (default 20): ") or "20")
    except ValueError:
        print("Invalid input. Using default values.")
        num_steps, num_customers, num_employees, num_books = 50, 10, 3, 20
    
    return num_steps, num_customers, num_employees, num_books

def main():
    """Main entry point"""
    
    # Print banner
    print_banner()
    
    # Setup environment
    setup_environment()
    
    # Interactive configuration
    print("\nWould you like to configure simulation parameters? (y/n): ", end="")
    response = input().strip().lower()
    
    if response == 'y':
        num_steps, num_customers, num_employees, num_books = interactive_menu()
    else:
        # Default configuration
        num_steps = 50
        num_customers = 10
        num_employees = 3
        num_books = 20
        print("\nUsing default configuration:")
        print(f"  Steps: {num_steps}, Customers: {num_customers}, Employees: {num_employees}, Books: {num_books}")
    
    # Run simulation
    model, dashboard, visualization = run_simulation(
        num_steps=num_steps,
        num_customers=num_customers,
        num_employees=num_employees,
        num_books=num_books
    )
    
    if model is None:
        print("\n✗ Simulation failed to complete")
        sys.exit(1)
    
    # Display results
    display_results(model, dashboard, visualization)
    
    # Inspect ontology
    inspect_ontology(model.ontology)
    
    # Final message
    print("\n" + "="*70)
    print("✓ BOOKSTORE MANAGEMENT SYSTEM - EXECUTION COMPLETE")
    print("="*70)
    print("\nGenerated files:")
    print("  • ontology/bookstore.owl - Ontology file")
    print("  • simulation_metrics.png - Simulation metrics visualization")
    print("  • book_popularity.png - Book popularity analysis")
    print("  • customer_spending.png - Customer spending patterns")
    print("  • inventory_status.png - Current inventory status")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()