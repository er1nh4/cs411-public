import pytest
from boxing.models.ring_model import RingModel
from boxing.models.boxers_model import Boxer, create_boxer, delete_boxer
from boxing.utils.api_utils import get_random

# Mock get_random function to return a fixed value
def mock_get_random(value):
    return lambda: value

@pytest.fixture
def ring():
    """Fixture to create an instance of RingModel."""
    return RingModel()

@pytest.fixture
def boxer1():
    """Fixture to create an instance of Boxer 1 (Ali)."""
    boxer = Boxer(id=1, name="Ali", weight=180, height=70, reach=72.5, age=28, weight_class="MIDDLEWEIGHT")
    
    # Clean up any existing boxer with the same ID in the database
    try:
        delete_boxer(boxer.id)  # Delete any existing boxer with the same ID
    except ValueError:
        pass  # If the boxer doesn't exist, continue without error
    
    # Ensure the boxer is added to the database
    try:
        create_boxer(boxer.name, boxer.weight, boxer.height, boxer.reach, boxer.age)
    except ValueError as e:
        print(f"Error creating boxer: {e}")
        pass  # If the boxer already exists, ignore the error and continue
    
    return boxer

@pytest.fixture
def boxer2():
    """Fixture to create an instance of Boxer 2 (Tyson)."""
    boxer = Boxer(id=2, name="Tyson", weight=220, height=72, reach=75, age=30, weight_class="HEAVYWEIGHT")
    
    # Clean up any existing boxer with the same ID in the database
    try:
        delete_boxer(boxer.id)  # Delete any existing boxer with the same ID
    except ValueError:
        pass  # If the boxer doesn't exist, continue without error
    
    # Ensure the boxer is added to the database
    try:
        create_boxer(boxer.name, boxer.weight, boxer.height, boxer.reach, boxer.age)
    except ValueError as e:
        print(f"Error creating boxer: {e}")
        pass  # If the boxer already exists, ignore the error and continue
    
    return boxer

def test_fight_success(ring, boxer1, boxer2, mocker):
    """Test a successful fight between two boxers."""
    ring.enter_ring(boxer1)
    ring.enter_ring(boxer2)

    # Mock get_random to return a value that determines boxer1 as the winner
    mocker.patch("boxing.utils.api_utils.get_random", return_value=0.9)  # Boxer1 wins if random < 0.8

    # Ensure the correct winner is returned
    winner = ring.fight()
    assert winner == "Ali", f"Expected 'Ali' to win, but got {winner}"

def test_get_fighting_skill(boxer1):
    """Test the calculation of the fighting skill of a boxer."""
    skill = boxer1.get_fighting_skill()
    expected_skill = (boxer1.weight * len(boxer1.name)) + (boxer1.reach / 10)  # Adjusted expected calculation
    assert skill == expected_skill, f"Expected skill {expected_skill}, but got {skill}"
