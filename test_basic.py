#!/usr/bin/env python3
"""
Basic tests for the car rental system outline.
"""

import sys
import unittest
from basic_rental import Car, Customer, CarRentalSystem


class TestBasicCarRentalSystem(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.system = CarRentalSystem()
        self.car = Car("C001", "Toyota", "Camry")
        self.customer = Customer("CUST001", "John Smith")

    def test_car_creation(self):
        """Test car object creation."""
        self.assertEqual(self.car.car_id, "C001")
        self.assertEqual(self.car.make, "Toyota")
        self.assertEqual(self.car.model, "Camry")
        self.assertTrue(self.car.available)

    def test_customer_creation(self):
        """Test customer object creation."""
        self.assertEqual(self.customer.customer_id, "CUST001")
        self.assertEqual(self.customer.name, "John Smith")

    def test_add_car(self):
        """Test adding a car to the system."""
        self.system.add_car(self.car)
        self.assertEqual(len(self.system.cars), 1)
        self.assertIn(self.car, self.system.cars)

    def test_add_customer(self):
        """Test adding a customer to the system."""
        self.system.add_customer(self.customer)
        self.assertEqual(len(self.system.customers), 1)
        self.assertIn(self.customer, self.system.customers)

    def test_successful_rental(self):
        """Test successful car rental."""
        self.system.add_car(self.car)
        self.system.add_customer(self.customer)

        result = self.system.rent_car("CUST001", "C001")

        self.assertTrue(result)
        self.assertFalse(self.car.available)
        self.assertEqual(len(self.system.rentals), 1)

    def test_failed_rental_nonexistent_customer(self):
        """Test rental failure with nonexistent customer."""
        self.system.add_car(self.car)

        result = self.system.rent_car("INVALID", "C001")

        self.assertFalse(result)
        self.assertTrue(self.car.available)
        self.assertEqual(len(self.system.rentals), 0)

    def test_failed_rental_unavailable_car(self):
        """Test rental failure with unavailable car."""
        self.car.available = False
        self.system.add_car(self.car)
        self.system.add_customer(self.customer)

        result = self.system.rent_car("CUST001", "C001")

        self.assertFalse(result)
        self.assertEqual(len(self.system.rentals), 0)

    def test_list_available_cars(self):
        """Test listing available cars."""
        car1 = Car("C001", "Toyota", "Camry", True)
        car2 = Car("C002", "Honda", "Civic", False)

        self.system.add_car(car1)
        self.system.add_car(car2)

        available = self.system.list_available_cars()

        self.assertEqual(len(available), 1)
        self.assertIn(car1, available)
        self.assertNotIn(car2, available)


def main():
    """Run the tests."""
    print("Running basic car rental system tests...")
    unittest.main(verbosity=2)  # type: ignore[no-untyped-call]


if __name__ == "__main__":
    main()
