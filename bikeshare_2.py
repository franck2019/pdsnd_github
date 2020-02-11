import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }


# my_list 
cities = ["chicago", "new york", "washington"]
filters = ["month", "day", "both", "none"]
months = ["all", "january", "february", "march", "april", "may","june"]
days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

# question
question_1 = "Would you like to see data for Chicago, New York, or Washington?\n"
question_2 = "Would you like to filter the data by month, day, both or not at all? Type none for no time filter\n"
question_3 = "Which month - January, February, March, April, May, or June?\n"
question_4 = "Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n"



def handle_invalid_inputs(question,my_list):
    """
    Gets, tests if the input of a question(question) belongs to a list(my_list) that we attend 
    and handle invalid inputs of the user.

    Args:
        (str) question - the question for what we want to get and test the input of the user.
        (list) my_list - the list of answer that we wish to have.
        
    Returns:
        (str) final_answer - a string containing a good input typed by the user.
    """

    final_answer = None
    while final_answer not in my_list:
        final_answer = input(question).lower()

    return final_answer



def get_month():
    """
    Gets the input month choosed by the user in case where filter_choosed equal to "month".
        
    Returns:
        month - name of the month
    """
    return handle_invalid_inputs(question_3, months)



def get_day():
    """
    Gets the input day choosed by the user in case where filter_choosed equal to "day".
        
    Returns:
        day - string contening the name of the day
    """
    return handle_invalid_inputs(question_4, days)



def get_both():
    """
    Gets the input month and day choosed by the user in case where filter_choosed equal to "both".
        
    Returns:
        (str) get_month()
        (str) get_day()
    """
    return get_month(), get_day()



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter_choosed by, or "all" to apply no month filter_choosed
        (str) day - name of the day of week to filter_choosed by, or "all" to apply no day filter_choosed
        (str) filter_choosed - name of the the choosed filter_choosed
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = handle_invalid_inputs(question_1, cities)
    
    # get the user input of the filter_choosed (month, day, both, or not at all(none))

    filter_choosed = handle_invalid_inputs(question_2, filters)
    
    # if filter_choosed == "month"
    if filter_choosed == "month":
        # get user input for month (all, january, february, ... , june)
        month = get_month()
        day = "all"
        
    # if filter_choosed == "day"
    if filter_choosed == "day":
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = get_day()
        month = "all"
    
    # if filter_choosed == "both"
    if filter_choosed == "both":
        # get user input for day of week and month
        month, day = get_both()
        
    # if filter_choosed == none
    if filter_choosed == "none":
        month = "all"
        day = "all"

    print('-'*40)
    return city, month, day, filter_choosed




def load_data(city, month, day):
    """
    Loads data for the specified city and filter_chooseds by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter_choosed by, or "all" to apply no month filter_choosed
        (str) day - name of the day of week to filter_choosed by, or "all" to apply no day filter_choosed
    Returns:
        df - Pandas DataFrame containing city data filter_chooseded by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour


    # filter_choosed by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1

        # filter_choosed by month to create the new dataframe
        df = df[df['month'] == month]

    # filter_choosed by day of week if applicable
    if day != 'all':
        # filter_choosed by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df





def popular_counts_column(column):
    """ 
    calculate statistics(popular entry of that column and his occurrence) on the most frequent times of travel.
    
    Args:
        (pd.Series) column - column of a DataFrame
        
    Returns:
        popular_anything - string containing the popular entry
        counts_anything - int containing number of occurence of that popular entry

    """
    popular_anything = column.mode()[0]
    counts_anything = column.value_counts()[popular_anything]
    
    return popular_anything, counts_anything




def time_stats(df, filter_choosed):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    """
    # display the most common month and occurrence
    popular_month = df['month'].mode()[0]
    # count the occurrence of the most popular month
    counts_month = df['month'].value_counts()[popular_month]
    """
    # display the most common month and number of occurrence
    popular_month, counts_month = popular_counts_column(df['month'])
    print('The Most Popular month:{}, Counts:{},'.format(popular_month, counts_month), end = ' ')
    # display the most common day of week and number of occurence
    popular_day, counts_day = popular_counts_column(df['day_of_week'])
    print('The Most Popular day:{}, Counts:{},'.format(popular_day, counts_day), end = ' ')
    # display the most common start hour and number of occurrence
    popular_hour, counts_hour = popular_counts_column(df['hour'])
    print('The Most Popular hour:{}, Counts:{},  Filter:{}\n'.format(popular_hour, counts_hour, filter_choosed))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)





def station_stats(df, filter_choosed):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start, counts_start = popular_counts_column(df['Start Station'])
    print('Start Station:{}, Counts:{},'.format(popular_start, counts_start), end = ' ')

    # display most commonly used end station
    popular_end, counts_end = popular_counts_column(df['End Station'])
    print('End Station:{}, Counts:{},'.format(popular_end, counts_end, filter_choosed), end = ' ')

    # display most frequent combination of start station and end station trip
    popular_start_end, counts_start_end = popular_counts_column(df['Start Station'] + '-' + df['End Station'])
    #print("Popular Trip:('{}'), Counts:{},  Filter:{}\n".format(popular_start_end, counts_start_end, filter_choosed))
    print("Popular Trip:('{}'-'{}'), Counts:{},  Filter:{}\n".format(popular_start_end.split('-')[0],popular_start_end.split('-')[1], counts_start_end, filter_choosed))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def trip_duration_stats(df, filter_choosed):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    travel_number = df['Trip Duration'].size
    print('Total Duration:{}, Count:{},'.format(total_travel_time, travel_number), end = ' ')
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Avg Duration:{}, Filter:{}\n'.format(mean_travel_time, filter_choosed))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df, city, filter_choosed):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Statistics for User Types ...... \n')
    user_types_dict = dict(df['User Type'].value_counts())
    for key, value in user_types_dict.items():
        print('{}:{}'.format(key,value), end = ' ')
    print('filter:', filter_choosed)

    # Display counts of gender
    print('\nStatistics for gender ...... \n')
    if city != 'washington':
        gender_dict = dict(df['Gender'].value_counts())
        for key, value in gender_dict.items():
            print('{}:{}'.format(key,value), end = ' ')
        print(' filter:', filter_choosed)
    else:
        print('No data about gender')

    # Display earliest, most recent, and most common year of birth
    print('\nStatistics for year of birth ...... \n')
    if city != 'washington':
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        popular_year = df['Birth Year'].mode()[0]
        print('Earliest Year:{}, Most Recent Year:{}, Most Popular Year:{}, filter:{}'.format(earliest_year, most_recent_year, popular_year, filter_choosed))
    else:
        print('No data about birth of year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def individual_trip_data(df):
    """Displays individual trip data of each user."""
    data = df.to_dict('records')
    i = 0
    j = 5
    length = len(data)

    while True:
        see_trip = input('\nWould you like to individual trip data? Type yes or no.\n')
        if see_trip.lower() != 'yes':
            break
        else:
            if i < j and i < length:
                for i in range(j):
                    print(data[i])
        i = j
        j += 5    


def main():
    while True:
        city, month, day, filter_choosed = get_filters()
        #print (city, month, day, filter_choosed)
        
        df = load_data(city, month, day)
        #print (df)
        #print(df.columns)
        #print(filter_choosed)no
        
        time_stats(df, filter_choosed)
        station_stats(df, filter_choosed)
        trip_duration_stats(df, filter_choosed)
        user_stats(df, city, filter_choosed)
        individual_trip_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
            

if __name__ == "__main__":
	main()
