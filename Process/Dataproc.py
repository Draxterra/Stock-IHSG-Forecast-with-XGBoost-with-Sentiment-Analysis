import ast
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from .SentimentAnalysis import SentimentAnalysis


@dataclass
class DatasetConfig:
    file_path: str
    file_path_sentiment: str = None
    split_ratio: float = 0.8
    n_in: int = 10
    n_out: int = 1
    sentiment_scenario: int = 1
    drop_columns: bool = True
    drop_columns_list: list = field(
        default_factory=lambda: ["Change%", "Volume"]
    )  # Daftar kolom yang akan di-drop
    start_date: str = None  # Tanggal awal dalam format 'YYYY-MM-DD'
    end_date: str = None  # Tanggal akhir dalam format 'YYYY-MM-DD'


@dataclass
class DataSplit:
    X_train: pd.DataFrame = field(default_factory=pd.DataFrame)
    X_val: pd.DataFrame = field(default_factory=pd.DataFrame)
    y_train: np.ndarray = field(default_factory=lambda: np.array([]))
    y_val: np.ndarray = field(default_factory=lambda: np.array([]))


@dataclass
class ScaledData:
    X_train_scaled: pd.DataFrame = field(default_factory=pd.DataFrame)
    X_val_scaled: pd.DataFrame = field(default_factory=pd.DataFrame)
    X_train_scaled_transposed: np.ndarray = field(default_factory=lambda: np.empty(0))
    X_val_scaled_transposed: np.ndarray = field(default_factory=lambda: np.empty(0))


@dataclass
class ReturnsData:
    absolute_return: np.ndarray = field(default_factory=lambda: np.array([]))
    relative_return: np.ndarray = field(default_factory=lambda: np.array([]))
    log_return: np.ndarray = field(default_factory=lambda: np.array([]))


