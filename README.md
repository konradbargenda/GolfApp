# GolfApp
This application goal is to give users ability to enter statistics and journal entries and based on performance their practice is planned.

1. Steps to Run the Code:
   - have all files in one folder
   - go to file called main.py and start program there
   - After program is on you can go to the feature that intrests you
   - make sure to provide all information if you want to input data into journal and round.
   - in journal first select date then put in number of hours that you slept, how do you feel it can be short note, and choose number of meals you had. After choosing input name of the meal into corresponding number. Lastly you can put additional notes. Then you can click save entry which will save everything.
   - In golf statistics you can choose how many rounds you want to see, after that you can also choose name of pga tour player and compare data.
   - in adding new round input all data that is required always make sure to put valid data for attempts as avrages will not be correct
   -  In journal entries you can see all entries you have made into journal. by simple clicking it you can read more details.
   -  In practice feature you have to input number of hours that you want to spend on practice and then program will give you percentages for each area also there is option to see exercises that you can do

2. Dependencies:
import tkinter as tk
from tkinter import ttk
from golf_database import Database  
from journal import Journal  
from rounds import Round  
from golf_statistics import StatisticsWindow  
from journal_viewer import JournalViewer  
from practice import Practice
from tkinter import messagebox
import csv
import sqlite3
from tkcalendar import Calendar

pip install tkcalendar

my version of python: 3.10.5(.venv)
