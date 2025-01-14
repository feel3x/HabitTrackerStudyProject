import HabitManager
import Habit
import PeriodicityHelper
import datetime
import dateutil
import random
import Analytics

manager = HabitManager.HabitManager()

habits_to_insert = [("CleanHome", "days=2"), ("WaterPlants", "weekly"), ("TeethBrushing", "daily"), ("Workout", "daily"), ("PayRent", "Monthly"), ("HaveAdventure", "yearly")]
current_time = datetime.datetime.now()
#delete these Habits in case they already exist
for name, periodicity in habits_to_insert:
    if(name in manager.Dict_Of_Habits):
            manager.delete_habit(name, True)
    habit_periodicity_delta = PeriodicityHelper.get_relative_delta(periodicity)
    #calculate creation date for 100 periods before now
    creation_date = current_time - (habit_periodicity_delta * 99)
    #create habit
    new_habit = manager.create_habit(name, periodicity, creation_date)
    #randomly add completions for 100 periods of the randomly chosen periodicity and keep track of the supposed streak/streak-break values
    for i in range(100):
        #create test date within the next period according to the test habit's periodicity
        completion_test_date = datetime.datetime.strptime(new_habit.creation_date, "%Y-%m-%d %H:%M:%S.%f") + (PeriodicityHelper.get_relative_delta(new_habit.periodicity) * (i+1))
        completion_test_date = completion_test_date - datetime.timedelta(hours=1)

        #make random choice to complete habit or not. Likelyhood slightly leaning towards completing
        random_choice = random.randrange(0,100,1)

        #add streak
        if random_choice < 70:
            #insert completion date
            manager.complete_habit(name, completion_test_date)

    Analytics.get_streak_info(manager, name)
