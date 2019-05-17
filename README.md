# AdvWebDev

App Title: WHATS UP THE ROAD?

Setup:
    Once you have changed directories into the AdvWebDev folder, please run the launch.sh bash script, or run these commands:
        First run: 

            mongod
            mongo

        This will start running the mongoDB server

        Secondly run: 

            source ./env/bin/activate
            flask run
        
        This will start the web server

Usage(functions in order):

    LOGIN: Once the web server is running, you will be brought to the login page.

    CREATE ACCOUNT: If this is your first time accessing the webpage please create an account

    ENTER START LOCATION: Once you are logged in you will be brought to the main homepage, here you will enter a                          start location by clickin 'Enter Start Location', can be your current address or anywhere                       you would like to start your journey from.

    ENTER DESTINATION: After entering your start location the same procedure is repeated for your destination by                       clicking 'Enter Destination'.

    LOCAL TWEETS: After you have entered your location and destination you can click on 'Local Tweets'. This will                 display the Top 5 trending topics on Twitter in your area, as well as a sample of live Tweets in                your area.

    MAPS: There are two maps that you can view by clicking the 'View Maps' dropdown and selecting either 'Traffic         Map' or 'Directions Map'.

    TRAFFIC MAP: The traffic map will show current traffic conditions, and will focus the map on your given start                location.

    DIRECTIONS MAP: The directions map will show you the path to your destination, as well as the distance and time                 it will take to get there in a car. You also have the option to select different modes of                       transportation and the route will change.

    LOGOUT: After all features have been observed the user can logout of the website and will be brought back to            the login screen.

