# Daymap2Calendar
## What is it?
A small Python 3 program that takes your Daymap timetable and adds to to a Google Calendar. This program only works for GIHS students
for several reasons:
- Daymap version differ between schools, meaning that the timetable may be in a different format or layout
- This program was built around the GIHS timetable structure. Lesson times would need to be rearranged for other schools.
For general use, it is recommended that you use the GUI (general user interface) version, as it is far more user friendly. However, feel
free to download the code and play around with it as you wish.

## Dependencies
Daymap2Calendar depends on the following third-party libraries:
- Pandas
- requests_ntlm
- pickle
- Google API libraries

To install the dependencies, run the following: ```pip install -r requirements.txt```. Please note: You will need to enable the Google Calendar API for your Google account and download the resulting ```credentials.json``` file. This is neccesary to authenticate the program with the users Google account. Go [here](https://developers.google.com/calendar/quickstart/python) to learn more.

## Contributing
Wanna help make Daymap2Calendar better? If it's a small problem, open an issue and tell me about whats going wrong. If you want to make
contributions to the project directly, fork the repo, make your changes and open a pull request. I'll review what you've changed and merge 
it if I can! Please ensure you thoroughly test your changes before submitting a pull request, it saves both of us time in the long run.
