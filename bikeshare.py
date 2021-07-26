"""
Title: User Bikeshare Data Project
Date: 27/07/2021
Author: James Ross
"""

import time
import pandas as pd #pandas version 1.3.0
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_filter = False
day_filter = False
city_status = ""


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (Chicago, New York City, Washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please select the specific city you wish to analyse: Chicago, New York, Washington\n').title()
        print()
        if city == 'Chicago' or city == 'New York' or city == 'Washington':
            print("You have selected {}. You will need to restart the program to select another option.".format(city))
            print()
            break
        else:
            print('Please enter the exact spelling of one of either the cities of Chicago, Ney York or Washington.')
            print()
            continue
    
    # get user input for month (all, january, february, ... , june)
    while True:
        month_choice = input('Will you filter by "Month", or analyse all the months? Type "All" for no month filter.\n').title()
        print()
        if month_choice == 'All':
            month = 'All'
            break
        elif month_choice == 'Month':
            while True:
                month = input('Select month: January, February, March, April, May, June\n').title()
                print()
                if month  == 'January' or month == 'February' or month == 'March' or month == 'April' or month == 'May' or month == 'June':
                    print("You have selected {}".format(month))
                    print()
                    break
                else:
                    print('Please enter the exact spelling of the month you wish to choose.')
                    print()
                    continue
            break 
        else:
            print('Please select the option of "Month" or "All".')
            print()
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Will you filter by a specific day or analyse all the days? Select "All" for no day filter or a specifc day: Monday, Tuesday, ... Sunday.\n').title()
        print()
        if day == 'All' or day == 'Monday' or day == 'Tuesday' or day == 'Wednesday' or day == 'Thursday' or day == 'Friday' or day == 'Saturday' or day == 'Sunday':
            print("You have selected {}.".format(day))
            print()
            break 
        else:
            print('Please select "all" or a specific day of the week from "Monday" through to "Sunday"')
            print()
            continue    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # city filter status
    global city_status
    city_status = city
    
    # normalising parameters with file data 
    city = city.lower()
    month = month.lower()
      
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        # month filter status for functions
        global month_filter
        month_filter = True

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

        # day filter status for functions
        global day_filter
        day_filter = True
    
    return df


def filter_status(df):    
    # convert months to string
    months = {1: 'January', 2: 'February', 3: 'March', 4:  'April', 5: 'May', 6: 'June'}
    filter_month = df['month'].value_counts()
    converted_month = months[filter_month.idxmax(0)]

    # convert day to single value
    filter_day = df['day_of_week'].mode() 

    # print filter status
    if month_filter == True and day_filter == True:
        print('Filter: {} and {}'.format(converted_month, filter_day[0])) 
    elif month_filter == True:
        print('Filter: {} and All Days'.format(converted_month))
    elif day_filter == True:
        print('Filter: {} and All Months'.format(filter_day[0]))
    else:   
        print('Filter: NA (All Months and All Days)')
    print()


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # filter status
    filter_status(df)
    
    # display the most common month
    if month_filter != True:
        common_month = df['month'].value_counts()  
        months = {1: 'January', 2: 'February', 3: 'March', 4:  'April', 5: 'May', 6: 'June'}
        converted_month = months[common_month.idxmax(0)]                    
        print("Most common month: {} Count: {}".format(converted_month,common_month.max(0)))    
    
    # display the most common day of week
    if day_filter != True:
        common_day = df['day_of_week'].value_counts()
        print("Most common day: {} Count: {}".format(common_day.idxmax(0),common_day.max(0)))
    
    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].value_counts()
    print("Most common start hour (24 hour time): {} Count: {}".format(common_hour.idxmax(0),common_hour.max(0)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # filter status
    filter_status(df)
        
    # display most commonly used start station
    common_start = df['Start Station'].value_counts()
    print("Most common start station: {}    Count: {}".format(common_start.idxmax(0),common_start.max(0)))

    # display most commonly used end station
    common_end = df['End Station'].value_counts()
    print("Most common end station: {}      Count: {}".format(common_end.idxmax(0),common_end.max(0)))

    # display most frequent combination of start station and end station trip
    common_combination = df[['Start Station', 'End Station']].value_counts()
    print("Most frequent combination of start and end station:\n{}      Count: {}".format(common_combination.idxmax(0),common_combination.max(0)))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # filter status
    filter_status(df)
    
    # display total travel time
    total_travel = df['Trip Duration'].sum()
    hours = total_travel // 3600
    minutes = ((total_travel - (hours * 3600)) // 60)
    seconds = ((total_travel - (hours * 3600) - (minutes * 60))) 
    print("Total Travel Time: {} seconds or {} hours {} minutes and {} seconds ".format(total_travel, hours, minutes, seconds))
    

    # display mean travel time
    mean_travel = round((df['Trip Duration'].mean()))
    minutes = mean_travel // 60
    seconds = mean_travel % 60
    print("Mean Travel Time: {} seconds or {} minutes and {} seconds".format(mean_travel, minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # filter status
    filter_status(df)
    
    # Display counts of user types
    print("User Types: ")
    print(df['User Type'].value_counts())
    print()
    
    # Display counts of gender
    if city_status != "Washington":
        print("Gender: ")
        print(df['Gender'].value_counts())
        print("Please note that gender data is only available for Subscribers. Not Customers.")
    else:
        print("Washington does not have gender data.")
    print()

    # Display earliest, most recent, and most common year of birth
    if city_status != "Washington":
        print("Earliest Birth Year: {}".format(int(df["Birth Year"].min())))
        print("Most Recent Birth Year: {}".format(int(df["Birth Year"].max())))
        print("Most Common Birth Year: {}".format(int(df["Birth Year"].mode())))
    else:
        print("Washington does not have birth data.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays 5 rows of individual trip data upon user prompting"""
    
    # check if user wants to view more data
    while True:
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        print()
        if view_data == 'no':
            break
        elif view_data == 'yes':
            start_loc = 0
            end_loc = 5
            
            # data loops 5 data rows
            while True:
                print(df.iloc[start_loc:end_loc])
                start_loc += 5
                end_loc += 5
                
                # stop if no more data to present
                if end_loc > len(df):
                    print()
                    print("No more data to show.")
                    print()
                    return
                
                # user prompted to continue or not
                while True:
                    view_data = input("Do you wish to continue? Enter yes or no\n").lower()
                    print()
                    if view_data == 'yes':
                        break
                    elif view_data == 'no':
                        return
                    else:
                        print("Please select either 'yes' or 'no'.")
                        print()
                continue
        else:       
            print("Please select either 'yes' or 'no'.")
            print()
            continue

def main():
    while True:             
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
