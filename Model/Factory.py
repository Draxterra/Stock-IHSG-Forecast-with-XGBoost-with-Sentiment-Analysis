# model_factory.py
from typing import Dict

from Process.Dataproc import Dataproc

from .ModelXGBoost import ModelXGBoost


class ModelFactory:
    @staticmethod
    def use_model(model_type: str, dataproc: Dataproc, params: Dict = None):
        """
        Create a model instance given a model type and a Dataproc instance.

        Parameters
        ----------
        model_type : str
            The type of model to create. Can be 'SVR', 'LR','Xgboost','LSTM', or 'Ridge'.
        dataproc : Dataproc
            The Dataproc instance to use for preprocessing data.
        params : Dict, optional
            Model parameters to pass to the model instance.

        Returns
        -------
        Model
            An instance of the requested model type.

        Raises
        ------
        ValueError
            If an unknown model type is given.
        """
        if model_type == "Xgboost":
            model = ModelXGBoost(dataproc, params)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        return model
