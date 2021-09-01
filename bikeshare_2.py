import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'dc': 'washington.csv' }
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June']
DAYS_OF_WEEK = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). 
    while True:
        city = input('Please enter the city to analyze. (Chicago, New York, or DC): ').lower()
        if city in CITY_DATA.keys():
            break
        else:
            print(f'{city.title()} is not available.')
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please enter month you would like to analyze.'\
            ' (January, February, March,....). For all months press Enter ')
        if month.title() in MONTHS:
            break
        elif month == '':
            month = 'all'
            break
        else:
            print(f'{month} is not a valid input.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please enter the day of the week you would like to analyze.'\
            ' (Monday, Tuesday, Wednesday,....). For all days press Enter: ').lower()
        if day in DAYS_OF_WEEK:
            break
        elif day == '':
            day = 'all'
            break
        else:
            print(f'{day} is not a valid input.')

    print('-'*40)
    return city, month.title(), day.title()

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
    df = pd.read_csv(CITY_DATA[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df['Month'] = df["Start Time"].dt.month
    df['Day'] = df["Start Time"].dt.day_name()
    df['Hour'] = df["Start Time"].dt.hour
    if month != 'All' and day != 'All':
        return df.loc[(df['Month'] == MONTHS.index(month) + 1) & (df['Day'] == day)]
    elif month != 'All':
        return df.loc[df['Month'] == MONTHS.index(month) + 1]
    elif day != 'All':
        return df.loc[df['Day'] == day]
    else:
        return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if df['Month'].nunique(1) != 1:
        popular_month = df['Month'].mode()[0]
        print(f'The most common month is: {MONTHS[popular_month -1].title()}')
    else:
        filter_month = df['Month'].values[0]
        print(f'For the month of {MONTHS[filter_month - 1]}')
    # display the most common day of week
    if df['Day'].nunique(1) != 1:
        popular_day = df['Day'].mode()[0]
        print(f'The most common retal day is: {popular_day}')
    else:
        filter_day = df['Day'].values[0]
        print(f'On {filter_day}s ')

    # display the most common start hour
    popular_hour = df['Hour'].mode()[0]
    print(f'The most common rental hour is: {popular_hour}')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print(f'The most commonly used start station is:\n{popular_start}')

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print(f'The most commonly used end station is:\n{popular_end}')

    # display most frequent combination of start station and end station trip
    # create new df to create the start/end combo and counts
    popular_combo = df.groupby(['Start Station', 'End Station']).size().to_frame('Counts').reset_index()
    # find max index of the start/end combo for printability
    combo_stat = popular_combo.loc[popular_combo['Counts'].idxmax()]
    print(f'The most frequent combination of start station\
         and end station trip is:\n{combo_stat.to_string()}')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'Total trip duration: {total_travel_time}')

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print(f'Average trip duration: {average_travel_time}')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'User type breakdown:\n{user_types.to_string()}')
    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print(f'\nGender breakdown:\n{gender_count.to_string()}')
    else:
        print('\nGender breakdown:\nGender information not available')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        data = [df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].mode()[0]]
        data_ser = pd.Series(data, index=['Earliest', 'Most Recent', 'Most Common'])
        print(f'\nBirth year breakdown:\n{data_ser.to_string()}')
    else:
        print('\nBirth year breakdown:\nBirth year information not available.')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-'*40)

def raw_data(df):
    """
    Solicit user input and display raw data 5 row at a time.
    """
    resp = input('\nWould you like to see the raw data?: ').lower()
    i = 0
    while resp == 'yes' and i < df.shape[0]:
        print(df.iloc[i:i+5])
        i += 5
        resp = input('Would you like to see more?: ')

def main():
    """
    Main function to output data returned from time_stats(), station_stats()
    trip_duration_stats(), and user_stats()
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
