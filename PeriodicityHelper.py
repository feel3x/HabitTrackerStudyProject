import dateutil
import dateutil.relativedelta

def get_relative_delta(periodicity):
    """
    Function to retrieve the corresponding relativedelta Object for a str.

    Parameters:
    periodicity (str): The periodicity of the Habit

    Returns:
    Relativedelta: Relativedelta Object for the given Periodicity.
    """ 
    if(str(periodicity).lower() == "daily"):
        return dateutil.relativedelta.relativedelta(days=1)
    if(str(periodicity).lower() == "weekly"):
        return dateutil.relativedelta.relativedelta(weeks=1)
    if(str(periodicity).lower() == "monthly"):
        return dateutil.relativedelta.relativedelta(months=1)
    if(str(periodicity).lower() == "yearly"):
        return dateutil.relativedelta.relativedelta(years=1)
    
    #Custom Periodicity 
    #remove whitespaces 
    periodicity = periodicity.replace(" ", "").lower()
    #split by comma
    periodicity_array = periodicity.split(",")
    entered_days = 0
    entered_weeks = 0
    entered_months = 0
    entered_years = 0
    for data in periodicity_array:
        split_data = data.split("=")
        try:
            if(len(split_data)< 2):
                return None
            if(split_data[0] == "days"):
                entered_days = int(split_data[1])
            if(split_data[0] == "weeks"):
                entered_weeks = int(split_data[1])
            if(split_data[0] == "months"):
                entered_months = int(split_data[1])
            if(split_data[0] == "years"):
                entered_years = int(split_data[1])
        except:
            return None
    try:
        return dateutil.relativedelta.relativedelta(years=entered_years, months=entered_months, weeks=entered_weeks, days=entered_days)
    except:
        return None
    