import HabitManager
import Analytics
from HabitManager import bcolors

current_manager : HabitManager.HabitManager = None

def start_guide(manager:HabitManager.HabitManager):
    global current_manager
    current_manager = manager
    get_action()


def get_action():
    print(" ")
    action = input(bcolors.WARNING + 'What would you like to do? Options: "Create" (Create new Habit), "Complete" (Complete a Habit), "Delete" (Delete a Habit), "Analyze" (Analyze your Habits)\n' + bcolors.ENDCOLOR)
    print(bcolors.BLUE + action + bcolors.ENDCOLOR)
    if(action.lower() == "create"):
        create_habit()
        return
    if(action.lower() == "complete"):
        complete_habit()
        return
    if(action.lower() == "delete"):
        delete_habit()
        return
    if(action.lower() == "analyze"):
        analyze_habits()
        return
    print(bcolors.FAIL + "Not able to do \""+action+"\". Please try again and chose from the given options." + bcolors.ENDCOLOR)
    print(" ")
    get_action()

def create_habit():
    newHabit = None
    while newHabit is None:
        name = prompt("What is the name for your new habit?")

        periodicity = prompt("How often does this habit need to be completed? Options: \"Daily\", \"Weekly\", \"Monthly\", \"Yearly\", or set a custom periodicity like this example: \"Days=2,Weeks=3,Years=1...\"")

        newHabit = current_manager.create_habit(name, periodicity)
        print(" ")
    get_action()

def complete_habit():
    completed_date = None
    while(completed_date is None):
        name = prompt("What is the name of the habit you would you like to complete?")

        current_manager.complete_habit(name)
        print(" ")
    get_action()
    
def delete_habit():
    delete_success = False
    while(not delete_success):
        name = prompt("What is the name of the habit you would you like to delete?")

        delete_success = current_manager.delete_habit(name)
        print(" ")
    get_action()

def analyze_habits():
    action = prompt("What would you like to analyze? Options: 1 = List all habits, 2 = List Habits sorted by longest streak, 3 = Filter Habits by periodicity, 4 = Get infos about a Habit's streaks, 5 = List worst Habits")

    try:
        action = int(action)
        if(action < 1 or action > 5):
            raise Exception
    except:
        print(bcolors.FAIL+ "Please input a number between 1 and 5." + bcolors.ENDCOLOR)
        print(" ")
        analyze_habits()
    if(action == 1):
        Analytics.get_all_habits(current_manager)
        print(" ")
    if(action == 2):
        Analytics.get_longest_streaks(current_manager)
        print(" ")
    if(action == 3):
        filter_results = None
        while filter_results is None:  
            filter = prompt("What periodicity would you like to filter for?  Options: \"Daily\", \"Weekly\", \"Monthly\", \"Yearly\", or set a custom periodicity like this example: \"Days=2,Weeks=3,Years=1...\"")
            filter_results = Analytics.filter_habits_by_periodicity(current_manager, filter)
    if(action == 4):
        streak_results = None
        while streak_results is None:  
            habit_name = prompt("What is the name of the Habit you want to get streak information about?")
            streak_results = Analytics.get_streak_info(current_manager, habit_name)
            print(" ")
    if(action == 5):
        Analytics.get_least_completed_habits(current_manager)
        print(" ")
    analyze_habits()

        

    
    
def prompt(text):
    result = input(bcolors.CYAN + "Type \"<<<\" to go back to main.\n" + bcolors.ENDCOLOR + bcolors.WARNING + text + "\n" + bcolors.ENDCOLOR)
    print(bcolors.BLUE + result + bcolors.ENDCOLOR)
    if(result == "<<<"):
        get_action()
    return result

if __name__ == '__main__':
    manager = HabitManager.HabitManager()
    start_guide(manager)
  