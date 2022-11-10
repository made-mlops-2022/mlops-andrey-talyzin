from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import preprocessing
import pandas as pd
import numpy as np

class SqrTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, sqr_features: list):

        self.sqr_features = sqr_features

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        X_ = X.copy()
        X_[self.sqr_features] = X_[self.sqr_features] ** 2

        return X_