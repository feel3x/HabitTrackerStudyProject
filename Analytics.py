import HabitManager
import Habit
import PeriodicityHelper
import datetime
from HabitManager import bcolors

def get_all_habits(manager:HabitManager.HabitManager, start_date = datetime.datetime.min, end_date=None):
    """
    This function prints and returns a list of all habits.

    Parameters:
    manager (HabitManager): the manager containing the habits.
    start_date (datetime): The start of the period. (FOR FUTURE IMPLEMENTATIONS)
    end_date(datetime): The end of the period. (FOR FUTURE IMPLEMENTATIONS)

    Returns:
    list: List of Habit Objects.
    """
    if(end_date is None):
            end_date = datetime.datetime.now()

    #iterate through all habits in Manager Dictionary
    list_of_habits = []
    for name, habit in manager.Dict_Of_Habits.items():
        print(f'"{habit.name}" - {habit.periodicity} - Created on {habit.creation_date}')
        list_of_habits.append(habit)
    
    #check results
    if(len(list_of_habits) < 1):
        print("No Habits found. Pleaes try to create some first.")
        return None

    return list_of_habits

def filter_habits_by_periodicity(manager:HabitManager.HabitManager, periodicity: str):
    """
    This function prints and returns a list of all habits with the given periodicity.

    Parameters:
    manager (HabitManager): the manager containing the habits.
    periodicity (str): The periodicity to filter for.

    Returns:
    list: List of Habit Objects.
    """
    #iterate through all habits
    list_of_filtered_habits = []
    for name, habit in manager.Dict_Of_Habits.items():
        #cross check periodicities
        if(PeriodicityHelper.get_relative_delta(habit.periodicity) == PeriodicityHelper.get_relative_delta(periodicity)):
            print(f'"{habit.name}" - {habit.periodicity} - Created on {habit.creation_date}')
            list_of_filtered_habits.append(habit)

    #check results
    if(len(list_of_filtered_habits) < 1):
        print("No Habits found with Periodicity \""+ periodicity + "\".")
        return None

    return list_of_filtered_habits


#Prints and returns a list with habits and the streak's length sorted by the longest streak from longest to shortest
def get_longest_streaks(manager:HabitManager.HabitManager, start_date = datetime.datetime.min, end_date=None):
    """
    Prints and returns a list with habits and the streak's length sorted by the longest streak from longest to shortest.

    Parameters:
    manager (HabitManager): the manager containing the habits.
    start_date (datetime): The start of the period. (FOR FUTURE IMPLEMENTATIONS)
    end_date(datetime): The end of the period. (FOR FUTURE IMPLEMENTATIONS)

    Returns:
    list: List of Habit Objects.
    """
    if(end_date is None):
        end_date = datetime.datetime.now()

    #get habits and their longest streaks
    list_of_habits_longeststreaks = []
    for name, habit in manager.Dict_Of_Habits.items():
        longest_streak = habit.get_streak_infos()[1]
        list_of_habits_longeststreaks.append((habit, longest_streak))

    #check results
    if(len(list_of_habits_longeststreaks) < 1):
        print("No Habits found. Pleaes try to create some first.")
        return None
    
    #reverse sort list by longest streak
    list_of_habits_longeststreaks.sort(reverse=True, key=sort_helper_function)

    #print list
    for habit, longest_streak in list_of_habits_longeststreaks:
        print(f'"{habit.name}" - Longest Streak: ' + str(longest_streak))

    return list_of_habits_longeststreaks

#prints and returns current streak, longest streak, current streak-break and longest streak break
def get_streak_info(manager:HabitManager.HabitManager, habit_name:str, start_date = datetime.datetime.min, end_date=None):
    """
    Prints and returns current streak, longest streak, current streak-break and longest streak break.

    Parameters:
    manager (HabitManager): the manager containing the habits.
    start_date (datetime): The start of the period. (FOR FUTURE IMPLEMENTATIONS)
    end_date(datetime): The end of the period. (FOR FUTURE IMPLEMENTATIONS)

    Returns:
    list: List of Habit Objects.
    """ 
    if(end_date is None):
        end_date = datetime.datetime.now()
    #verify existanse of habit key
    if(habit_name not in manager.Dict_Of_Habits):
        print(bcolors.FAIL + "The habit with the name \""+ habit_name + "\" does not exist." + bcolors.ENDCOLOR)
        return None
    
    habit = manager.Dict_Of_Habits[habit_name]

    #verify existanse of habit
    if(habit is None):
        print(bcolors.FAIL + "The habit with the name \""+ habit_name + "\" does not exist." +bcolors.ENDCOLOR)
        return None
    
    #get streak infos from habit
    current_streak, longest_streak, current_streak_break, longest_streak_break, total_interuptions = habit.get_streak_infos(start_date, end_date)
    
    #print strak infos
    print(f'"{habit.name}": Current Streak: {current_streak} - Longest Streak: {longest_streak} - Current Streak-Break: {current_streak_break} - Longest Streak-Break {longest_streak_break} - Total Interuptions of Streaks: {total_interuptions}')
    
    return current_streak, longest_streak, current_streak_break, longest_streak_break, total_interuptions

def get_least_completed_habits(manager:HabitManager.HabitManager):
    """
    Prints and returns a list of the worst, least completed habits.

    Parameters:
    manager (HabitManager): the manager containing the habits.

    Returns:
    list: List of Habit Objects.
    """ 
    #get habits, their longest streak braks and most interuptions
    list_of_habits_longestbreaks_interuptions = []
    for name, habit in manager.Dict_Of_Habits.items():
        habit_streak_infos = habit.get_streak_infos()
        list_of_habits_longestbreaks_interuptions.append((habit, habit_streak_infos[4], habit_streak_infos[3]))
    
    #check results
    if(len(list_of_habits_longestbreaks_interuptions) < 1):
        print("No Habits found. Pleaes try to create some first.")
        return None
    
    #reverse sort list by total interuptions and secondary by longest streak-break
    list_of_habits_longestbreaks_interuptions.sort(reverse=True, key=sort_helper_function)

    #print list
    for habit, total_interuptions, longest_streak in list_of_habits_longestbreaks_interuptions:
        print(f'"{habit.name}":  - Total Interuptions: {str(total_interuptions)} - Longest Streak-Break: {str(longest_streak)}')

    return list_of_habits_longestbreaks_interuptions

#This function helps sorting the lists
def sort_helper_function(e):
    if(len(e) < 3):
        return e[1]
    if(len(e) < 4):
        return e[1], e[2]