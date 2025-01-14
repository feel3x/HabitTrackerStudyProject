import datetime
import Habit
import sqlite3
import os
import PeriodicityHelper


class HabitManager:
    """
    Class to manage all the Habit Objects and communicate with database.

    Attributes:
    Dict_Of_Habits (dictionary): A dictionary containing all the Habits and their names as Keys.
    db_connection (Connection): The connection to the Database.
    db_cursor(Cursor): The Cursor of the Database.
    """ 
    def __init__(self):
        self.Dict_Of_Habits = {}

        #establish connection to database
        self.db_connection = sqlite3.connect(os.path.join(os.path.abspath(os.path.dirname(__file__)),"databases","habits_data.db"))

        #enforce foreign keys in database
        self.db_connection.execute("PRAGMA foreign_keys = 1")
        self.db_cursor = self.db_connection.cursor()

        #retrieve the habits currently saved in the database into this manager
        self.retrieve_habits()

    def create_habit(self, name, periodicity, creation_date = None):
        """
        Function to create a new Habit.

        Parameters:
        name (str): The name of the new Habit.
        periodicity (str): The periodicity of the new Habit

        Returns:
        Habit: New Habit Object.
        """ 
        print("Creating new Habit...")
        #check if a habit with this name already exists.
        if(name in self.Dict_Of_Habits):
            print(bcolors.FAIL + "A Habit with this name already exists. Please chose a different name." + bcolors.ENDCOLOR)
            return None
        
        #Verify that name only exists of letters and numbers
        if(not name.isalnum()):
            print(bcolors.FAIL + "The name can only consist of alphanumeric letters and numbers." + bcolors.ENDCOLOR)
            return None
        
        #verify that the entered periodicity is valid
        if(Habit.PeriodicityHelper.get_relative_delta(periodicity) is None):
            print(bcolors.FAIL + "The entered Periodicity is not valid. Please chose from \"Daily\", \"Weekly\", \"Monthly\", \"Yearly\", or set a custom periodicity like this example: \"Days=2,Weeks=3,Years=1...\"" + bcolors.ENDCOLOR)
            return None
        
        if(creation_date is None):
            creation_date = datetime.datetime.now()

        #Add new Habit to database
        if(not self.sql_action("INSERT INTO Habits(habit_name, periodicity, creation_date) VALUES (?,?,?)", (name, periodicity, creation_date))):
            print(bcolors.FAIL + "Habit could not be added to the database." + bcolors.ENDCOLOR)
            return None
        new_habit_id = self.db_cursor.lastrowid
                        
        #create new habit
        new_habit = Habit.Habit(new_habit_id, name, periodicity, creation_date)
        if(new_habit == None):
            print(bcolors.FAIL + "Habit Object could not be created." + bcolors.ENDCOLOR)
            return None
        
        #Finally add new Habbit to Manager Habits List
        self.Dict_Of_Habits[new_habit.name] = new_habit

        print(bcolors.OKGREEN + "Habit with name \"" + new_habit.name + "\" successfully created at " + datetime.datetime.strftime(creation_date, "%d/%m/%Y - %H:%M:%S") + " with a Periodicity of " + new_habit.periodicity + "." + bcolors.ENDCOLOR)
        return new_habit
    
    def delete_habit(self, name, no_confirmation = False):
        """
        Function to delete a Habit.

        Parameters:
        name (str): The name of the Habit to delete.
        no_confirmation (boolean): If the Habit should be deleted without confirmation by the user.

        Returns:
        Boolean: True when successful.
        """ 
        #check if a habit with this name exists.
        if(name not in self.Dict_Of_Habits):
            print(bcolors.FAIL + "A Habit with this name was not found." + bcolors.ENDCOLOR)
            return False
        habit_to_delete = self.Dict_Of_Habits[name]
        
        if(not no_confirmation):
            #Make the user confirm the deletion
            decision = None
            while(decision is None or (decision != "y" and decision != "n")):
                decision = input(bcolors.WARNING+ "Are you sure you want to delete the habit \""+name+"\"? \n Y for Yes. N for No.\n" + bcolors.ENDCOLOR).lower()
            if(decision == "n"):
                return False
        

        #remove Habit from database
        if(not self.sql_action("DELETE FROM Habits WHERE habit_id = ?", (habit_to_delete.id,))):
            print(bcolors.FAIL + "Habit could not be deleted from Database." + bcolors.ENDCOLOR)
            return False
        
        #remove Habit from list
        self.Dict_Of_Habits.pop(name)
        print(bcolors.OKGREEN + "Habit was successfully removed." + bcolors.ENDCOLOR)
        return True

    def complete_habit(self, name, time_completed = None):
        """
        Function to coomplete new Habit.

        Parameters:
        name (str): The name of the new Habit.
        time_completed (datetime): Optional time for when the habit should be marked as completed for.

        Returns:
        Datetime: Date and Time when the Habit was completed.
        """ 
        #check if this habit exists
        if(name not in self.Dict_Of_Habits):
            print(bcolors.FAIL + "Habit was NOT found." + bcolors.ENDCOLOR)
            return None
        completed_habit = self.Dict_Of_Habits[name]

        if(time_completed is None):
            time_completed = datetime.datetime.now()

        #add completed date to database
        if(not self.sql_action("INSERT INTO Completion_Dates(habit_id, completion_date) VALUES(?,?)", (completed_habit.id, time_completed))):
            print(bcolors.FAIL + "Completion Date could not be inserted into Database." + bcolors.ENDCOLOR)
            return None
        
        #complete Habit
        time_completed = completed_habit.complete_task(time_completed)
        
        return time_completed

    def retrieve_habits(self):
        print("Retrieving habits from database...")

        #retrieve entries from database
        self.db_cursor.execute("SELECT * FROM Habits LEFT JOIN Completion_Dates ON Habits.habit_id LIKE Completion_Dates.habit_id")
        result = self.db_cursor.fetchall()

        #create new Habit object for each entry
        for entry in result:
            #See if Habit is already in the list. If so, only add the Completion Dates
            if(entry[1] in self.Dict_Of_Habits):
                self.Dict_Of_Habits[entry[1]].complete_task(entry[6])
                continue
            
            #create new Habit object
            new_habit_obj = Habit.Habit(entry[0], entry[1], entry[2], entry[3])
            #add the first completion date if one exists
            if(entry[6] is not None):
                new_habit_obj.complete_task(entry[6])
            
            #add Habit object to Dictionary
            self.Dict_Of_Habits[new_habit_obj.name] = new_habit_obj

    def sql_action(self, sql_statement, values):
        try:
            self.db_cursor.execute(sql_statement, values)
        except sqlite3.Error as er:
            print(bcolors.FAIL + "Database error: " + str(er.sqlite_errorcode) + bcolors.ENDCOLOR)  
            return False
        self.db_connection.commit()
        return True

#Colorcoding in Console
class bcolors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDCOLOR = '\033[0m'


        
