# Timer 2 Calender
Timer Tracker with Google Calendar Integration

## Description
This is a Python desktop application built using PyQt5 to track time and events, and sync them with your Google Calendar. The application includes a timer that you can start and stop, and it automatically creates an event in your Google Calendar with the duration of the timer.

## Features
- Start and stop timer
 - Automatically creates an event in your Google Calendar with the duration of the timer
- Option to edit event name and details before saving to Google Calendar
- Option to select which calendar to sync events to

## Installation
Clone the repository to your local machine.
Make sure you have Python 3 installed on your machine.
Install the required packages using the following command:

```
pip install -r requirements.txt
```

## Enable the Google Calendar API by following the instructions here.
- Download the credentials.json file and save it in the project directory.

## Usage
Run the main.py file using the following command:

```
python main.py
```
- Enter a name for the event and select which calendar to sync it to (if you have multiple calendars).
- Click the "Start" button to start the timer.
- Click the "Stop" button to stop the timer and save the event to your Google Calendar.

## Future Improvements
- Allow users to set a specific start and end time for the event
- Option to add multiple events at once
- Option to track time spent on specific tasks or projects
- Integration with other calendar services

## Credits
This application was built by Md. Zonaid