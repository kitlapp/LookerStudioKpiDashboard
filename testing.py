import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import calendar

from cleaning import month_components_calculation, day_components_calculation


def plot_circular_month(dataframe, month_columns):
    """
    Plots the circular visualization of the cyclical components (x_comp and y_comp) for each month column.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame containing the cyclical components.
        month_columns (list): List of month column names for which cyclical encoding was done.
    """
    for col in month_columns:
        # Get the x_comp and y_comp columns for each month column
        x_comp_col = f'x_comp_{col}'
        y_comp_col = f'y_comp_{col}'

        # Get the values for the plot
        x_values = dataframe[x_comp_col].dropna()
        y_values = dataframe[y_comp_col].dropna()

        # Create the figure and polar axis
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

        # Convert cartesian to polar coordinates (theta = angle)
        angle = np.arctan2(y_values, x_values)  # Calculate the angle
        radius = np.sqrt(x_values ** 2 + y_values ** 2)  # Calculate the radius (magnitude)

        # Plot the points in polar coordinates
        ax.scatter(angle, radius, label=f'Month {col}')
        ax.set_title(f'Cyclical Plot for Month {col}')
        ax.set_xlabel('Angle (radians)')
        ax.set_ylabel('Magnitude (Radius)')

        # Display the plot
        plt.show()


def plot_circular_day(dataframe, day_columns):
    """
    Plots the circular visualization of the cyclical components (x_comp and y_comp) for each day column.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame containing the cyclical components.
        day_columns (list): List of day column names for which cyclical encoding was done.
    """
    for col in day_columns:
        # Get the x_comp and y_comp columns for each day column
        x_comp_col = f'x_comp_{col}'
        y_comp_col = f'y_comp_{col}'

        # Get the values for the plot
        x_values = dataframe[x_comp_col].dropna()
        y_values = dataframe[y_comp_col].dropna()

        # Create the figure and polar axis
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

        # Convert cartesian to polar coordinates (theta = angle)
        angle = np.arctan2(y_values, x_values)  # Calculate the angle
        radius = np.sqrt(x_values ** 2 + y_values ** 2)  # Calculate the radius (magnitude)

        # Plot the points in polar coordinates
        ax.scatter(angle, radius, label=f'Day {col}')
        ax.set_title(f'Cyclical Plot for Day {col}')
        ax.set_xlabel('Angle (radians)')
        ax.set_ylabel('Magnitude (Radius)')

        # Display the plot
        plt.show()


def test_month_components_calculation(dataframe, month_columns):

    result = month_components_calculation(dataframe=dataframe, month_columns=month_columns)

    for col in month_columns:
        x_comp_col = f'x_comp_{col}'
        y_comp_col = f'y_comp_{col}'

        assert x_comp_col in result.columns, f"Missing column: {x_comp_col}"
        assert y_comp_col in result.columns, f"Missing column: {y_comp_col}"

        # Ensure no NaN values in the newly created columns
        assert not result[x_comp_col].isna().any(), f"NaN values found in {x_comp_col}"
        assert not result[y_comp_col].isna().any(), f"NaN values found in {y_comp_col}"

        # Ensure sine and cosine values are within the expected range [-1, 1]
        assert result[x_comp_col].between(-1, 1).all(), f"Values in {x_comp_col} exceed range [-1,1]"
        assert result[y_comp_col].between(-1, 1).all(), f"Values in {y_comp_col} exceed range [-1,1]"

        # Ensure month values are valid (between 1 and 12)
        assert result[col].between(1, 12).all(), f"Invalid month values in {col}"

        assert pd.api.types.is_numeric_dtype(result[x_comp_col]), f"Column {x_comp_col} contains non-numeric values"
        assert pd.api.types.is_numeric_dtype(result[y_comp_col]), f"Column {y_comp_col} contains non-numeric values"

    plot_circular_month(result, month_columns)

    return 'Test Passed'


