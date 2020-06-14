import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv','new york city': 'new_york_city.csv','washington': 'washington.csv' }
MONTH_DATA = [ 'all','january', 'february', 'march', 'april', 'may', 'june']
DAY_DATA = ['all','monday', 'tuesday', 'wednesday', 'friday', 'saturday','sunday']

def get_filters():


    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_name =''
    while(city_name not in CITY_DATA):
     city_name = input( 'please choose one of the following cities: [chicago, new york city, washington]:\n').lower()
    if(city_name in CITY_DATA):
     city = CITY_DATA[city_name]

    #get user input for month (all, january, february, ... , june)
    month_name=''
    while(month_name not in MONTH_DATA):
     month_name = input( 'please choose a month or all:[january, february, march, april, may, june, all]:\n').lower()
    if(month_name in MONTH_DATA):
     month = month_name

    #get user input for day of week (all, monday, tuesday, ... sunday)
    day_name=''
    while(day_name not in DAY_DATA):
     day_name = input( 'please choose a day or all:[sunday, monday, tuesday, wednesday, friday, saturday, all]:\n').lower()
    if(day_name in DAY_DATA):
     day = day_name

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
    df = pd.read_csv(city)
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    most_common_month = df['month'].mode()[0]
    print("The most common month is: " + MONTH_DATA[most_common_month])

    #display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print("The most common day of week is: " + str(most_common_day))

    #display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print("The most common start hour is: " + str(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is: " + str(common_start_station))
    #display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is: " + str(common_end_station))

    #display most frequent combination of start station and end station trip
    frequent_combination = (df['Start Station'] +" , "+ df['End Station']).mode()[0]
    print("The most frequent combination of start station and end station trip is : " + str(frequent_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_time = df['Trip Duration'].sum()
    print("The total travel time is: " + str(total_time))

    #display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("The mean travel time is: " + str(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    #Display counts of gender
    if city != 'washington.csv':
     gender_types = df['Gender'].value_counts()
     print(gender_types)
    if city =='washington.csv':
     print ('Washington does not have gender data')

    #Display earliest, most recent, and most common year of birth
    if city != 'washington.csv':
     earliest = df['Birth Year'].min()
     most_recent = df['Birth Year'].max()
     most_common = df['Birth Year'].mode()[0]
     print('Earliest birth is: '+ str(int(earliest)))
     print('Most recent birth is: '+ str(int(most_recent)))
     print('Most common birth is: '+ str(int(most_common)))
    if city == 'washington.csv':
      print ('Washington does not have birth year data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):

    x = 0
    user_answer = input("\n Do you want to see 5 lines of raw data? (Yes or No): \n")
    while user_answer.lower() == 'yes':
        print(df.iloc[x:x + 5])
        x += 5
        user_answer = input("\n Do you want to see 5 lines of raw data? (Yes or No): \n")
        print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        raw_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
