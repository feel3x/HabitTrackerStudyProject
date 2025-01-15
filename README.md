This repository contains the source files for the python backend Habit Tracker project done for a study project. 

## Installation
## Clone Repository
```shell
# HTTPS
git clone https://github.com/feel3x/HabitTrackerStudyProject.git --recursive
```

## Install Requirements
```shell
cd HabitTrackerStudyProject
pip install requirements.txt
```

## Usage
## Command Line Interface
```shell
python tracker_cli.py ACTION SUB-ACTOIN [OPTIONS]
```
Example (filters Habits by periodicity "daily"):
```shell
python tracker_cli.py analytics filter_periodicity -p daily
```
get help in any stage of the CLI with -h or --help
```shell
python tracker_cli.py -h
```

## Command Line Guide
```shell
python guide.py
```
or
```shell
python tracker_cli.py guided
```

##Testing
Run tests using pytest 
```shell
pytest
```


