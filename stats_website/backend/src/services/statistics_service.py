"""Statistics service for providing system statistics."""

from typing import Dict, Any

from src.dal.vacation_dao import VacationDAO
from src.dal.user_dao import UserDAO
from src.dal.like_dao import LikeDAO


class StatisticsService:
    """Service for providing system statistics."""

    def __init__(self) -> None:
        """Initialize statistics service with DAOs."""
        self.vacation_dao = VacationDAO()
        self.user_dao = UserDAO()
        self.like_dao = LikeDAO()

    def get_vacation_stats(self) -> Dict[str, int]:
        """Get vacation statistics (past, ongoing, future).
        
        Returns:
            dict: Dictionary with 'pastVacations', 'ongoingVacations', 'futureVacations'
        """
        stats = self.vacation_dao.get_vacations_by_date_range()
        return {
            "pastVacations": stats["past"],
            "ongoingVacations": stats["ongoing"],
            "futureVacations": stats["future"],
        }

    def get_total_users(self) -> Dict[str, int]:
        """Get total number of users.
        
        Returns:
            dict: Dictionary with 'totalUsers'
        """
        count = self.user_dao.count_total()
        return {"totalUsers": count}

    def get_total_likes(self) -> Dict[str, int]:
        """Get total number of likes.
        
        Returns:
            dict: Dictionary with 'totalLikes'
        """
        count = self.like_dao.count_total()
        return {"totalLikes": count}

    def get_likes_distribution(self) -> list[Dict[str, Any]]:
        """Get likes distribution by vacation destination.
        
        Returns:
            list: List of dictionaries with 'destination' and 'likes' keys
        """
        return self.like_dao.get_distribution_by_destination()

