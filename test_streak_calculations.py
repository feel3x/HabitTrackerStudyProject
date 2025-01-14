import pytest
import HabitManager
import Analytics
import random
import datetime
import PeriodicityHelper

#This test inserts random completion data for a test habit, and keeps track of the streak/streak-break values of the inserted data. Then checks against the get_streak_info function values. 
def test_habit_completion():
    manager = HabitManager.HabitManager()

    test_periodicities = ["daily", "yearly", "days=2,weeks=4"]

    #prepare test:
    #delete possible old existing test habits
    if("StreakTestHabit" in manager.Dict_Of_Habits):
            manager.delete_habit("StreakTestHabit", True)
    #create test habit
    test_habit = manager.create_habit("StreakTestHabit", random.choice(test_periodicities))

    #randomly add completions for 100 periods of the randomly chosen periodicity and keep track of the supposed streak/streak-break values
    simulated_current_streak = 0
    simulated_current_streak_break = 0
    simulated_longest_streak = 0
    simulated_longest_streak_break = 0
    simulated_total_interuptions = 0
    last_inserted_date = None
    for i in range(100):
        #create test date within the next period according to the test habit's periodicity
        completion_test_date = datetime.datetime.strptime(test_habit.creation_date, "%Y-%m-%d %H:%M:%S.%f") + (PeriodicityHelper.get_relative_delta(test_habit.periodicity) * (i+1))
        last_inserted_date = completion_test_date
        completion_test_date = completion_test_date - datetime.timedelta(hours=1)

        #make random choice to complete habit or not
        random_choice = random.randint(0,1)

        #add streak
        if random_choice == 0:
            #insert completion date
            manager.complete_habit("StreakTestHabit", completion_test_date)

            #increase simulated streak
            simulated_current_streak += 1
            simulated_current_streak_break = 0

        #miss streak
        if random_choice == 1:   
            #increase simulated streak-break and interuptions
            simulated_current_streak_break += 1
            if(simulated_current_streak > 0):
                simulated_total_interuptions += 1
            simulated_current_streak = 0  

        #check for record streaks   
        if simulated_current_streak > simulated_longest_streak:
             simulated_longest_streak = simulated_current_streak
        if simulated_current_streak_break > simulated_longest_streak_break:
             simulated_longest_streak_break = simulated_current_streak_break

    #Run actual Test:
    current_streak, longest_streak, current_streak_break, longest_streak_break, total_interuptions = Analytics.get_streak_info(manager, "StreakTestHabit", test_habit.creation_date, last_inserted_date)
    assert current_streak == simulated_current_streak
    assert longest_streak == simulated_longest_streak
    assert current_streak_break == simulated_current_streak_break
    assert longest_streak_break == simulated_longest_streak_break
    assert total_interuptions == simulated_total_interuptions

    #clean test habit
    manager.delete_habit("StreakTestHabit", True)

        
             

    

                 
    


