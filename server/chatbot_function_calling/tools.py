import json
import requests

def get_wrong_questions(user_id: str):
    """Retrieve and display the user's recent wrong questions.

    Args:
      user_id: The ID of the user whose wrong questions should be retrieved.

    Returns:
      A list of dictionaries, each containing details of a wrong question with
      question content, the correct answer, and the user's answer.
    """
    url = f'http://127.0.0.1:1511/recent_wrong_questions?user_id={user_id}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        wrong_questions = data.get("wrong_questions", [])

        return wrong_questions

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def list_tests(user_id: int):
    """Retrieve a list of tests for a given user with specific test details.

    Args:
      user_id: The ID of the user whose tests are to be retrieved.

    Returns:
      A list of dictionaries, each containing the class, taken_date, and test_name of a test.
    """
    url = f'http://127.0.0.1:1511/list_tests?user_id={user_id}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant fields from each test
        tests = data.get("tests", [])
        test_details = [
            {
                "class": test.get("class", "N/A"),
                "taken_date": test.get("taken_date", "N/A"),
                "test_name": test.get("test_name", "N/A"),
                "test_result": test.get("test_result", "N/A"),
            }
            for test in tests
        ]
        
        return test_details

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def list_classes(user_id: int):
    """Retrieve a list of classes for a given user.

    Args:
      user_id: The ID of the user whose classes are to be retrieved.

    Returns:
      A list of dictionaries, each containing the name and description of a class.
    """
    url = f'http://127.0.0.1:1511/list_classes?user_id={user_id}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        classes = data.get("classes", [])
        class_info = [
            {"name": cls.get("name", "N/A"), "description": cls.get("description", "N/A")}
            for cls in classes
        ]
        
        return class_info

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []