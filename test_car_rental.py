"""
Basic tests for the car rental system.
"""

import unittest
from datetime import datetime, timedelta

from car_rental import Car, CarRentalSystem, Customer, Rental
from utils import validate_car_data, validate_customer_data


class TestCarRentalSystem(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.rental_system = CarRentalSystem()
        self.car = Car("C001", "Toyota", "Camry", 2022, 45.00)
        self.customer = Customer(
            "CUST001", "John Smith", "john.smith@email.com", "555-0101"
        )

    def test_car_creation(self):
        """Test car object creation."""
        self.assertEqual(self.car.car_id, "C001")
        self.assertEqual(self.car.make, "Toyota")
        self.assertEqual(self.car.model, "Camry")
        self.assertEqual(self.car.year, 2022)
        self.assertEqual(self.car.daily_rate, 45.00)
        self.assertTrue(self.car.available)

    def test_customer_creation(self):
        """Test customer object creation."""
        self.assertEqual(self.customer.customer_id, "CUST001")
        self.assertEqual(self.customer.name, "John Smith")
        self.assertEqual(self.customer.email, "john.smith@email.com")
        self.assertEqual(self.customer.phone, "555-0101")

    def test_add_car(self):
        """Test adding a car to the system."""
        self.rental_system.add_car(self.car)
        self.assertEqual(len(self.rental_system.cars), 1)
        self.assertEqual(self.rental_system.cars[0], self.car)

    def test_add_customer(self):
        """Test adding a customer to the system."""
        self.rental_system.add_customer(self.customer)
        self.assertEqual(len(self.rental_system.customers), 1)
        self.assertEqual(self.rental_system.customers[0], self.customer)

    def test_find_car(self):
        """Test finding a car by ID."""
        self.rental_system.add_car(self.car)
        found_car = self.rental_system.find_car("C001")
        self.assertEqual(found_car, self.car)

        not_found = self.rental_system.find_car("C999")
        self.assertIsNone(not_found)

    def test_find_customer(self):
        """Test finding a customer by ID."""
        self.rental_system.add_customer(self.customer)
        found_customer = self.rental_system.find_customer("CUST001")
        self.assertEqual(found_customer, self.customer)

        not_found = self.rental_system.find_customer("CUST999")
        self.assertIsNone(not_found)

    def test_available_cars(self):
        """Test getting available cars."""
        car1 = Car("C001", "Toyota", "Camry", 2022, 45.00, True)
        car2 = Car("C002", "Honda", "Civic", 2021, 40.00, False)

        self.rental_system.add_car(car1)
        self.rental_system.add_car(car2)

        available = self.rental_system.get_available_cars()
        self.assertEqual(len(available), 1)
        self.assertEqual(available[0], car1)

    def test_rent_car(self):
        """Test car rental process."""
        self.rental_system.add_car(self.car)
        self.rental_system.add_customer(self.customer)

        rental = self.rental_system.rent_car("CUST001", "C001", 3)

        self.assertIsNotNone(rental)
        self.assertEqual(rental.customer, self.customer)
        self.assertEqual(rental.car, self.car)
        self.assertEqual(rental.days, 3)
        self.assertFalse(self.car.available)
        self.assertEqual(len(self.rental_system.rentals), 1)

    def test_return_car(self):
        """Test car return process."""
        self.rental_system.add_car(self.car)
        self.rental_system.add_customer(self.customer)

        rental = self.rental_system.rent_car("CUST001", "C001", 3)
        self.assertIsNotNone(rental, "rent_car should return a Rental object")
        rental_id = rental.rental_id

        success = self.rental_system.return_car(rental_id)

        self.assertTrue(success)
        self.assertTrue(rental.returned)
        self.assertTrue(self.car.available)

    def test_rental_summary(self):
        """Test rental system summary."""
        self.rental_system.load_sample_data()
        summary = self.rental_system.get_rental_summary()

        self.assertIn("total_cars", summary)
        self.assertIn("available_cars", summary)
        self.assertIn("total_customers", summary)
        self.assertIn("active_rentals", summary)
        self.assertIn("completed_rentals", summary)
        self.assertIn("total_revenue", summary)

    def test_memory_leak_fix_cleanup_old_rentals(self):
        """Test that old completed rentals are cleaned up to prevent memory leaks."""
        self.rental_system.add_car(self.car)
        self.rental_system.add_customer(self.customer)
        
        # Set a short retention period for testing
        self.rental_system.rental_retention_days = 1
        
        # Create and complete a rental
        rental = self.rental_system.rent_car("CUST001", "C001", 3)
        self.assertIsNotNone(rental)
        rental_id = rental.rental_id
        
        # Simulate the rental being old by modifying its end_date
        # This simulates a rental that ended more than 1 day ago
        old_end_date = datetime.now() - timedelta(days=2)
        rental.end_date = old_end_date
        
        # Return the car - this should trigger cleanup
        success = self.rental_system.return_car(rental_id)
        self.assertTrue(success)
        
        # The old rental should have been cleaned up
        # Since the rental ended 2 days ago but retention is 1 day
        self.assertEqual(len(self.rental_system.rentals), 0, 
                        "Old completed rental should be cleaned up to prevent memory leak")

    def test_memory_leak_fix_recent_rentals_preserved(self):
        """Test that recent completed rentals are preserved."""
        self.rental_system.add_car(self.car)
        self.rental_system.add_customer(self.customer)
        
        # Set retention period
        self.rental_system.rental_retention_days = 30
        
        # Create and complete a rental
        rental = self.rental_system.rent_car("CUST001", "C001", 3)
        self.assertIsNotNone(rental)
        rental_id = rental.rental_id
        
        # This rental is recent (default end_date is start_date + days)
        # Return the car
        success = self.rental_system.return_car(rental_id)
        self.assertTrue(success)
        
        # The recent rental should still be in the system
        self.assertEqual(len(self.rental_system.rentals), 1, 
                        "Recent completed rental should be preserved")
        self.assertTrue(self.rental_system.rentals[0].returned)

    def test_cleanup_old_rentals_method(self):
        """Test the cleanup_old_rentals method directly."""
        self.rental_system.add_car(self.car)
        self.rental_system.add_customer(self.customer)
        
        # Set short retention period
        self.rental_system.rental_retention_days = 1
        
        # Create multiple rentals
        rental1 = self.rental_system.rent_car("CUST001", "C001", 1)
        self.assertIsNotNone(rental1)
        
        # Make rental1 old and completed
        rental1.returned = True
        rental1.end_date = datetime.now() - timedelta(days=2)
        
        # Add the car back for second rental
        self.car.available = True
        rental2 = self.rental_system.rent_car("CUST001", "C001", 1) 
        self.assertIsNotNone(rental2)
        
        # rental2 is active (not returned)
        self.assertEqual(len(self.rental_system.rentals), 2)
        
        # Run cleanup
        removed_count = self.rental_system.cleanup_old_rentals()
        
        # Should remove 1 old completed rental, keep 1 active rental
        self.assertEqual(removed_count, 1)
        self.assertEqual(len(self.rental_system.rentals), 1)
        self.assertEqual(self.rental_system.rentals[0], rental2)  # Active rental preserved


class TestValidation(unittest.TestCase):

    def test_validate_car_data(self):
        """Test car data validation."""
        valid_car = {
            "car_id": "C001",
            "make": "Toyota",
            "model": "Camry",
            "year": 2022,
            "daily_rate": 45.00,
        }
        self.assertTrue(validate_car_data(valid_car))

        # Missing field
        invalid_car = {"car_id": "C001", "make": "Toyota", "model": "Camry"}
        self.assertFalse(validate_car_data(invalid_car))

        # Invalid year
        invalid_year = valid_car.copy()
        invalid_year["year"] = 1800
        self.assertFalse(validate_car_data(invalid_year))

    def test_validate_customer_data(self):
        """Test customer data validation."""
        valid_customer = {
            "customer_id": "CUST001",
            "name": "John Smith",
            "email": "john.smith@email.com",
            "phone": "555-0101",
        }
        self.assertTrue(validate_customer_data(valid_customer))

        # Invalid email
        invalid_email = valid_customer.copy()
        invalid_email["email"] = "invalid-email"
        self.assertFalse(validate_customer_data(invalid_email))


if __name__ == "__main__":
    unittest.main()  # type: ignore[no-untyped-call]
