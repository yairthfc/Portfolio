
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from polynomial_fitting import PolynomialFitting


def load_data(filename: str) -> pd.DataFrame:
    """
    Load city daily temperature dataset and preprocess data.
    Parameters
    ----------
    filename: str
        Path to house prices dataset

    Returns
    -------
    Design matrix and response vector (Temp)
    """
    month_count = {1: 0, 2: 31, 3: 59, 4: 90, 5: 120, 6: 151, 7: 181, 8: 212, 9: 243, 10: 273, 11: 304, 12: 334}
    data = pd.read_csv(filename, parse_dates=['Date'])

    data.dropna(inplace=True)
    data = data[data['Day'] > 0]
    data = data[data['Month'] > 0]
    data = data[data['Year'] > 0]
    data = data[data['Temp'] > -20]

    def month_days(month_num):
        return month_count[month_num]
    
    data['DayOfYear'] = data['Month'].apply(month_days)
    data['DayOfYear'] = data['DayOfYear'] + data['Day']

    return data



if __name__ == '__main__':
    # Question 2 - Load and preprocessing of city temperature dataset
    df = load_data("city_temperature.csv")

    # Question 3 - Exploring data for specific country
    data_israel = df[df['Country'] == 'Israel']
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data_israel, x='DayOfYear', y='Temp', hue='Year', palette='tab10')
    plt.title('Average Daily Temperature in Israel as a Function of DayOfYear')
    plt.xlabel('Day of Year')
    plt.ylabel('Temperature (°C)')
    plt.legend(title='Year', bbox_to_anchor=(1, 1), loc='upper left')
    plt.grid(True)
    plt.show()

    monthly_std = data_israel.groupby('Month')['Temp'].agg(np.std).reset_index()
    
    plt.figure(figsize=(8, 5))
    sns.barplot(x='Month', y='Temp', data=monthly_std, palette='viridis')
    plt.title('Standard Deviation of Daily Temperatures by Month in Israel')
    plt.xlabel('Month')
    plt.ylabel('Standard Deviation of Temperature (°C)')
    plt.grid(True)
    plt.show()
    
    # Question 4 - Exploring differences between countries
    data = df.groupby(['Country', 'Month'])['Temp'].agg(['mean', 'std']).reset_index()
    data.rename(columns={'mean': 'AverageTemp', 'std': 'TempStdDev'}, inplace=True)
    plt.figure(figsize=(14, 8))
    for country in data['Country'].unique():
        country_data = data[data['Country'] == country]
        plt.errorbar(country_data['Month'], country_data['AverageTemp'], yerr=country_data['TempStdDev'], label=country, fmt='-o')
    plt.xlabel('Month')
    plt.ylabel('Temperature (°C)')
    plt.title('Average Monthly Temperature with Standard Deviation by Country')
    plt.legend(title='Country')
    plt.grid(True)
    plt.show()
    
    
    # Question 5 - Fitting model for different values of `k`
    train_il, test_il = train_test_split(data_israel, test_size=0.25, random_state=42)
    x_train_il, y_train = train_il.DayOfYear, train_il.Temp
    x_test_il , y_test = test_il.DayOfYear , test_il.Temp

    losses = []
    for k in range(1,11):
        model = PolynomialFitting(k)
        model.fit(x_train_il, y_train)
        loss = model.loss(x_test_il, y_test)
        rounded = round(loss, 2)
        losses.append(rounded)

    losses = np.array(losses)
    ks = np.array([1,2,3,4,5,6,7,8,9,10])
    data_k = pd.DataFrame({'k' : ks, 'test error' : losses})

    plt.figure(figsize=(8, 5))
    sns.barplot(x='k', y='test error', data=data_k, palette='viridis')
    plt.title('test error for different polynomial k')
    plt.xlabel('K')
    plt.ylabel('Test Error')
    plt.grid(True)
    plt.show()



    # Question 6 - Evaluating fitted model on different countries
    chosen_k = 2
    model1 = PolynomialFitting(chosen_k)
    model1.fit(x_train_il, y_train)

    countries = df['Country'].unique()
    countries = countries[countries != 'Israel']  # exclude Israel

    errors = []
    for country in countries:
        data_country = df[df['Country'] == country]
        x_country = data_country['DayOfYear']
        y_country = data_country['Temp']
        error = model1.loss(x_country, y_country)
        errors.append((country, error))

    # Convert to DataFrame for plotting
    errors_df = pd.DataFrame(errors, columns=['Country', 'Error'])

    # Plot the errors
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Country', y='Error', data=errors_df, palette='viridis')
    plt.title('Model Error Over Each Country')
    plt.xlabel('Country')
    plt.ylabel('Error')
    plt.grid(True)
    plt.show()
