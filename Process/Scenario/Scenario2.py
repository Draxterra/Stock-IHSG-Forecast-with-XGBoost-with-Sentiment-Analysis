# Scenario1.py

import pandas as pd


# Sigma i=1 to n when Xi/2


class Scenario2:
    def __init__(self, news: pd.DataFrame) -> None:
        self.news = news
        self.result = self.process()

    def process(self) -> pd.DataFrame:
        df_avg_sentimen = self.news
        df_avg_sentimen_clean = df_avg_sentimen.dropna(subset=["Sentiment_Score"])
        # df_avg_sentimen_clean.set_index("tanggal", inplace=True)
        return df_avg_sentimen_clean
