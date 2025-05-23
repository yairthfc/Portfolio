from classifiers import Perceptron, LDA, GaussianNaiveBayes
from typing import Tuple
from utils import *
from loss_functions import misclassification_error
import matplotlib.pyplot as plot
from math import atan2, pi
import numpy as np

def load_dataset(filename: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load dataset for comparing the Gaussian Naive Bayes and LDA classifiers. File is assumed to be an
    ndarray of shape (n_samples, 3) where the first 2 columns represent features and the third column the class

    Parameters
    ----------
    filename: str
        Path to .npy data file

    Returns
    -------
    X: ndarray of shape (n_samples, 2)
        Design matrix to be used

    y: ndarray of shape (n_samples,)
        Class vector specifying for each sample its class

    """
    data = np.load(filename)
    return data[:, :2], data[:, 2].astype(int)


def run_perceptron():
    """
    Fit and plot fit progression of the Perceptron algorithm over both the linearly separable and inseparable datasets

    Create a line plot that shows the perceptron algorithm's training loss values (y-axis)
    as a function of the training iterations (x-axis).
    """
    def callback_func(perception, x, y):
        predicted = perception._predict(x)
        losses.append(misclassification_error(y, predicted))


    for n, f in [("Linearly Separable", "linearly_separable.npy"), ("Linearly Inseparable", "linearly_inseparable.npy")]:
        # Load dataset
        X, y = load_dataset(f)

        # Fit Perceptron and record loss in each fit iteration
        per = Perceptron(callback=callback_func)
        losses = []
        per.fit(X,y)
        print(losses)

        # Plot figure of loss as function of fitting iteration
        plot.plot(losses, label=f"{n} DataSet")
        plot.title("Perceptron Training Loss over Iterations")
        plot.xlabel("Iterations")
        plot.ylabel("Training Loss")
        plot.legend()
        plot.show()

def get_ellipse(mu: np.ndarray, cov: np.ndarray):
    """
    Draw an ellipse centered at given location and according to specified covariance matrix

    Parameters
    ----------
    mu : ndarray of shape (2,)
        Center of ellipse

    cov: ndarray of shape (2,2)
        Covariance of Gaussian

    Returns
    -------
        scatter: A plotly trace object of the ellipse
    """

    l1, l2 = tuple(np.linalg.eigvalsh(cov)[::-1])
    theta = atan2(l1 - cov[0, 0], cov[0, 1]) if cov[0, 1] != 0 else (np.pi / 2 if cov[0, 0] < cov[1, 1] else 0)
    t = np.linspace(0, 2 * pi, 100)
    xs = (l1 * np.cos(theta) * np.cos(t)) - (l2 * np.sin(theta) * np.sin(t))
    ys = (l1 * np.sin(theta) * np.cos(t)) + (l2 * np.cos(theta) * np.sin(t))

    return go.Scatter(x=mu[0] + xs, y=mu[1] + ys, mode="lines", marker_color="black")


def compare_gaussian_classifiers():
    """
    Fit both Gaussian Naive Bayes and LDA classifiers on both gaussians1 and gaussians2 datasets
    """
    for f in ["gaussian1.npy", "gaussian2.npy"]:
        # Load dataset
        X,y = load_dataset(f)

        # Fit models and predict over training set
        L = LDA()
        G = GaussianNaiveBayes()
        L_pre, G_pre, L_acc, G_acc = None,None,None,None

        from loss_functions import accuracy
        models = [L, G]
        for model in models:
            model.fit(X,y)
            if isinstance(model, LDA):
                L_pre = L._predict(X)
                L_acc = accuracy(y, L_pre)
            elif isinstance(model,GaussianNaiveBayes): 
                G_pre = G._predict(X)
                G_acc = accuracy(y, G_pre)

        # # Plot a figure with two suplots, showing the Gaussian Naive Bayes predictions on the left and LDA predictions
        # # on the right. Plot title should specify dataset used and subplot titles should specify algorithm and accuracy
        # # Create subplots

        fig = make_subplots(rows=1, cols=2,
                        subplot_titles=[f"LDA, Accuracy: {L_acc:.2f}",
                                        f"Gaussian NB, Accuracy: {G_acc:.2f}"])

        # Add traces for data-points setting symbols and colors
        fig.add_trace(go.Scatter(x=X[:, 0], y=X[:, 1], mode='markers',
                                marker=dict(color=L_pre, symbol=y, size=10),
                                name="LDA"),
                    row=1, col=1)

        fig.add_trace(go.Scatter(x=X[:, 0], y=X[:, 1], mode='markers',
                                marker=dict(color=G_pre, symbol=y, size=10),
                                name="Gaussian NB"),
                    row=1, col=2)

        # # Add `X` dots specifying fitted Gaussians' means
        fig.add_trace(go.Scatter(x=L.mu_[:, 0], y=L.mu_[:, 1], mode='markers',
                                marker=dict(color='black', symbol='x', size=12),
                                showlegend=False),
                    row=1, col=1)
        fig.add_trace(go.Scatter(x=G.mu_[:, 0], y=G.mu_[:, 1], mode='markers',
                                marker=dict(color='black', symbol='x', size=12),
                                showlegend=False),
                    row=1, col=2)

        # # Add ellipses depicting the covariances of the fitted Gaussians
        for i in range(len(L.mu_)):
            fig.add_trace(get_ellipse(L.mu_[i], L.cov_), row=1, col=1)

        for i in range(len(G.mu_)):
            fig.add_trace(get_ellipse(G.mu_[i], np.diag(G.vars_[i])), row=1, col=2)

        fig.show()

if __name__ == '__main__':
    np.random.seed(0)
    run_perceptron()
    compare_gaussian_classifiers()
