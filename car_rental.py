"""
Car Rental System - Main Module

A simple car rental management system for training purposes.
This module handles the core car rental operations.
"""

import csv
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class Car:
    """Represents a rental car."""

    def __init__(
        self,
        car_id: str,
        make: str,
        model: str,
        year: int,
        daily_rate: float,
        available: bool = True,
    ):
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.daily_rate = daily_rate
        self.available = available

    def __str__(self):
        status = "Available" if self.available else "Rented"
        return f"{self.year} {self.make} {self.model} (ID: {self.car_id}) - ${self.daily_rate}/day - {status}"


class Customer:
    """Represents a rental customer."""

    def __init__(self, customer_id: str, name: str, email: str, phone: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone

    def __str__(self):
        return f"Customer {self.customer_id}: {self.name} ({self.email})"


class Rental:
    """Represents a car rental transaction."""

    def __init__(
        self,
        rental_id: str,
        customer: Customer,
        car: Car,
        start_date: datetime,
        days: int,
    ):
        self.rental_id = rental_id
        self.customer = customer
        self.car = car
        self.start_date = start_date
        self.days = days
        self.end_date = start_date + timedelta(days=days)
        self.total_cost = car.daily_rate * days
        self.returned = False

    def __str__(self):
        return (
            f"Rental {self.rental_id}: {self.customer.name} renting "
            f"{self.car.make} {self.car.model} for {self.days} days "
            f"(${self.total_cost:.2f})"
        )


class CarRentalSystem:
    """Main car rental management system."""

    def __init__(self):
        self.cars: List[Car] = []
        self.customers: List[Customer] = []
        self.rentals: List[Rental] = []
        # Memory management: Retain completed rentals for this many days
        self.rental_retention_days = 30

    def add_car(self, car: Car) -> None:
        """Add a car to the fleet."""
        self.cars.append(car)

    def add_customer(self, customer: Customer) -> None:
        """Add a customer to the system."""
        self.customers.append(customer)

    def get_available_cars(self) -> List[Car]:
        """Get list of available cars."""
        return [car for car in self.cars if car.available]

    def find_car(self, car_id: str) -> Optional[Car]:
        """Find a car by ID."""
        for car in self.cars:
            if car.car_id == car_id:
                return car
        return None

    def find_customer(self, customer_id: str) -> Optional[Customer]:
        """Find a customer by ID."""
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer
        return None

    def rent_car(self, customer_id: str, car_id: str, days: int) -> Optional[Rental]:
        """Process a car rental."""
        customer = self.find_customer(customer_id)
        car = self.find_car(car_id)

        if not customer:
            print(f"Customer {customer_id} not found")
            return None

        if not car:
            print(f"Car {car_id} not found")
            return None

        if not car.available:
            print(f"Car {car_id} is not available")
            return None

        # Create rental
        rental_id = f"R{len(self.rentals) + 1:04d}"
        rental = Rental(rental_id, customer, car, datetime.now(), days)

        # Mark car as unavailable
        car.available = False

        # Add to rentals
        self.rentals.append(rental)

        print(f"Rental created: {rental}")
        return rental

    def cleanup_old_rentals(self) -> int:
        """
        Clean up old completed rentals to prevent memory leaks.
        
        Removes completed rentals that are older than the retention period
        to prevent unlimited memory growth from accumulating rental history.
        
        Returns:
            int: Number of old rentals removed
        """
        if not self.rentals:
            return 0
            
        current_time = datetime.now()
        cutoff_date = current_time - timedelta(days=self.rental_retention_days)
        
        # Count rentals before cleanup
        initial_count = len(self.rentals)
        
        # Keep only rentals that are either:
        # 1. Not returned yet (active rentals)
        # 2. Returned recently (within retention period)
        self.rentals = [
            rental for rental in self.rentals
            if not rental.returned or rental.end_date >= cutoff_date
        ]
        
        # Calculate how many were removed
        removed_count = initial_count - len(self.rentals)
        
        if removed_count > 0:
            print(f"Cleaned up {removed_count} old completed rental(s) to prevent memory leak")
        
        return removed_count

    def return_car(self, rental_id: str) -> bool:
        """
        Process a car return.
        
        This method handles returning a rented car and includes cleanup
        to prevent memory leaks from accumulating completed rentals.
        """
        for rental in self.rentals:
            if rental.rental_id == rental_id and not rental.returned:
                rental.returned = True
                rental.car.available = True
                print(f"Car returned: {rental}")
                
                # Trigger cleanup of old completed rentals to prevent memory leak
                # This ensures that the rentals list doesn't grow indefinitely
                self.cleanup_old_rentals()
                
                return True

        print(f"Rental {rental_id} not found or already returned")
        return False

    def get_rental_summary(self) -> Dict:
        """Get rental system summary."""
        active_rentals = [r for r in self.rentals if not r.returned]
        total_revenue = sum(r.total_cost for r in self.rentals if r.returned)

        return {
            "total_cars": len(self.cars),
            "available_cars": len(self.get_available_cars()),
            "total_customers": len(self.customers),
            "active_rentals": len(active_rentals),
            "completed_rentals": len([r for r in self.rentals if r.returned]),
            "total_revenue": total_revenue,
        }

    def load_sample_data(self):
        """Load sample cars and customers for demonstration."""
        # Sample cars
        sample_cars = [
            Car("C001", "Toyota", "Camry", 2022, 45.00),
            Car("C002", "Honda", "Civic", 2021, 40.00),
            Car("C003", "Ford", "Mustang", 2023, 75.00),
            Car("C004", "Chevrolet", "Malibu", 2022, 50.00),
            Car("C005", "Nissan", "Altima", 2021, 42.00),
        ]

        for car in sample_cars:
            self.add_car(car)

        # Sample customers
        sample_customers = [
            Customer("CUST001", "John Smith", "john.smith@email.com", "555-0101"),
            Customer("CUST002", "Jane Doe", "jane.doe@email.com", "555-0102"),
            Customer("CUST003", "Bob Johnson", "bob.johnson@email.com", "555-0103"),
            Customer("CUST004", "Alice Brown", "alice.brown@email.com", "555-0104"),
        ]

        for customer in sample_customers:
            self.add_customer(customer)


def main():
    """Main function to demonstrate the car rental system."""
    print("=== Car Rental System Demo ===")

    # Initialize system
    rental_system = CarRentalSystem()
    rental_system.load_sample_data()

    # Show available cars
    print("\nAvailable Cars:")
    for car in rental_system.get_available_cars():
        print(f"  {car}")

    # Demo rental
    print("\n--- Demo Rental ---")
    rental = rental_system.rent_car("CUST001", "C001", 3)

    # Show updated available cars
    print("\nAvailable Cars After Rental:")
    for car in rental_system.get_available_cars():
        print(f"  {car}")

    # Show summary
    print("\nRental System Summary:")
    summary = rental_system.get_rental_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
