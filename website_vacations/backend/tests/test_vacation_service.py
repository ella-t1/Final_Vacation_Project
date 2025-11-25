"""Comprehensive tests for VacationService."""

import pytest
from datetime import date, timedelta

from src.services.vacation_service import VacationService
from tests.test_db_init import init_test_db


@pytest.fixture(autouse=True)
def setup_test_db():
    """Initialize test database before each test."""
    init_test_db()


class TestVacationService:
    """Test suite for VacationService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = VacationService()
        self.today = date.today()

    # ========== List Vacations Tests ==========

    def test_list_vacations_success(self):
        """Positive test: List all vacations."""
        vacations = list(self.service.list_vacations())
        assert len(vacations) >= 12  # At least 12 from seed data
        # Check sorting (should be by start_date ascending)
        for i in range(len(vacations) - 1):
            assert vacations[i].start_date <= vacations[i + 1].start_date

    def test_list_vacations_includes_past(self):
        """Positive test: List includes past vacations."""
        # Add a past vacation manually (bypassing validation)
        from src.dal.vacation_dao import VacationDAO
        dao = VacationDAO()
        past_date = self.today - timedelta(days=10)
        dao.insert({
            "country_id": 1,
            "description": "Past vacation",
            "start_date": past_date,
            "end_date": past_date + timedelta(days=5),
            "price": 1000.0,
            "image_name": None,
        })
        # List should include it
        vacations = list(self.service.list_vacations())
        assert any(v.description == "Past vacation" for v in vacations)

    # ========== Add Vacation Tests ==========

    def test_add_vacation_success(self):
        """Positive test: Add a valid vacation."""
        vacation = self.service.add_vacation(
            country_id=1,
            description="Amazing vacation",
            start_date=self.today + timedelta(days=30),
            end_date=self.today + timedelta(days=37),
            price=2500.0,
            image_name="test.jpg"
        )
        assert vacation.id > 0
        assert vacation.description == "Amazing vacation"
        assert vacation.price == 2500.0

    def test_add_vacation_minimal_fields(self):
        """Positive test: Add vacation without image."""
        vacation = self.service.add_vacation(
            country_id=2,
            description="Simple vacation",
            start_date=self.today + timedelta(days=20),
            end_date=self.today + timedelta(days=25),
            price=1500.0
        )
        assert vacation.id > 0
        assert vacation.image_name is None

    def test_add_vacation_empty_description(self):
        """Negative test: Empty description."""
        with pytest.raises(ValueError, match="Description is mandatory"):
            self.service.add_vacation(
                1, "", self.today + timedelta(days=10),
                self.today + timedelta(days=15), 1000.0
            )

    def test_add_vacation_negative_price(self):
        """Negative test: Negative price."""
        with pytest.raises(ValueError, match="Price must be between 0 and 10,000"):
            self.service.add_vacation(
                1, "Test", self.today + timedelta(days=10),
                self.today + timedelta(days=15), -100.0
            )

    def test_add_vacation_price_too_high(self):
        """Negative test: Price exceeds 10,000."""
        with pytest.raises(ValueError, match="Price must be between 0 and 10,000"):
            self.service.add_vacation(
                1, "Test", self.today + timedelta(days=10),
                self.today + timedelta(days=15), 15000.0
            )

    def test_add_vacation_end_before_start(self):
        """Negative test: End date before start date."""
        with pytest.raises(ValueError, match="End date cannot be earlier"):
            self.service.add_vacation(
                1, "Test", self.today + timedelta(days=15),
                self.today + timedelta(days=10), 1000.0
            )

    def test_add_vacation_past_start_date(self):
        """Negative test: Start date in the past."""
        with pytest.raises(ValueError, match="Past dates cannot be selected"):
            self.service.add_vacation(
                1, "Test", self.today - timedelta(days=5),
                self.today + timedelta(days=5), 1000.0
            )

    def test_add_vacation_invalid_country(self):
        """Negative test: Invalid country ID."""
        with pytest.raises(ValueError, match="does not exist"):
            self.service.add_vacation(
                9999, "Test", self.today + timedelta(days=10),
                self.today + timedelta(days=15), 1000.0
            )

    # ========== Update Vacation Tests ==========

    def test_update_vacation_success(self):
        """Positive test: Update vacation successfully."""
        # Add a vacation first
        vacation = self.service.add_vacation(
            1, "Original", self.today + timedelta(days=40),
            self.today + timedelta(days=45), 2000.0
        )
        # Update it
        updated = self.service.update_vacation(
            vacation.id,
            description="Updated description",
            price=2500.0
        )
        assert updated.description == "Updated description"
        assert updated.price == 2500.0

    def test_update_vacation_all_fields(self):
        """Positive test: Update all fields."""
        vacation = self.service.add_vacation(
            1, "Original", self.today + timedelta(days=50),
            self.today + timedelta(days=55), 2000.0
        )
        new_start = self.today + timedelta(days=60)
        new_end = self.today + timedelta(days=65)
        updated = self.service.update_vacation(
            vacation.id,
            country_id=2,
            description="Fully updated",
            start_date=new_start,
            end_date=new_end,
            price=3000.0,
            image_name="new.jpg"
        )
        assert updated.country_id == 2
        assert updated.description == "Fully updated"
        assert updated.start_date == new_start
        assert updated.end_date == new_end
        assert updated.price == 3000.0
        assert updated.image_name == "new.jpg"

    def test_update_vacation_past_dates_allowed(self):
        """Positive test: Update with past dates (allowed for updates)."""
        # Create vacation with future dates
        vacation = self.service.add_vacation(
            1, "Future", self.today + timedelta(days=100),
            self.today + timedelta(days=105), 2000.0
        )
        # Update to past dates (should be allowed)
        past_start = self.today - timedelta(days=10)
        past_end = self.today - timedelta(days=5)
        updated = self.service.update_vacation(
            vacation.id,
            start_date=past_start,
            end_date=past_end
        )
        assert updated.start_date == past_start
        assert updated.end_date == past_end

    def test_update_vacation_not_found(self):
        """Negative test: Update non-existent vacation."""
        with pytest.raises(ValueError, match="does not exist"):
            self.service.update_vacation(99999, description="Test")

    def test_update_vacation_empty_description(self):
        """Negative test: Empty description."""
        vacation = self.service.add_vacation(
            1, "Test", self.today + timedelta(days=70),
            self.today + timedelta(days=75), 2000.0
        )
        with pytest.raises(ValueError, match="cannot be empty"):
            self.service.update_vacation(vacation.id, description="")

    def test_update_vacation_invalid_price(self):
        """Negative test: Invalid price."""
        vacation = self.service.add_vacation(
            1, "Test", self.today + timedelta(days=80),
            self.today + timedelta(days=85), 2000.0
        )
        with pytest.raises(ValueError, match="Price must be between 0 and 10,000"):
            self.service.update_vacation(vacation.id, price=15000.0)

    def test_update_vacation_end_before_start(self):
        """Negative test: End date before start date."""
        vacation = self.service.add_vacation(
            1, "Test", self.today + timedelta(days=90),
            self.today + timedelta(days=95), 2000.0
        )
        with pytest.raises(ValueError, match="End date cannot be earlier"):
            self.service.update_vacation(
                vacation.id,
                start_date=self.today + timedelta(days=100),
                end_date=self.today + timedelta(days=95)
            )

    def test_update_vacation_invalid_country(self):
        """Negative test: Invalid country ID."""
        vacation = self.service.add_vacation(
            1, "Test", self.today + timedelta(days=110),
            self.today + timedelta(days=115), 2000.0
        )
        with pytest.raises(ValueError, match="does not exist"):
            self.service.update_vacation(vacation.id, country_id=9999)

    # ========== Delete Vacation Tests ==========

    def test_delete_vacation_success(self):
        """Positive test: Delete vacation successfully."""
        # Add a vacation
        vacation = self.service.add_vacation(
            1, "To Delete", self.today + timedelta(days=120),
            self.today + timedelta(days=125), 2000.0
        )
        # Delete it
        self.service.delete_vacation(vacation.id)
        # Verify it's deleted
        with pytest.raises(ValueError, match="does not exist"):
            self.service.update_vacation(vacation.id, description="Test")

    def test_delete_vacation_cascades_likes(self):
        """Positive test: Deleting vacation deletes associated likes."""
        from src.services.user_service import UserService
        user_service = UserService()
        # Register a user
        user = user_service.register_user("Delete", "Test", "delete@example.com", "pass1234")
        # Add a vacation
        vacation = self.service.add_vacation(
            1, "With Likes", self.today + timedelta(days=130),
            self.today + timedelta(days=135), 2000.0
        )
        # Like the vacation
        user_service.like_vacation(user.id, vacation.id)
        # Delete the vacation
        self.service.delete_vacation(vacation.id)
        # Verify like is gone (trying to unlike should fail)
        with pytest.raises(ValueError, match="has not liked"):
            user_service.unlike_vacation(user.id, vacation.id)

    def test_delete_vacation_not_found(self):
        """Negative test: Delete non-existent vacation."""
        with pytest.raises(ValueError, match="does not exist"):
            self.service.delete_vacation(99999)
