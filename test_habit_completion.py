import pytest
import HabitManager
import Analytics

#Tests the creation and deletion of habits with equivalence groups of names that should be rejected and accepted, as well as avoid duplicates. 
def test_habit_completion():
    manager = HabitManager.HabitManager()

    #prepare Test:
    #delete possible old existing test habits
    if("CompletionTestHabit" in manager.Dict_Of_Habits):
            manager.delete_habit("CompletionTestHabit", True)
    if("NonexistantTestHabit" in manager.Dict_Of_Habits):
            manager.delete_habit("NonexistantTestHabit", True)
    
    #create test habit
    test_habit = manager.create_habit("CompletionTestHabit", "daily")
    
    #assert preconfigurations
    current_streak, longest_streak, current_streak_break, longest_streak_break, total_interuptions = Analytics.get_streak_info(manager, "CompletionTestHabit")
    assert current_streak == 0

    #run test:
    #complete habit
    assert manager.complete_habit("CompletionTestHabit") is not None
    
    #assert that completion was successful
    current_streak, longest_streak, current_streak_break, longest_streak_break, total_interuptions = Analytics.get_streak_info(manager, "CompletionTestHabit")
    assert current_streak == 1

    #assert rejection of completion of non existant habit
    assert manager.complete_habit("NonexistantTestHabit") is None

    #clean test habit
    manager.delete_habit("CompletionTestHabit", True)


    
