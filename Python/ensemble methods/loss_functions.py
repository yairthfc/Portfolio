import numpy as np


def misclassification_error(y_true: np.ndarray, y_pred: np.ndarray, normalize: bool = True) -> float:
    """
    Calculate misclassification loss

    Parameters
    ----------
    y_true: ndarray of shape (n_samples, )
        True response values
    y_pred: ndarray of shape (n_samples, )
        Predicted response values
    normalize: bool, default = True
        Normalize by number of samples or not

    Returns
    -------
    Misclassification of given predictions
    """
    if y_pred.shape != y_true.shape:
        raise IndexError("not the same size")

    missclass = np.sum(y_pred != y_true)
    print(missclass)
    print("  -  ")
    if normalize:
        return missclass / y_pred.shape[0]
    else:
        return missclass


