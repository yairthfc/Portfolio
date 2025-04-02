
import numpy as np
from typing import NoReturn
from linear_regression import LinearRegression
import pandas as pd
from sklearn.model_selection import train_test_split
import os
import seaborn as sns
import matplotlib.pyplot as plt

def preprocess_train(X: pd.DataFrame, y: pd.Series):
    """
    Preprocess training data.
    """
    x_temp = X

    x_temp['price'] = y
    # Drop columns id and date
    x_temp = x_temp.drop(["id", "date"], axis=1)
    # Drop rows that violate base rules
    negative_values_mask = (x_temp.drop(columns=["lat", "long", "price"]) < 0).any(axis=1)
    missing_values_mask = x_temp.isnull().any(axis=1)
    sqft_living_sqft_lot_mask = (x_temp['sqft_living'] + x_temp['sqft_lot']) > 0
    yr_built_yr_renovated_mask = (x_temp['yr_renovated'] == 0) | (x_temp['yr_built'] < x_temp['yr_renovated'])

    invalid_rows_mask = negative_values_mask | missing_values_mask | ~sqft_living_sqft_lot_mask | ~yr_built_yr_renovated_mask
    x_temp = x_temp[~invalid_rows_mask]

    # create a new years built range column
    def get_year_range(year):
        if year > 2024:
            return None  
        elif year < 2000:
            year -= 1900
            return 1900 + (year // 10) * 10
        else:
            year -= 2000
            return 2000 + (year // 10) * 10

    x_temp['yr_built_range'] = x_temp['yr_built'].apply(get_year_range)
    x_temp = x_temp.dropna(subset=['yr_built_range'])
    x_temp = x_temp.drop(columns=["yr_built"], axis=1)
    
    x_temp.fillna(0, inplace=True)

    x_ready , y_ready = x_temp.drop("price", axis=1), x_temp.price
    
    return x_ready, y_ready

def preprocess_test(X: pd.DataFrame):
    """
    preprocess test data. You are not allowed to remove rows from X, but only edit its columns.
    Parameters
    ----------
    X: pd.DataFrame
        the loaded data

    Returns
    -------
    A preprocessed version of the test data that matches the coefficients format.
    """
    x_temp = X

    x_temp = x_temp.drop(["id", "date"], axis=1)

    def get_year_range(year):
        if year > 2024:
            return None  
        elif year < 2000:
            year -= 1900
            return 1900 + (year // 10) * 10
        else:
            year -= 2000
            return 2000 + (year // 10) * 10

    x_temp['yr_built_range'] = x_temp['yr_built'].apply(get_year_range)
    x_temp = x_temp.drop(columns=["yr_built"], axis=1)
    x_temp.fillna(0, inplace=True)
    return x_temp





def feature_evaluation(X: pd.DataFrame, y: pd.Series, output_path: str = ".") -> NoReturn:
    """
    Create scatter plot between each feature and the response.
        - Plot title specifies feature name
        - Plot title specifies Pearson Correlation between feature and response
        - Plot saved under given folder with file name including feature name
    Parameters
    ----------
    X : DataFrame of shape (n_samples, n_features)
        Design matrix of regression problem

    y : array-like of shape (n_samples, )
        Response vector to evaluate against

    output_path: str (default ".")
        Path to folder in which plots are saved
    """
    for column in X.columns:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=X[column], y=y)
        covariance = X[column].cov(y)
        std_X = X[column].std()
        std_y = y.std()
        pearson_corr = covariance / (std_X * std_y)
        title = f"{column} vs. Price\n"
        title += f"Pearson Correlation: {pearson_corr:.2f}"
        plt.title(title)
        plot_filename = f"{column}_scatter_plot.png"
        plt.savefig(os.path.join(output_path, plot_filename))
        plt.close()


if __name__ == '__main__':
    np.random.seed(3)
    df = pd.read_csv("house_prices.csv")
    X, y = df.drop("price", axis=1), df.price

    # Question 2 - split train test
    X_train_og, X_test_og, y_train_og, y_test_og = train_test_split(X, y, test_size=0.25, random_state=42)
    # Question 3 - preprocessing of housing prices train dataset
    x_train, y_train = preprocess_train(X_train_og,y_train_og)
    # Question 4 - Feature evaluation of train dataset with respect to response
    # feature_evaluation(x_train,y_train)
    x_test = preprocess_test(X_test_og)
    # Question 6 - Fit model over increasing percentages of the overall training data
    # For every percentage p in 10%, 11%, ..., 100%, repeat the following 10 times:
    #   1) Sample p% of the overall training data
    #   2) Fit linear model (including intercept) over sampled set
    #   3) Test fitted model over test set
    #   4) Store average and variance of loss over test set
    # Then plot average loss as function of training size with error ribbon of size (mean-2*std, mean+2*std)
    p_loss = []
    precent_na = []
    std_losses = []
    for i in range(10,101):
        for_std = []
        sum1 = 0
        for j in range(10):
            sample_index = x_train.sample(frac=(i/100)).index
            sample_x = x_train.loc[sample_index]
            sample_y = y_train.loc[sample_index]
            model = LinearRegression()
            model.fit(sample_x, sample_y)
            loss = model.loss(x_test, y_test_og)
            sum1+= loss
            for_std.append(loss)
        p_loss.append(sum1/10)
        precent_na.append(i)
        std = np.std(for_std)
        std_losses.append(std)
    
    for i in range(len(p_loss)):
        std_losses[i] = 2 * std_losses[i]
    std_losses = np.array(std_losses)
    p_loss = np.array(p_loss)
    precent_na = np.array(precent_na)


# Plotting the graph
    plt.figure(figsize=(8, 5))
    plt.errorbar(precent_na, p_loss,yerr= std_losses, fmt='o', color='blue',
                 ecolor='green', elinewidth=2, capsize=5, label='Mean Loss ± 2 * Std Dev')

    # Add labels and title
    plt.xlabel('p%')
    plt.ylabel('Mean Loss')
    plt.title('Mean Loss as a Function of p% with Confidence Interval')

    # Add legend
    plt.legend()

    # Show plot
    plt.grid(True)
    plt.show()
    




