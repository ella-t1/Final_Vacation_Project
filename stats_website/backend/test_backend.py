"""Simple test script to verify backend structure and imports."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from src.config import DbConfig, get_connection_kwargs
        print("✓ Config module imported successfully")
        
        from src.dal.base_dao import BaseDAO
        from src.dal.user_dao import UserDAO
        from src.dal.vacation_dao import VacationDAO
        from src.dal.like_dao import LikeDAO
        from src.dal.role_dao import RoleDAO
        print("✓ All DAO modules imported successfully")
        
        from src.services.auth_service import AuthService
        from src.services.statistics_service import StatisticsService
        print("✓ All service modules imported successfully")
        
        from src.api.app import create_app
        from src.api.routes import register_routes
        print("✓ All API modules imported successfully")
        
        print("\n✅ All imports successful! Backend structure is correct.")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("Testing backend structure...\n")
    success = test_imports()
    sys.exit(0 if success else 1)

