# HERZZ - Basic Car Rental System Outline

A minimal implementation demonstrating the core concepts of a car rental management system.

## Overview

This basic outline provides the fundamental building blocks for a car rental system:

- **Car**: Basic car representation with ID, make, model, and availability status
- **Customer**: Simple customer with ID and name
- **CarRentalSystem**: Core system for managing cars, customers, and rentals

## Features

- Add cars to the fleet
- Register customers  
- Process simple car rentals
- Track car availability
- List available cars

## Usage

```bash
# Run the basic demo
python basic_rental.py
```

## Basic API

```python
# Create system
rental_system = CarRentalSystem()

# Add cars and customers
rental_system.add_car(Car("C001", "Toyota", "Camry"))
rental_system.add_customer(Customer("CUST001", "John Smith"))

# Process rental
rental_system.rent_car("CUST001", "C001")

# List available cars
rental_system.list_available_cars()
```

## Implementation Details

This is intentionally kept minimal (~80 lines) to serve as a basic outline that can be extended with more sophisticated features like:

- Advanced pricing models
- Rental duration tracking
- Return processing
- Data persistence
- Detailed reporting
- Error handling
- Input validation

The goal is to provide a clean foundation that demonstrates the core concepts while remaining simple and easy to understand.