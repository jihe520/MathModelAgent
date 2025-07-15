"""
This file contains implementations of various mathematical models.
"""
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from statsmodels.tsa.arima.model import ARIMA


class MathematicalModels:
    """
    A collection of mathematical models for regression, classification, and time series analysis.
    """

    @staticmethod
    def linear_regression(X, y):
        """
        Fits a linear regression model.

        Args:
            X: Training data (features).
            y: Target values.

        Returns:
            A trained linear regression model.
        """
        model = LinearRegression()
        model.fit(X, y)
        return model

    @staticmethod
    def logistic_regression(X, y):
        """
        Fits a logistic regression model.

        Args:
            X: Training data (features).
            y: Target values.

        Returns:
            A trained logistic regression model.
        """
        model = LogisticRegression()
        model.fit(X, y)
        return model

    @staticmethod
    def arima(series, order=(5, 1, 0)):
        """
        Fits an ARIMA model to a time series.

        Args:
            series: The time series data.
            order: The (p, d, q) order of the model.

        Returns:
            A fitted ARIMA model result.
        """
        model = ARIMA(series, order=order)
        model_fit = model.fit()
        return model_fit
