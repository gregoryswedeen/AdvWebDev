# AdvWebDev

App Title: WHATS UP THE ROAD?

Python Version: 3.6

Server File: app.py

HTML Files: All HTML files can be found within the Templates folder

Databases: MySQL username 'gregory.swedeen' password 'KFDP5DAP'
           MongoDB is run locally and does not require any login credentials
           
Setup:
    Once you have changed directories into the AdvWebDev folder, please run these commands:

        Start Environment:

            source ./env/bin/activate


        Install Python 3.6: 
            sudo apt-get install python3.6 
            alias python3='/usr/bin/python3.6' 

            My account is not one of the approved sudo-ers so I am unable to set version to Python3.6
            If Python3.6 is not installed to '/usr/bin/python3.6', run 'whereis Python3.6'

        Install Requirements:

            sudo apt install python3-pip
            pip install -r requirements.txt

            Again, without Python 3.6 the requirements will not be able to be installed
            Pip3 must be used, this will become available once Python3.6 is installed

        Start Mongo:
            
            mongod 
            mongo 

            This will start the mongo server, an additional terminal may need to be opened to continue as this will bring you to the mongo shell.

        Start Server:

            flask run
        
            This will start the web server

Usage(functions in order):

    LOGIN: Once the web server is running, you will be brought to the login page.

    CREATE ACCOUNT: If this is your first time accessing the webpage please create an account. This User data is                    then stored in the MySQL database.

    ENTER START LOCATION: Once you are logged in you will be brought to the main homepage, here you will enter a                          start location by clickin 'Enter Start Location', can be your current address or anywhere                       you would like to start your journey from. This field utilises Google Maps AutoComplete

    ENTER DESTINATION: After entering your start location the same procedure is repeated for your destination by                       clicking 'Enter Destination'. This field utilises Google Maps AutoComplete

    LOCAL TWEETS: After you have entered your location and destination you can click on 'Local Tweets'. This will                 display the Top 5 trending topics on Twitter in your area, as well as a sample of live Tweets in                your area. This utilises the Twitter API and the Tweepy library for Python. 

    MAPS: There are two maps that you can view by clicking the 'View Maps' dropdown and selecting either 'Traffic         Map' or 'Directions Map'.

    TRAFFIC MAP: The traffic map will show current traffic conditions, and will focus the map on your given start                location. This utilises Google Maps traffic.

    DIRECTIONS MAP: The directions map will show you the path to your destination, as well as the distance and time                 it will take to get there in a car. You also have the option to select different modes of                       transportation and the route will change. This utilises Google Maps API

    LOGOUT: After all features have been observed the user can logout of the website and will be brought back to            the login screen.

