import pytest
import HabitManager

#Tests the creation and deletion of habits with equivalence groups of names that should be rejected and accepted, as well as avoid duplicates. 
def test_habit_creation_and_deletion():
    manager = HabitManager.HabitManager()

    #equivalence groups:
    #Names for a habit that should not be rejected when creating and deleting
    non_rejecting_testing__data= [("TestHabit1", "daily"), ("TestHabit", "YEARLY"), ("10101010", "days=2,MONths=3")]
    #Names for a habit that should be rejected when creating a habit
    rejecting_creation_testing_data= [("TestHabit1", "daily"), ("TestHabit2", "days"), ("TestHabit3", ""), ("TestHabit3", "1"), ("TestHabit4", " "), ("TestHabit5", "@"),(" ", "daily"), ("TestHabit@", "daily"), ("", "daily")]


    #prepare Test:
    #delete possible old existing test habits
    for name, periodicity in non_rejecting_testing__data:
        if(name in manager.Dict_Of_Habits):
            manager.delete_habit(name, True)
    if("NonexistantTestHabit" in manager.Dict_Of_Habits):
            manager.delete_habit("NonexistantTestHabit", True)
    
    #Execute creation test
    #non rejecting
    for name, periodicity in non_rejecting_testing__data:
        assert manager.create_habit(name, periodicity) != None
        assert name in manager.Dict_Of_Habits
    #rejecting
    for name, periodicity in rejecting_creation_testing_data:
        assert manager.create_habit(name, periodicity) is None
        if(name != "TestHabit1"):
            assert name not in manager.Dict_Of_Habits

    #Execute deletion test
    #non rejecting
    for name, periodicity in non_rejecting_testing__data:
        assert manager.delete_habit(name, True) is True
        assert name not in manager.Dict_Of_Habits
    #reject deleting a non existant habit
    assert manager.delete_habit("NonexistantTestHabit", True) is False
    
