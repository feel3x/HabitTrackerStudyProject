import HabitManager
import Analytics
import datetime
import argparse
import Guide

parser = argparse.ArgumentParser(prog='HabitTracker',
                    description='This Habit Tracker is the backend implementation to help you track your habits.',
                    epilog='Thank you for using the Habit Tracker backend.')
subparsers = parser.add_subparsers(dest="actions", required=True)

# create the parser for the "guided" command
guided_parser = subparsers.add_parser('guided', help='Guided Command Line Interface Experience')

# create the parser for the "create" command
create_parser = subparsers.add_parser('create', help='Create a new habit.')
create_parser.add_argument('-n', '--name', required=True, type=str, help='Name of new habit.')
create_parser.add_argument('-p', '--periodicity', required=True, type=str, help='How often this habit has to be completed. Options: \"Daily\", \"Weekly\", \"Monthly\", \"Yearly\", or set a custom periodicity like this example: \"Days=2,Weeks=3,Years=1...\"')

# create the parser for the "complete" command
complete_parser = subparsers.add_parser('complete', help='Complete a habit.')
complete_parser.add_argument('-n', '--name', required=True, type=str, help='Name of the habit to be completed.')

# create the parser for the "delete" command
delete_parser = subparsers.add_parser('delete', help='Delete a habit.')
delete_parser.add_argument('-n', '--name', required=True, type=str, help='Name of the habit to be deleted.')
delete_parser.add_argument('-y', '--yes', action=argparse.BooleanOptionalAction, default=False, help='Delete Habit without confirmation needed.')

# create the parser for the "analytics" command
analytics_parser = subparsers.add_parser('analytics', help='Tools for analyzing your Habits')

#parsers for analytics
analytics_subparser = analytics_parser.add_subparsers(dest="analytics_actions")

#analytics parser to list habits
list_analytics_parser = analytics_subparser.add_parser('list', help='List all habits.')

#analytics parser to get longest streak
list_analytics_parser = analytics_subparser.add_parser('longest_streak', help='List all habits sorted by their longest streak.')

#analytics parser to filter habits by periodicity
list_analytics_parser = analytics_subparser.add_parser('filter_periodicity', help='List all habits with the given periodicity.')
list_analytics_parser.add_argument('-p', '--periodicity', required=True, type=str, help='The periodicity to filter by. Options: \"Daily\", \"Weekly\", \"Monthly\", \"Yearly\", or set a custom periodicity like this example: \"Days=2,Weeks=3,Years=1...\"')

#analytics parser to filter habits by periodicity
list_analytics_parser = analytics_subparser.add_parser('streak_infos', help='Get Infos about streaks and streak-breask of certain habit.')
list_analytics_parser.add_argument('-n', '--name', required=True, type=str, help='The name of the habit to get information about.')

#analytics parser to get longest streak
list_analytics_parser = analytics_subparser.add_parser('worst_habits', help='List all habits sorted by their most interuptions and longest streak-breaks.')

args = parser.parse_args()
manager = HabitManager.HabitManager()

#start functions according to choices in CLI

#Guide
if(args.actions=="guided"):
    Guide.start_guide(manager)

#Create habit
if(args.actions=="create"):
    manager.create_habit(args.name, args.periodicity)

#Delete habit
if(args.actions=="delete"):
    manager.delete_habit(args.name, args.yes)

#Complete habit
if(args.actions=="complete"):
    manager.complete_habit(args.name)

#Analytics
if(args.actions=="analytics"):
    #List habits
    if(args.analytics_actions=="list"):
        Analytics.get_all_habits(manager)
    #List by Longest Streak
    if(args.analytics_actions=="longest_streak"):
        Analytics.get_longest_streaks(manager)
    #Filter periodicity
    if(args.analytics_actions=="filter_periodicity"):
        Analytics.filter_habits_by_periodicity(manager, args.periodicity)
    #Get streak information about habit
    if(args.analytics_actions=="streak_infos"):
        Analytics.get_streak_info(manager, args.name)
    #List worst habits
    if(args.analytics_actions=="worst_habits"):
        Analytics.get_least_completed_habits(manager)