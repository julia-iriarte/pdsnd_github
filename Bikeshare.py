import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). 
    while True:
        city = input('Would you like to see data for Chicago, New York City or Washington? ').lower()
        if city in ['chicago', 'new york city', 'washington']:
            break 
        else:
            print('This is not a valid option for city. Please type it correctly.')
    print('\nCity filter: ', city.title())

    # Get user input to filter which month they want to analyze (from January to June). 
    while True:
        month_filter = input('\nWould you like to filter the data by month? Type yes or no. ').lower()
        if month_filter == 'yes':
            while True:
                month = input('\nWhich month? January, February, March, April, May or June? ').lower()
                if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                    break
                else:
                    print('\nThis is not a valid option for month. Please type it correctly. ')
            break
        elif month_filter == 'no':
            month = 'all'
            break
        else:
            print('\nThis is not a valid option. Please type it correctly. ')

    # Get user input to filter day of the week to analize (all, monday, tuesday, ... sunday).         
    while True:
        day_filter = input('\nWould you like to filter the data by day? Type yes or no. ').lower()
        if day_filter == 'yes':
            while True:
                day = input('\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? ').lower()
                if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                    break
                else:
                    print('\nThis is not a valid option for day. Please type it correctly. ')
            break
        elif day_filter == 'no':
            day = 'all'
            break
        else:
            print('\nThis is not a valid option. Please type it correctly. ')
 
    # Sum up time filters.    
    print(f'Time filters: \n Day: {day} \n Month: {month}')

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    # Loads data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Converts the Start Time column to datetime and extracts month, day of week and hour from Start Time to create new columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # Filters by month if applicable  to create the new dataframe.
    if month != 'all':
        month_index = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        # filters by month to create the new dataframe
        df = df[df['month'] == month_index]

    # Filters by day of week if applicable to create the new dataframe.
    if day != 'all':
        day_index = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'].index(day) 
        df = df[df['day_of_week'] == day_index]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displays the most common month.
    popular_month = df['month'].mode()[0]
    print(f"Most popular month: {['january', 'february', 'march', 'april', 'may', 'june'][popular_month - 1]}")

    # Displays the most common day of week.
    popular_day = df['day_of_week'].mode()[0]
    print(f"Most popular day: {['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'][popular_day]}")
    
    # Displays the most common start hour.
    popular_hour = df['hour'].mode()[0]
    print(f'Most popular hour: {popular_hour}:00')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays most commonly used start station.
    popular_start = df['Start Station'].mode()[0]
    print(f'Most popular start station: {popular_start}')

    # Displays most commonly used end station.
    popular_end = df['End Station'].mode()[0]
    print(f'Most popular end station: {popular_end}')

    # Displays most frequent combination of start station and end station trip.
    popular_combination = (df['Start Station'] + ' - ' + df['End Station']).mode()[0]
    print(f'Most popular combination start-end station: {popular_combination}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displays total travel time (in seconds).
    print(f"Total travel time: {df['Trip Duration'].sum()} seconds")
    
    # Displays mean travel time (in seconds).
    print(f"Average travel time: {df['Trip Duration'].mean()}seconds")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types.
    print('Counts of user types: ')
    print(df['User Type'].value_counts())

    if city in ['chicago', 'new york city']:
        # Displays counts of gender and earliest, most recent, and most common year of birth.
        # Data only available for Chicago and New York City.
        print('\nCounts of gender: ')
        print(df['Gender'].value_counts())
        print(f"\nEarliest year of birth: {int(df['Birth Year'].min())}")
        print(f"Most recent year of birth: {int(df['Birth Year'].max())}")
        print(f"Most common year of birth: {int(df['Birth Year'].mode()[0])}")
    else:
        print(f'\nGender and birth data not available for {city.title()}')
              
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """Get filters and displays statistics as long as the user ask for them."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        # Get user input for showing raw data or no.
        raw_data = input('Would you like to see 5 lines of raw data? Enter yes or no.\n').lower()
        n = 0
        while raw_data == 'yes':
            print(df[n:n+5])
            n = n + 5
            raw_data = input('Would you like to see the next 5 lines of raw data? Enter yes or no.\n').lower()
            
        # Get user input for restarting the program or ending it.                       
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
