#!/usr/bin/env python3
"""
Basic Car Rental System Outline

A minimal implementation demonstrating the core concepts
of a car rental management system.
"""


class Car:
    """Basic car representation."""
    
    def __init__(self, car_id, make, model, available=True):
        self.car_id = car_id
        self.make = make
        self.model = model
        self.available = available
    
    def __str__(self):
        status = "Available" if self.available else "Rented"
        return f"{self.make} {self.model} ({self.car_id}) - {status}"


class Customer:
    """Basic customer representation."""
    
    def __init__(self, customer_id, name):
        self.customer_id = customer_id
        self.name = name
    
    def __str__(self):
        return f"{self.name} ({self.customer_id})"


class CarRentalSystem:
    """Basic car rental management system."""
    
    def __init__(self):
        self.cars = []
        self.customers = []
        self.rentals = []
    
    def add_car(self, car):
        """Add a car to the fleet."""
        self.cars.append(car)
    
    def add_customer(self, customer):
        """Add a customer to the system."""
        self.customers.append(customer)
    
    def rent_car(self, customer_id, car_id):
        """Process a simple car rental."""
        # Find customer and car
        customer = next((c for c in self.customers if c.customer_id == customer_id), None)
        car = next((c for c in self.cars if c.car_id == car_id), None)
        
        if not customer or not car or not car.available:
            return False
        
        # Process rental
        car.available = False
        rental = {"customer": customer, "car": car}
        self.rentals.append(rental)
        
        print(f"Rental successful: {customer.name} rented {car.make} {car.model}")
        return True
    
    def list_available_cars(self):
        """List all available cars."""
        available = [car for car in self.cars if car.available]
        if available:
            print("Available cars:")
            for car in available:
                print(f"  {car}")
        else:
            print("No cars available")
        return available


def main():
    """Demonstrate the basic car rental system."""
    print("=== Basic Car Rental System Demo ===")
    
    # Create system
    rental_system = CarRentalSystem()
    
    # Add some cars
    rental_system.add_car(Car("C001", "Toyota", "Camry"))
    rental_system.add_car(Car("C002", "Honda", "Civic"))
    rental_system.add_car(Car("C003", "Ford", "Focus"))
    
    # Add some customers
    rental_system.add_customer(Customer("CUST001", "John Smith"))
    rental_system.add_customer(Customer("CUST002", "Jane Doe"))
    
    # Show available cars
    rental_system.list_available_cars()
    
    # Process a rental
    print("\nProcessing rental...")
    rental_system.rent_car("CUST001", "C001")
    
    # Show updated availability
    print("\nAfter rental:")
    rental_system.list_available_cars()
    
    print(f"\nTotal rentals processed: {len(rental_system.rentals)}")


if __name__ == "__main__":
    main()