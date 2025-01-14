import datetime
import PeriodicityHelper

class Habit:
    """
    Class representing a Habit Object.

    Attributes:
    id (int): the Unique id of the Habit in the database.
    name (str): The name of the Habit.
    periodicity(str): The periodicity of the Habit.
    creation_date(datetime): The time the habit was created.
    completion_dates(list): A list of the dates when the Habit was completed.
    """ 
    def __init__(self, id, name, periodicity, creation_date = None):
        self.id = id
        self.name = name
        self.periodicity = periodicity
        if(creation_date is None):
            creation_date = datetime.datetime.now()
        if(not isinstance(creation_date, str)):
            creation_date = creation_date.strftime("%Y-%m-%d %H:%M:%S.%f")
        self.creation_date = creation_date
        self.completion_dates = []

    def complete_task(self, past_date = None):
        """
        Function to complete the task of this Habit for the current time for a given datetime.

        Parameters:
        past_date (datetime): Optional date the Habit should be completed for.

        Returns:
        Datetime: Datetime Object of the completed date and time.
        """ 
        if(past_date is None):
            past_date = datetime.datetime.now()
        if(not isinstance(past_date, str)):
            past_date = past_date.strftime("%Y-%m-%d %H:%M:%S.%f")
        newDateTime = past_date
        self.completion_dates.append(newDateTime)
        return newDateTime
    
    #returns infos about the streaks and breaks of this habit
    def get_streak_infos(self, start_date=datetime.datetime.min, end_date=None):
        """
        Returns infos about the streaks and breaks of this habit.

        Parameters:
        start_date (datetime): The start of the period. (FOR FUTURE IMPLEMENTATIONS)
        end_date(datetime): The end of the period. (FOR FUTURE IMPLEMENTATIONS)

        Returns:
        Tuple: current_streak, longest_streak, current_streak_break, longest_streak_break, total_interuptions.
        """ 
        if(end_date is None):
            end_date = datetime.datetime.now()
        current_streak = 0
        current_streak_break = 0
        longest_streak = 0
        longest_streak_break = 0
        total_interuptions = 0
        counter = 1
        if(isinstance(start_date, str)):
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S.%f")
        if(isinstance(end_date, str)):
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S.%f")
        period_start_date = start_date
        period_end_date = datetime.datetime.min
        #iterate through all completion dates and start counting the streak in the given period
        while period_end_date<end_date:
            #create start and end dates for the period to be checking for in this iteration
            period_start_date = datetime.datetime.strptime(self.creation_date, "%Y-%m-%d %H:%M:%S.%f") + (PeriodicityHelper.get_relative_delta(self.periodicity) * (counter-1))
            period_end_date = datetime.datetime.strptime(self.creation_date, "%Y-%m-%d %H:%M:%S.%f") + (PeriodicityHelper.get_relative_delta(self.periodicity) * counter)

            if(period_start_date < start_date):
                continue

            found_date = False
            for date in self.completion_dates:
                if(isinstance(date, str)):
                    date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
                if(date > period_start_date and date < period_end_date):
                    #last recorded completion date is within this period -> streak incresed           
                    current_streak_break = 0
                    current_streak += 1
                    if(current_streak > longest_streak):
                        longest_streak = current_streak
                    found_date = True
                    break
            if(not found_date):
                #last recorded completion date is older than the checked period -> Streak broken
                if(current_streak>0):
                    #record an interuption
                    total_interuptions +=1
                current_streak = 0
                current_streak_break += 1
                if(current_streak_break > longest_streak_break):
                    longest_streak_break = current_streak_break
            
            #any other date is a duplicate and can be skipped
            counter +=1

        return current_streak, longest_streak, current_streak_break, longest_streak_break, total_interuptions
