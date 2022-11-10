from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


class SqrTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, sqr_features: list):

        self.sqr_features = sqr_features

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        X_ = X.copy()
        X_[self.sqr_features] = X_[self.sqr_features] ** 2

        return X_