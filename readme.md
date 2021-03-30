# The Daily App

This is a simple app to receive daily emails on different subjects of choice.  The email addresses 
are gathered from an excel file (started with a google docs file):

The excel file is in the project directory and contains these fields:
["name", "surname", "email", "interest", "search", "zip"]

name: is used in code to address the email
surname: there for future us
email: email address to send the mail
interest: topics to search
search: either "qInTitle" or q --> this queries either just the title or title and text of article
zip: used for weather and earthquake info

The other excel file the app uses is the API_list.
Fields:
["API_Name", "API_number", "email_address", "password"]
API_Name: name of the api - usually the website name
API_number: the api key, for this the news site it requires "api_Key={the key here}"
email_address: the email address I'm sending from - I've created a new google email just for this app.
password: password for the email address so it can send the emails.
This file I keep in a folder on my desktop I link all my programs that require API or Email info to it.

for more info: https://github.com/ValleyRobotics/daily_app/blob/gh-pages/index.md