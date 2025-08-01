"""
Test script to validate the Flask application structure
"""

import os
import sys

def test_file_structure():
    """Test if all required files exist"""
    required_files = [
        "main.py",
        "requirements.txt",
        "src/routers/router.py",
        "src/services/service1.py"
    ]
    
    print("Testing file structure...")
    all_exist = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"[OK] {file_path} - EXISTS")
        else:
            print(f"[ERROR] {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def test_imports():
    """Test if imports work correctly"""
    print("\nTesting imports...")
    
    try:
        # Test service imports
        sys.path.append('.')
        from src.services.service1 import generate_travel_plan, save_travel_plan
        print("[OK] Service imports - SUCCESS")
        
        # Test router imports  
        from src.routers.router import travel_blueprint
        print("[OK] Router imports - SUCCESS")
        
        return True
        
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Other error: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing Travel Planner Flask Application Structure\n")
    
    structure_ok = test_file_structure()
    
    if structure_ok:
        imports_ok = test_imports()
        
        if imports_ok:
            print("\n[SUCCESS] All tests passed! The Flask application structure is correct.")
            print("\nTo run the application:")
            print("1. Install dependencies: pip install -r requirements.txt")
            print("2. Set up environment variables (GROQ_API_KEY, WEATHER_API_KEY, GEOAPIFY_API_KEY)")
            print("3. Run the app: python main.py")
            print("4. Access API at: http://localhost:5000")
        else:
            print("\n[ERROR] Import tests failed. Please install dependencies first.")
    else:
        print("\n[ERROR] File structure tests failed. Some files are missing.")

if __name__ == "__main__":
    main()