class Dataproc:
    def __init__(self, config: DatasetConfig, scaler: MinMaxScaler = MinMaxScaler()):
        self.config = config
        self.scaler = scaler
        logging.info("Initializing Dataproc with config: %s", config)
        self.DATA: pd.DataFrame = self._read_dataset()
        self.DATA_SENTIMENT = self._read_dataset_sentiment()
        self.split_lengths: Tuple[int, int] = self._calculate_split_lengths()
        self.DATA_SUPERVISED: pd.DataFrame = self._select_supervised_data()
        self.data_split = self._split_data()
        self.scaled_data = self._scale_data()
        self.returns = self._calculate_returns()
        self.feature_len: int = self.DATA.shape[1]

    def _read_dataset(self) -> pd.DataFrame:
        logging.info("Reading dataset from: %s", self.config.file_path)
        data = pd.read_csv(self.config.file_path)
        data["Date"] = pd.to_datetime(data["Date"], format="%d/%m/%Y")
        data.set_index("Date", inplace=True)

        # Drop columns sesuai konfigurasi
        if self.config.drop_columns and self.config.drop_columns_list:
            data = data.drop(self.config.drop_columns_list, axis=1)
            logging.info("Dropped columns: %s", self.config.drop_columns_list)

        # Filter data berdasarkan start_date dan end_date
        if self.config.start_date:
            data = data[data.index >= pd.to_datetime(self.config.start_date)]
        if self.config.end_date:
            data = data[data.index <= pd.to_datetime(self.config.end_date)]

        logging.info("Dataset read successfully with shape: %s", data.shape)
        return data

    def _read_dataset_sentiment(self) -> pd.DataFrame:
        if self.config is None or self.config.file_path_sentiment is None:
            logging.info(
                "config is None or self.config.file_path_sentiment is None. Returning None"
            )
            return None
        logging.info(
            "Reading dataset sentiment from: %s", self.config.file_path_sentiment
        )
        data_sentiment = pd.read_csv(self.config.file_path_sentiment)
        # self._extract_date(data_sentiment)
        # data_sentiment = self._extract_news_json(data_sentiment)
        data_sentiment.dropna(subset=["tanggal"], inplace=True)
        data_sentiment["tanggal"] = pd.to_datetime(data_sentiment["tanggal"])
        data_sentiment.set_index("tanggal", inplace=True)
        return data_sentiment

    def _extract_date(self, data):
        data["tanggal"] = pd.to_datetime(
            data["tanggal"].str.extract(r"(\d{2}/\d{2}/\d{4})")[0], format="%d/%m/%Y"
        )
        return data

    def _extract_news_json(self, data):
        data["Extract"] = data["Extract"].apply(
            lambda x: ast.literal_eval(x) if pd.notna(x) else {}
        )

        # Normalize JSON data into new columns
        extracted_features = pd.json_normalize(data["Extract"])
        data = pd.concat([data.drop(columns=["Extract"]), extracted_features], axis=1)
        return data

    def combine_sentiment_and_stock_data(self):
        data_process = SentimentAnalysis(
            self.DATA_SENTIMENT, self.config.sentiment_scenario
        )

        combined_data = pd.merge(
            self.DATA,
            data_process.processed_data,
            how="left",
            left_index=True,
            right_index=True,
        )
        combined_data["Sentiment_Score"] = combined_data["Sentiment_Score"].ffill()
        return combined_data

    def _calculate_split_lengths(self) -> Tuple[int, int]:
        total_length = len(self.DATA)
        train_length = int(total_length * self.config.split_ratio)
        val_length = total_length - train_length
        logging.info(
            "Split lengths calculated: train_length=%d, val_length=%d",
            train_length,
            val_length,
        )
        return train_length, val_length

    def _select_supervised_data(self) -> pd.DataFrame:
        if self.config.file_path_sentiment is None:
            return self._create_supervised_data()
        else:
            if self.config.sentiment_scenario == 2:
                # Tambah scenario disini soalnya harus di supervised dulu terus edit split datanya huhuhu
                self.DATA = self.combine_sentiment_and_stock_data()
                data_sup = self._create_supervised_data()
                return self._sigma_score(data_sup)

            elif self.config.sentiment_scenario == 3:
                self.DATA = self.combine_sentiment_and_stock_data()
                data_sup = self._create_supervised_data()
                return self._scenario3(data_sup)

            elif self.config.sentiment_scenario == 4:
                self.DATA = self.combine_sentiment_and_stock_data()
                data_sup = self._create_supervised_data()
                return self._scenario4(data_sup)

            elif self.config.sentiment_scenario == 5:
                self.DATA = self.combine_sentiment_and_stock_data()
                data_sup = self._create_supervised_data()
                return self._scenario4(data_sup)

            self.DATA = self.combine_sentiment_and_stock_data()
            return self._create_supervised_data()

    def _scenario3(self, data_sup):
        sentiment_columns = [
            col
            for col in data_sup.columns
            if col.startswith("Sentiment_Score(t-") and col != "Sentiment_Score(t-1)"
        ]
        data_sup = data_sup.drop(columns=sentiment_columns)
        return data_sup

    def _scenario4(self, data_sup):
        sentiment_columns = [
            col for col in data_sup.columns if col.startswith("Sentiment_Score(t-")
        ]
        # Hitung sum dari kolom-kolom tersebut dan bagi dengan 2
        data_sup["Sigma_Sentiment"] = data_sup[sentiment_columns].sum(axis=1)
        data_sup = data_sup.drop(columns=sentiment_columns)
        return data_sup

    def _scenario5(self, data_sup):
        sentiment_columns = [
            col for col in data_sup.columns if col.startswith("Sentiment_Score(t-")
        ]
        # Hitung sum dari kolom-kolom tersebut dan bagi dengan 2
        data_sup["Sigma_Sentiment"] = data_sup[sentiment_columns].sum(axis=1) / np.exp(
            np.arange(len(sentiment_columns))
        )
        data_sup = data_sup.drop(columns=sentiment_columns)
        return data_sup

    def _sigma_score(self, data_sup):
        sentiment_columns = [
            col for col in data_sup.columns if col.startswith("Sentiment_Score(t-")
        ]
        # Hitung sum dari kolom-kolom tersebut dan bagi dengan 2
        data_sup["Sigma_Sentiment"] = data_sup[sentiment_columns].sum(axis=1) / 2
        data_sup = data_sup.drop(columns=sentiment_columns)
        return data_sup

    def _create_supervised_data(self) -> pd.DataFrame:
        logging.info("Creating supervised data")
        n_vars = self.DATA.shape[1]
        cols, names = [], []
        for i in range(self.config.n_in, 0, -1):
            cols.append(self.DATA.shift(i))
            names += [(f"{self.DATA.columns[j]}(t-{i})") for j in range(n_vars)]
        for i in range(0, self.config.n_out):
            cols.append(self.DATA.shift(-i))
            suffix = f"(t+{i})" if i > 0 else "(t)"
            names += [(f"{self.DATA.columns[j]}{suffix}") for j in range(n_vars)]
        agg = pd.concat(cols, axis=1)
        agg.index = self.DATA.index
        agg.columns = names
        logging.info("Supervised data created with shape: %s", agg.dropna().shape)
        return agg.dropna()

    def _split_data(self) -> DataSplit:
        logging.info("Splitting data into train and validation sets")
        X_train = self.DATA_SUPERVISED.iloc[: self.split_lengths[0]]
        X_val = self.DATA_SUPERVISED.iloc[self.split_lengths[0] :]
        y_train = X_train["Close(t)"]
        y_val = X_val["Close(t)"]
        if self.config.file_path_sentiment is None:
            X_train = X_train.drop(["Open(t)", "Close(t)", "High(t)", "Low(t)"], axis=1)
            X_val = X_val.drop(["Open(t)", "Close(t)", "High(t)", "Low(t)"], axis=1)
        else:
            X_train = X_train.drop(
                ["Open(t)", "Close(t)", "High(t)", "Low(t)", "Sentiment_Score(t)"],
                axis=1,
            )
            X_val = X_val.drop(
                ["Open(t)", "Close(t)", "High(t)", "Low(t)", "Sentiment_Score(t)"],
                axis=1,
            )

        logging.info(
            "Data split complete: X_train shape=%s, X_val shape=%s",
            X_train.shape,
            X_val.shape,
        )
        return DataSplit(X_train, X_val, y_train, y_val)

    def _scale_data(self) -> ScaledData:
        logging.info("Scaling data")
        X_train_scaled = pd.DataFrame(
            self.scaler.fit_transform(self.data_split.X_train),
            columns=self.data_split.X_train.columns,
        )
        X_val_scaled = pd.DataFrame(
            self.scaler.transform(self.data_split.X_val),
            columns=self.data_split.X_train.columns,
        )
        X_train_transposed, X_val_transposed = self._transpose_data(
            X_train_scaled, X_val_scaled
        )
        logging.info("Data scaling complete")
        return ScaledData(
            X_train_scaled, X_val_scaled, X_train_transposed, X_val_transposed
        )

    def _transpose_data(
        self, X_train_scaled: pd.DataFrame, X_val_scaled: pd.DataFrame
    ) -> Tuple[np.ndarray, np.ndarray]:
        logging.info("Transposing scaled data")

        if (
            self.config.sentiment_scenario != 1
            and self.config.file_path_sentiment is not None
            and self.config.sentiment_scenario != 3
        ):
            sentiment_column = "Sigma_Sentiment"
            features_columns = [
                col for col in X_train_scaled.columns if col != sentiment_column
            ]
            timesteps = self.config.n_in
            features = len(features_columns) // timesteps

            X_train_time_series = [
                X_train_scaled[features_columns]
                .iloc[:, i * features : (i + 1) * features]
                .values
                for i in range(timesteps)
            ]
            X_val_time_series = [
                X_val_scaled[features_columns]
                .iloc[:, i * features : (i + 1) * features]
                .values
                for i in range(timesteps)
            ]
            sentiment_train = X_train_scaled[sentiment_column].values[
                :, np.newaxis, np.newaxis
            ]
            sentiment_val = X_val_scaled[sentiment_column].values[
                :, np.newaxis, np.newaxis
            ]

            # Gabungkan time-series dan sentiment score
            X_train = np.array(X_train_time_series).transpose(
                1, 0, 2
            )  # (samples, timesteps, features)
            X_val = np.array(X_val_time_series).transpose(1, 0, 2)

            # Tambahkan sentiment score ke fitur terakhir
            X_train = np.concatenate(
                [X_train, np.repeat(sentiment_train, timesteps, axis=1)], axis=2
            )
            X_val = np.concatenate(
                [X_val, np.repeat(sentiment_val, timesteps, axis=1)], axis=2
            )

            logging.info("Data transposition complete")
            return X_train, X_val
        elif (
            self.config.sentiment_scenario == 3
            and self.config.file_path_sentiment is not None
        ):
            sentiment_column = "Sentiment_Score(t-1)"
            features_columns = [
                col for col in X_train_scaled.columns if col != sentiment_column
            ]
            timesteps = self.config.n_in
            features = len(features_columns) // timesteps

            X_train_time_series = [
                X_train_scaled[features_columns]
                .iloc[:, i * features : (i + 1) * features]
                .values
                for i in range(timesteps)
            ]
            X_val_time_series = [
                X_val_scaled[features_columns]
                .iloc[:, i * features : (i + 1) * features]
                .values
                for i in range(timesteps)
            ]
            sentiment_train = X_train_scaled[sentiment_column].values[
                :, np.newaxis, np.newaxis
            ]
            sentiment_val = X_val_scaled[sentiment_column].values[
                :, np.newaxis, np.newaxis
            ]

            # Gabungkan time-series dan sentiment score
            X_train = np.array(X_train_time_series).transpose(
                1, 0, 2
            )  # (samples, timesteps, features)
            X_val = np.array(X_val_time_series).transpose(1, 0, 2)

            # Tambahkan sentiment score ke fitur terakhir
            X_train = np.concatenate(
                [X_train, np.repeat(sentiment_train, timesteps, axis=1)], axis=2
            )
            X_val = np.concatenate(
                [X_val, np.repeat(sentiment_val, timesteps, axis=1)], axis=2
            )

            logging.info("Data transposition complete")
            return X_train, X_val

        timesteps, features = (
            self.config.n_in,
            len(X_train_scaled.columns) // self.config.n_in,
        )
        X_train = [
            X_train_scaled.iloc[:, i * features : (i + 1) * features].values
            for i in range(timesteps)
        ]
        X_val = [
            X_val_scaled.iloc[:, i * features : (i + 1) * features].values
            for i in range(timesteps)
        ]
        logging.info("Data transposition complete")
        return np.array(X_train).transpose(1, 0, 2), np.array(X_val).transpose(1, 0, 2)

    def _calculate_returns(self) -> Dict[str, ReturnsData]:
        logging.info("Calculating returns")
        y_train = self.data_split.y_train
        y_val = self.data_split.y_val
        bbfil = 0  # Replace this with the desired bbfil value

        returns = {
            "y_train": ReturnsData(
                np.concatenate([[bbfil], np.diff(y_train)]),
                np.concatenate(
                    [[bbfil], np.diff(y_train) / y_train[:-1]]
                ),  # Multiply by 100 for percentage
                np.concatenate(
                    [[bbfil], np.diff(np.log(y_train))]
                ),  # Multiply by 100 for percentage
            ),
            "y_val": ReturnsData(
                np.concatenate([[bbfil], np.diff(y_val)]),
                np.concatenate(
                    [[bbfil], np.diff(y_val) / y_val[:-1]]
                ),  # Multiply by 100 for percentage
                np.concatenate(
                    [[bbfil], np.diff(np.log(y_val))]
                ),  # Multiply by 100 for percentage
            ),
        }
        logging.info("Returns calculation complete")
        return returns

    def get_scaled_data(self) -> ScaledData:
        logging.info("Getting scaled data")
        return self.scaled_data

    def get_returns(self) -> Dict[str, ReturnsData]:
        logging.info("Getting returns data")
        return self.returns

    def get_data_split(self) -> DataSplit:
        logging.info("Getting data split")
        return self.data_split


if __name__ == "__main__":
    config = DatasetConfig(file_path=r"Dataset\Stock\IHSG_Stock_Clean.csv")
    data_proc = Dataproc(config)
    print(data_proc.get_returns())
