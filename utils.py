"""
Utility functions for the car rental system.
"""

import csv
import json
from typing import Dict, List

from car_rental import Car, CarRentalSystem, Customer


def save_cars_to_json(cars: List[Car], filename: str) -> None:
    """Save cars data to JSON file."""
    cars_data = []
    for car in cars:
        cars_data.append(
            {
                "car_id": car.car_id,
                "make": car.make,
                "model": car.model,
                "year": car.year,
                "daily_rate": car.daily_rate,
                "available": car.available,
            }
        )

    with open(filename, "w") as f:
        json.dump(cars_data, f, indent=2)


def load_cars_from_json(filename: str) -> List[Car]:
    """Load cars data from JSON file."""
    cars = []
    try:
        with open(filename, "r") as f:
            cars_data = json.load(f)

        for car_data in cars_data:
            car = Car(
                car_data["car_id"],
                car_data["make"],
                car_data["model"],
                car_data["year"],
                car_data["daily_rate"],
                car_data["available"],
            )
            cars.append(car)
    except FileNotFoundError:
        print(f"File {filename} not found")

    return cars


def save_customers_to_csv(customers: List[Customer], filename: str) -> None:
    """Save customers data to CSV file."""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["customer_id", "name", "email", "phone"])

        for customer in customers:
            writer.writerow(
                [customer.customer_id, customer.name, customer.email, customer.phone]
            )


def load_customers_from_csv(filename: str) -> List[Customer]:
    """Load customers data from CSV file."""
    customers = []
    try:
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                customer = Customer(
                    row["customer_id"], row["name"], row["email"], row["phone"]
                )
                customers.append(customer)
    except FileNotFoundError:
        print(f"File {filename} not found")

    return customers


def generate_report(rental_system: CarRentalSystem) -> str:
    """Generate a comprehensive rental report."""
    summary = rental_system.get_rental_summary()

    report = ["=== CAR RENTAL SYSTEM REPORT ===\n"]

    # Summary statistics
    report.append("SUMMARY STATISTICS:")
    report.append(f"  Total Cars in Fleet: {summary['total_cars']}")
    report.append(f"  Available Cars: {summary['available_cars']}")
    report.append(
        f"  Cars Currently Rented: {summary['total_cars'] - summary['available_cars']}"
    )
    report.append(f"  Total Customers: {summary['total_customers']}")
    report.append(f"  Active Rentals: {summary['active_rentals']}")
    report.append(f"  Completed Rentals: {summary['completed_rentals']}")
    report.append(f"  Total Revenue: ${summary['total_revenue']:.2f}\n")

    # Available cars
    report.append("AVAILABLE CARS:")
    available_cars = rental_system.get_available_cars()
    if available_cars:
        for car in available_cars:
            report.append(f"  {car}")
    else:
        report.append("  No cars currently available")

    report.append("")

    # Active rentals
    report.append("ACTIVE RENTALS:")
    active_rentals = [r for r in rental_system.rentals if not r.returned]
    if active_rentals:
        for rental in active_rentals:
            report.append(f"  {rental}")
    else:
        report.append("  No active rentals")

    return "\n".join(report)


def validate_car_data(car_data: Dict) -> bool:
    """Validate car data format."""
    required_fields = ["car_id", "make", "model", "year", "daily_rate"]

    for field in required_fields:
        if field not in car_data:
            return False

    if not isinstance(car_data["year"], int) or car_data["year"] < 1900:
        return False

    if (
        not isinstance(car_data["daily_rate"], (int, float))
        or car_data["daily_rate"] <= 0
    ):
        return False

    return True


def validate_customer_data(customer_data: Dict) -> bool:
    """Validate customer data format."""
    required_fields = ["customer_id", "name", "email", "phone"]

    for field in required_fields:
        if field not in customer_data:
            return False
        if not customer_data[field] or not isinstance(customer_data[field], str):
            return False

    # Basic email validation
    if "@" not in customer_data["email"] or "." not in customer_data["email"]:
        return False

    return True


def calculate_inventory_utilization(rental_system: CarRentalSystem) -> float:
    """Calculate the utilization rate of the car inventory."""
    total_cars = len(rental_system.cars)
    
    # INTENTIONAL BUG: Division by zero when no cars in system
    # Missing check for total_cars == 0
    
    available_cars = len(rental_system.get_available_cars())
    rented_cars = total_cars - available_cars
    
    # This will cause ZeroDivisionError when total_cars is 0
    utilization_rate = (rented_cars / total_cars) * 100
    return utilization_rate
