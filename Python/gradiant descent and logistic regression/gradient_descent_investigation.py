import numpy as np
import pandas as pd
from typing import Tuple, List, Callable, Type

from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

from loss_functions import misclassification_error
from cross_validate import cross_validate
from base_module import BaseModule
from base_learning_rate import  BaseLR
from gradient_descent import GradientDescent
from learning_rate import FixedLR

from sklearn.model_selection import cross_val_score

# from IMLearn.desent_methods import GradientDescent, FixedLR, ExponentialLR
from modules import L1, L2
from logistic_regression import LogisticRegression
from utils import split_train_test

import plotly.graph_objects as go


def plot_descent_path(module: Type[BaseModule],
                      descent_path: np.ndarray,
                      title: str = "",
                      xrange=(-1.5, 1.5),
                      yrange=(-1.5, 1.5)) -> go.Figure:
    """
    Plot the descent path of the gradient descent algorithm

    Parameters:
    -----------
    module: Type[BaseModule]
        Module type for which descent path is plotted

    descent_path: np.ndarray of shape (n_iterations, 2)
        Set of locations if 2D parameter space being the regularization path

    title: str, default=""
        Setting details to add to plot title

    xrange: Tuple[float, float], default=(-1.5, 1.5)
        Plot's x-axis range

    yrange: Tuple[float, float], default=(-1.5, 1.5)
        Plot's x-axis range

    Return:
    -------
    fig: go.Figure
        Plotly figure showing module's value in a grid of [xrange]x[yrange] over which regularization path is shown

    Example:
    --------
    fig = plot_descent_path(IMLearn.desent_methods.modules.L1, np.ndarray([[1,1],[0,0]]))
    fig.show()
    """
    def predict_(w):
        return np.array([module(weights=wi).compute_output() for wi in w])

    from utils import decision_surface
    return go.Figure([decision_surface(predict_, xrange=xrange, yrange=yrange, density=70, showscale=False),
                      go.Scatter(x=descent_path[:, 0], y=descent_path[:, 1], mode="markers+lines", marker_color="black")],
                     layout=go.Layout(xaxis=dict(range=xrange),
                                      yaxis=dict(range=yrange),
                                      title=f"GD Descent Path {title}"))


def get_gd_state_recorder_callback() -> Tuple[Callable[[], None], List[np.ndarray], List[np.ndarray]]:
    """
    Callback generator for the GradientDescent class, recording the objective's value and parameters at each iteration

    Return:
    -------
    callback: Callable[[], None]
        Callback function to be passed to the GradientDescent class, recoding the objective's value and parameters
        at each iteration of the algorithm

    values: List[np.ndarray]
        Recorded objective values

    weights: List[np.ndarray]
        Recorded parameters
    """
    v, w = [], []
    def callback(val, weight, **kwargs):
        v.append(val)
        w.append(weight)
    return callback, v, w


def compare_fixed_learning_rates(init: np.ndarray = np.array([np.sqrt(2), np.e / 3]),
                                 etas: Tuple[float] = (1, .1, .01, .001)):
    l1_results, l2_results = {}, {}

    for learning_rate in etas:
        print(f"Running Gradient Descent with eta={learning_rate} for L1 and L2 objectives")

        l1_weights, l2_weights = init.copy(), init.copy()
        l1_gd = GradientDescent(learning_rate=FixedLR(learning_rate), callback=get_gd_state_recorder_callback()[0])
        l2_gd = GradientDescent(learning_rate=FixedLR(learning_rate), callback=get_gd_state_recorder_callback()[0])

        l1_cb, l1_vals, l1_wts = get_gd_state_recorder_callback()
        l1_gd.callback_ = l1_cb
        l1_result = l1_gd.fit(f=L1(weights=l1_weights), X=None, y=None)

        l2_cb, l2_vals, l2_wts = get_gd_state_recorder_callback()
        l2_gd.callback_ = l2_cb
        l2_result = l2_gd.fit(f=L2(weights=l2_weights), X=None, y=None)

        l1_results[learning_rate] = (np.array(l1_wts), np.array(l1_vals))
        l2_results[learning_rate] = (np.array(l2_wts), np.array(l2_vals))

        print(f"L1: Solution {l1_result}, Objective value {l1_vals[-1]}")
        print(f"L2: Solution {l2_result}, Objective value {l2_vals[-1]}")

    # Plot descent paths
    for learning_rate in etas:
        l1_path, l1_obj_vals = l1_results[learning_rate]
        l2_path, l2_obj_vals = l2_results[learning_rate]

        plot_descent_path(L1, l1_path, title=f"L1 Descent Path with eta={learning_rate}").show()
        plot_descent_path(L2, l2_path, title=f"L2 Descent Path with eta={learning_rate}").show()

    # Plot convergence rates for L1
    l1_fig = go.Figure(layout=go.Layout(xaxis=dict(title="GD Iteration"), yaxis=dict(title="Objective Value"),
                                        title="L1 GD Convergence For Different Learning Rates"))
    for learning_rate in etas:
        l1_path, l1_obj_vals = l1_results[learning_rate]
        l1_fig.add_trace(go.Scatter(x=np.arange(len(l1_obj_vals)), y=l1_obj_vals, mode='lines', name=f'eta={learning_rate}'))

    l1_fig.show()

    # Plot convergence rates for L2
    l2_fig = go.Figure(layout=go.Layout(xaxis=dict(title="GD Iteration"), yaxis=dict(title="Objective Value"),
                                        title="L2 GD Convergence For Different Learning Rates"))
    for learning_rate in etas:
        l2_path, l2_obj_vals = l2_results[learning_rate]
        l2_fig.add_trace(go.Scatter(x=np.arange(len(l2_obj_vals)), y=l2_obj_vals, mode='lines', name=f'eta={learning_rate}'))

    l2_fig.show()