def test_day_components_calculation(dataframe, year_columns, month_columns, day_columns):

    result = day_components_calculation(
        dataframe=dataframe,
        year_columns=year_columns,
        month_columns=month_columns,
        day_columns=day_columns)

    for col in day_columns:
        x_comp_col = f'x_comp_{col}'
        y_comp_col = f'y_comp_{col}'

        assert x_comp_col in result.columns, f"Missing column: {x_comp_col}"
        assert y_comp_col in result.columns, f"Missing column: {y_comp_col}"

        # Ensure no NaN values in the newly created columns
        assert not result[x_comp_col].isna().any(), f"NaN values found in {x_comp_col}"
        assert not result[y_comp_col].isna().any(), f"NaN values found in {y_comp_col}"

        # Ensure sine and cosine values are within the expected range [-1, 1]
        assert result[x_comp_col].between(-1, 1).all(), f"Values in {x_comp_col} exceed range [-1,1]"
        assert result[y_comp_col].between(-1, 1).all(), f"Values in {y_comp_col} exceed range [-1,1]"

        # Ensure day values are valid (between 1 and 31)
        assert result[col].between(1, 31).all(), f"Invalid day values in {col}"

        # Ensure year, month, and day columns are numeric (int type)
        assert pd.api.types.is_integer_dtype(result[col]), f"Column {col} contains non-integer values"
        assert pd.api.types.is_integer_dtype(
            result[year_columns[0]]), f"Year column {year_columns[0]} contains non-integer values"
        assert pd.api.types.is_integer_dtype(
            result[month_columns[0]]), f"Month column {month_columns[0]} contains non-integer values"

        # Verify correct month lengths for cyclical encoding
        for month, day in zip(month_columns, day_columns):
            if month in [1, 3, 5, 7, 8, 10, 12]:  # Months with 31 days
                assert result.loc[result[month] == month, day].between(
                    1, 31).all(), f"Invalid day values for 31-day month {month}"
            elif month in [4, 6, 9, 11]:  # Months with 30 days
                assert result.loc[result[month] == month, day].between(
                    1, 30).all(), f"Invalid day values for 30-day month {month}"
            elif month == 2:  # February (Leap year check)
                leap_year_mask = result[year_columns[0]].apply(lambda x: calendar.monthrange(x, 2)[1] == 29)
                assert result.loc[leap_year_mask, day].between(
                    1, 29).all(), f"Invalid day values for February in leap years"
                assert result.loc[~leap_year_mask, day].between(
                    1, 28).all(), f"Invalid day values for February in non-leap years"

        # Ensure cyclical encoding wraps around correctly
        for month, day in zip(month_columns, day_columns):
            month_mask = result[month] == month
            days_in_month = 31 if month in [1, 3, 5, 7, 8, 10, 12] else 30 if month in [4, 6, 9, 11] else 29 if \
                (result[year_columns[0]].apply(lambda x: calendar.monthrange(x, 2)[1] == 29)).any() else 28

            filtered_result_x = result.loc[month_mask, f'x_comp_{day}']
            filtered_result_y = result.loc[month_mask, f'y_comp_{day}']

            # Check if the filtered result for x_comp and y_comp are not empty before accessing the first element
            if not filtered_result_x.empty:
                assert filtered_result_x.iloc[0] == np.cos(2 * np.pi * 1 / days_in_month), \
                    f"Cyclical encoding for {day} did not wrap correctly for x_comp"
            else:
                print(f"No rows found for {month_mask} and x_comp_{day}")

            if not filtered_result_y.empty:
                assert filtered_result_y.iloc[0] == np.sin(2 * np.pi * 1 / days_in_month), \
                    f"Cyclical encoding for {day} did not wrap correctly for y_comp"
            else:
                print(f"No rows found for {month_mask} and y_comp_{day}")

        assert pd.api.types.is_numeric_dtype(
            result[x_comp_col]), f"Column {x_comp_col} contains non-numeric values"
        assert pd.api.types.is_numeric_dtype(
            result[y_comp_col]), f"Column {y_comp_col} contains non-numeric values"

    plot_circular_day(result, day_columns)

    return 'Test Passed'
