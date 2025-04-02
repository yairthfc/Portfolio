import numpy as np
from typing import Tuple
from utils import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from adaboost import AdaBoost
from decision_stump import DecisionStump

def generate_data(n: int, noise_ratio: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate a dataset in R^2 of specified size

    Parameters
    ----------
    n: int
        Number of samples to generate

    noise_ratio: float
        Ratio of labels to invert

    Returns
    -------
    X: np.ndarray of shape (n_samples,2)
        Design matrix of samples

    y: np.ndarray of shape (n_samples,)
        Labels of samples
    """
    '''
    generate samples X with shape: (num_samples, 2) and labels y with shape (num_samples).
    num_samples: the number of samples to generate
    noise_ratio: invert the label for this ratio of the samples
    '''
    X, y = np.random.rand(n, 2) * 2 - 1, np.ones(n)
    y[np.sum(X ** 2, axis=1) < 0.5 ** 2] = -1
    y[np.random.choice(n, int(noise_ratio * n))] *= -1
    return X, y


def fit_and_evaluate_adaboost(noise, n_learners=250, train_size=5000, test_size=500):
    (train_X, train_y), (test_X, test_y) = generate_data(train_size, noise), generate_data(test_size, noise)
    ada_boost = AdaBoost(wl=DecisionStump, iterations= n_learners)

    ada_boost.fit(train_X, train_y)
    # Question 1: Train- and test errors of AdaBoost in noiseless case
    train_errors = []
    test_errors = []

    for t in range(1, n_learners + 1):
        train_error = ada_boost.partial_loss(train_X, train_y, t)
        test_error = ada_boost.partial_loss(test_X, test_y, t)
        train_errors.append(train_error)
        test_errors.append(test_error)

    # Plotting training and test errors
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.arange(1, n_learners + 1), y=train_errors, mode='lines', name='Training Error'))
    fig.add_trace(go.Scatter(x=np.arange(1, n_learners + 1), y=test_errors, mode='lines', name='Test Error'))
    fig.update_layout(title='Training and Test Errors of AdaBoost',
                        xaxis_title='Number of Learners',
                        yaxis_title='Error',
                        template='plotly_white')
    fig.show()

    # Question 2: Plotting decision surfaces
    # Plot decision surfaces for different numbers of learners
    T = [5, 50, 100, 250]
    lims = np.array([np.r_[train_X, test_X].min(axis=0), np.r_[train_X, test_X].max(axis=0)]).T + np.array([-.1, .1])

    fig = make_subplots(rows=2, cols=2, subplot_titles=[f"{t} Learners" for t in T])

    for i, t in enumerate(T):
        row = (i // 2) + 1
        col = (i % 2) + 1
        
        decision_surface_trace = decision_surface(lambda X: ada_boost.partial_predict(X, t), lims[0], lims[1], showscale=False)
        scatter_trace = go.Scatter(x=test_X[:, 0], y=test_X[:, 1], mode='markers',
                                marker=dict(color=test_y, symbol='circle', colorscale=['blue', 'red'],
                                            line=dict(color='black', width=1)))
        
        fig.add_trace(decision_surface_trace, row=row, col=col)
        fig.add_trace(scatter_trace, row=row, col=col)

    fig.update_layout(title='Decision Surfaces for Different Numbers of Learners')
    fig.show()

    # Question 3: Decision surface of best performing ensemble
    best_T = np.argmin(test_errors) + 1  # best T is the index of the minimum test error
    fig = make_subplots(rows=1, cols=1, subplot_titles=[f"{best_T} best stump number to learn from "])

    decision_surface_trace = decision_surface(lambda X: ada_boost.partial_predict(X, best_T), lims[0], lims[1], showscale=False)
    scatter_trace = go.Scatter(x=test_X[:, 0], y=test_X[:, 1], mode='markers',
                            marker=dict(color=test_y, symbol='circle', colorscale=['blue', 'red'],
                                        line=dict(color='black', width=1)))
    fig.add_trace(decision_surface_trace, row=1, col=1)
    fig.add_trace(scatter_trace, row=1, col=1)
    fig.show()

    # Question 4: Decision surface with weighted samples
    D = ada_boost.D_[-1]
    normalized_D = D / np.max(D) * 5

    fig = go.Figure()

    decision_surface_trace = decision_surface(lambda X: ada_boost._predict(X), lims[0], lims[1], showscale=False)
    fig.add_trace(decision_surface_trace)

    scatter_trace = go.Scatter(
        x=train_X[:, 0], y=train_X[:, 1], mode='markers',
        marker=dict(
            size=normalized_D * 10, color=train_y, symbol='circle',
            colorscale=['blue', 'red'], line=dict(color='black', width=1)
        )
    )
    fig.add_trace(scatter_trace)
    fig.update_layout(title='Decision Surface with Weighted Samples')
    fig.show()


if __name__ == '__main__':
    np.random.seed(0)
    fit_and_evaluate_adaboost(0)
    fit_and_evaluate_adaboost(0.4)