def load_data(path: str = "SAheart.data", train_portion: float = .8) -> \
        Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Load South-Africa Heart Disease dataset and randomly split into a train- and test portion

    Parameters:
    -----------
    path: str, default= "../datasets/SAheart.data"
        Path to dataset

    train_portion: float, default=0.8
        Portion of dataset to use as a training set

    Return:
    -------
    train_X : DataFrame of shape (ceil(train_proportion * n_samples), n_features)
        Design matrix of train set

    train_y : Series of shape (ceil(train_proportion * n_samples), )
        Responses of training samples

    test_X : DataFrame of shape (floor((1-train_proportion) * n_samples), n_features)
        Design matrix of test set

    test_y : Series of shape (floor((1-train_proportion) * n_samples), )
        Responses of test samples
    """
    df = pd.read_csv(path)
    df.famhist = (df.famhist == 'Present').astype(int)
    return split_train_test(df.drop(['chd', 'row.names'], axis=1), df.chd, train_portion)


def fit_logistic_regression():
    # Load and split SA Heart Disease dataset
    X_train, y_train, X_test, y_test = load_data()

    # Fit logistic regression model
    gd = GradientDescent(learning_rate=FixedLR(1e-4), max_iter=20000, out_type="last")
    log_reg = LogisticRegression()
    log_reg.fit(X_train.values, y_train.values)

    # Predict probabilities
    probs = log_reg.predict_proba(X_train.values)

    # Compute ROC curve
    fpr, tpr, thresholds = roc_curve(y_train, probs)
    # fpr, tpr, thresholds = roc_curve(y_test.values, probs)
    roc_auc = auc(fpr, tpr)

    # Plot ROC curve
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()

    ####################################################################################

    optimal_threshold = thresholds[np.argmax(tpr - fpr)]
    print(f"Optimal threshold (alpha*) = {optimal_threshold}")

    # Calculate the test error at optimal threshold
    test_probs = log_reg.predict_proba(X_test.values)
    test_preds = (test_probs >= optimal_threshold).astype(int)
    test_error = np.mean(test_preds != y_test.values)
    print(f"Test error at optimal threshold = {test_error}")

    ####################################################################################

    lambdas = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1]
    print("\nQuestions 10 and 11:")
    norm = "l1"
    train_errors = []
    validation_errors = []
    for lam in lambdas:
        print(f"Running Cross-Validation on {norm.capitalize()}, lambda={lam}")
        result = cross_validate(LogisticRegression(solver=gd, penalty=norm, lam=lam), X_train.values, y_train.values, misclassification_error, cv=5)
        train_errors.append(result[0])
        validation_errors.append(result[1])

    fig = go.Figure([go.Scatter(x=lambdas, y=train_errors, mode="lines", name="Train Errors"),
                        go.Scatter(x=lambdas, y=validation_errors, mode="lines", name="Validation Errors")],
                    layout=dict(title=f"Errors of Cross-Validation using {norm.capitalize()} Regularization",
                                xaxis_title="Lambda", yaxis_title="Error"))
    fig.show()

    best_lam_idx = int(np.argmin(validation_errors))
    best_lam = lambdas[best_lam_idx]
    model = LogisticRegression(solver=gd, penalty=norm, lam=best_lam).fit(X_train.values, y_train.values)
    print("-"*30)
    print(f"Best lambda value was: {best_lam}")
    print(f"Error of LogisticRegression with {norm.capitalize()} Regularization on and optimal lambda on the"
            f" test set is: {model.loss(X_test.values, y_test.values)}")
    print("-" * 30)

if __name__ == '__main__':
    np.random.seed(0)
    compare_fixed_learning_rates()
    fit_logistic_regression()
