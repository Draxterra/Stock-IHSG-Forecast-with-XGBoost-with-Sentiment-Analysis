# Stock-IHSG-Forecast-with-XGBoost-with-Sentiment-Analysis

This project is part of my final assignment as a Data Science student at Telkom University. This project focuses on forecasting the Indonesian Stock Exchange Index (IHSG) using the *Extreme Gradient Boosting* (XGBoost) algorithm combined with sentiment analysis of financial news.

## Project Description

IHSG is the main indicator of the stock market in Indonesia. Forecasting the movement of IHSG is an interesting challenge because it is influenced by many factors, including historical data and market sentiment driven by news.

The main objectives of this project are:

1. Create an IHSG prediction model using XGBoost.
2. Perform sentiment analysis on financial news as one of the input features for the prediction model.
3. Integrate sentiment data and historical data to improve the prediction accuracy of IHSG.

## Dataset

This project uses two types of datasets:

1. **Historical IHSG Data**: This dataset includes closing prices, trading volume, and other technical data collected from trusted sources like Yahoo Finance or IDX.
2. **Financial News Data**: Financial news articles collected from various sources, such as economic news websites, for sentiment analysis.

## Technologies Used

- **Python**: The main programming language for data analysis and model implementation.
- **XGBoost**: A machine learning algorithm based on *gradient boosting* for prediction.
- **LLM ChatGPT**: For sentiment analysis of news text.
- **Pandas and NumPy**: For data manipulation and analysis.
- **Matplotlib**: For data visualization.
- **Scikit-learn**: For data preprocessing and model evaluation.

## Results and Visualization

The results of this project include:

- Visualization of the relationship between historical IHSG data and financial news sentiment.
- Evaluation of the prediction model’s accuracy using metrics like RMSE, MAE, and R-squared.
- Forecast of IHSG movements based on the latest data.

## How to Run the Project

1. **Clone this repository**:
To duplicate the project, use the following command:
```bash
git clone https://github.com/Draxterra/Stock-IHSG-Forecast-with-XGBoost-with-Sentiment-Analysis.git

3. **Install dependencies**:
To install the requirements, use the following command:
```bash
pip install -r requirements.txt
```
## Run the notebook or script

- Use *Jupyter Notebook* to run files in the `notebooks` folder.
- Alternatively, run files in the `src` folder for the end-to-end pipeline.


## Contact
If you have any questions or would like to discuss this project, feel free to contact me via email: rizkiwirat13@gmail.com.


