"""Business Logic Layer for Vacation operations."""

from datetime import date
from typing import Iterable, Optional

from src.dal.country_dao import CountryDAO
from src.dal.vacation_dao import VacationDAO
from src.models.dtos import VacationDTO


class VacationService:
    """Service for managing vacation-related business logic."""

    def __init__(self) -> None:
        """Initialize VacationService with required DAOs."""
        self._vacation_dao = VacationDAO()
        self._country_dao = CountryDAO()

    def list_vacations(self) -> Iterable[VacationDTO]:
        """
        Retrieve all vacations, sorted by start_date in ascending order.
        Includes vacations that have already ended.
        
        Returns:
            Iterable[VacationDTO]: List of all vacations
        """
        vacations = self._vacation_dao.list_all()
        return [
            VacationDTO(
                id=v["id"],
                country_id=v["country_id"],
                description=v["description"],
                start_date=v["start_date"],
                end_date=v["end_date"],
                price=float(v["price"]),
                image_name=v.get("image_name"),
            )
            for v in vacations
        ]

    def add_vacation(
        self,
        country_id: int,
        description: str,
        start_date: date,
        end_date: date,
        price: float,
        image_name: Optional[str] = None,
    ) -> VacationDTO:
        """
        Add a new vacation to the system.
        
        Validations:
        - All fields are mandatory (except image_name)
        - Price must be between 0 and 10,000
        - End date cannot be earlier than start date
        - Past dates cannot be selected (start_date must be today or future)
        - Country must exist
        
        Args:
            country_id: ID of the country
            description: Description of the vacation
            start_date: Start date of the vacation
            end_date: End date of the vacation
            price: Price of the vacation (0-10000)
            image_name: Optional image file name
            
        Returns:
            VacationDTO: The newly created vacation
            
        Raises:
            ValueError: If validation fails
        """
        # Validate mandatory fields
        if not description or not description.strip():
            raise ValueError("Description is mandatory")
        if not start_date:
            raise ValueError("Start date is mandatory")
        if not end_date:
            raise ValueError("End date is mandatory")
        if price is None:
            raise ValueError("Price is mandatory")

        # Validate price range
        if price < 0 or price > 10000:
            raise ValueError("Price must be between 0 and 10,000")

        # Validate dates
        if end_date < start_date:
            raise ValueError("End date cannot be earlier than start date")

        # Validate that start_date is not in the past
        today = date.today()
        if start_date < today:
            raise ValueError("Past dates cannot be selected for vacation period")

        # Validate country exists
        country = self._country_dao.get_by_id(country_id)
        if not country:
            raise ValueError(f"Country with ID {country_id} does not exist")

        # Insert new vacation
        vacation_data = {
            "country_id": country_id,
            "description": description.strip(),
            "start_date": start_date,
            "end_date": end_date,
            "price": float(price),
            "image_name": image_name.strip() if image_name else None,
        }

        vacation_id = self._vacation_dao.insert(vacation_data)

        return VacationDTO(
            id=vacation_id,
            country_id=vacation_data["country_id"],
            description=vacation_data["description"],
            start_date=vacation_data["start_date"],
            end_date=vacation_data["end_date"],
            price=vacation_data["price"],
            image_name=vacation_data["image_name"],
        )

    def update_vacation(
        self,
        vacation_id: int,
        *,
        country_id: Optional[int] = None,
        description: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        price: Optional[float] = None,
        image_name: Optional[str] = None,
    ) -> VacationDTO:
        """
        Update an existing vacation.
        
        Validations:
        - All fields are mandatory except image_name
        - Price must be between 0 and 10,000
        - End date cannot be earlier than start date
        - Past dates are allowed (for editing already ended vacations)
        - Country must exist if provided
        
        Args:
            vacation_id: ID of the vacation to update
            country_id: Optional new country ID
            description: Optional new description
            start_date: Optional new start date
            end_date: Optional new end date
            price: Optional new price (0-10000)
            image_name: Optional new image file name
            
        Returns:
            VacationDTO: The updated vacation
            
        Raises:
            ValueError: If validation fails or vacation doesn't exist
        """
        # Check if vacation exists
        existing_vacation = self._vacation_dao.get_by_id(vacation_id)
        if not existing_vacation:
            raise ValueError(f"Vacation with ID {vacation_id} does not exist")

        # Prepare update data (use existing values if not provided)
        update_data = {}
        
        if country_id is not None:
            # Validate country exists
            country = self._country_dao.get_by_id(country_id)
            if not country:
                raise ValueError(f"Country with ID {country_id} does not exist")
            update_data["country_id"] = country_id
        else:
            update_data["country_id"] = existing_vacation["country_id"]

        if description is not None:
            if not description.strip():
                raise ValueError("Description cannot be empty")
            update_data["description"] = description.strip()
        else:
            update_data["description"] = existing_vacation["description"]

        if start_date is not None:
            update_data["start_date"] = start_date
        else:
            update_data["start_date"] = existing_vacation["start_date"]

        if end_date is not None:
            update_data["end_date"] = end_date
        else:
            update_data["end_date"] = existing_vacation["end_date"]

        if price is not None:
            if price < 0 or price > 10000:
                raise ValueError("Price must be between 0 and 10,000")
            update_data["price"] = float(price)
        else:
            update_data["price"] = float(existing_vacation["price"])

        # Validate dates (end_date >= start_date)
        if update_data["end_date"] < update_data["start_date"]:
            raise ValueError("End date cannot be earlier than start date")

        # Image name can be None or empty string (to clear it)
        if image_name is not None:
            update_data["image_name"] = image_name.strip() if image_name.strip() else None
        else:
            update_data["image_name"] = existing_vacation.get("image_name")

        # Update vacation
        rows_affected = self._vacation_dao.update_by_id(vacation_id, update_data)
        if rows_affected == 0:
            raise ValueError(f"Failed to update vacation with ID {vacation_id}")

        # Return updated vacation
        updated_vacation = self._vacation_dao.get_by_id(vacation_id)
        return VacationDTO(
            id=updated_vacation["id"],
            country_id=updated_vacation["country_id"],
            description=updated_vacation["description"],
            start_date=updated_vacation["start_date"],
            end_date=updated_vacation["end_date"],
            price=float(updated_vacation["price"]),
            image_name=updated_vacation.get("image_name"),
        )

    def delete_vacation(self, vacation_id: int) -> None:
        """
        Delete an existing vacation.
        All likes associated with this vacation are automatically deleted (CASCADE).
        
        Args:
            vacation_id: ID of the vacation to delete
            
        Raises:
            ValueError: If vacation doesn't exist
        """
        # Check if vacation exists
        existing_vacation = self._vacation_dao.get_by_id(vacation_id)
        if not existing_vacation:
            raise ValueError(f"Vacation with ID {vacation_id} does not exist")

        # Delete vacation (likes are automatically deleted due to CASCADE)
        rows_affected = self._vacation_dao.delete_by_id(vacation_id)
        if rows_affected == 0:
            raise ValueError(f"Failed to delete vacation with ID {vacation_id}")


