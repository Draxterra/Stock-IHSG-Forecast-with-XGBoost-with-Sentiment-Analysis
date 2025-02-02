import logging
import os
from datetime import datetime

from Model import ModelFactory
from Process import Dataproc, DatasetConfig
from Utils import WriteEvaluation

# Define the directory for logs
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)  # Create the log directory if it doesn't exist

# Create a filename based on the current date and time
log_filename = os.path.join(log_dir, datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log"))

# Configure logging to output to the file with the specified format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(),  # Also output to console
    ],
)

if __name__ == "__main__":

    #################### Setup Area ###################################
    model_type = "Xgboost"  # Pastikan nama konsisten dengan di Factory : SVR, Xgboost, LSTM, Ridge,LR
    config = DatasetConfig(
        file_path=r"Dataset\Stock\IHSG_Stock_Clean.csv",
        # file_path_sentiment=r"Dataset\News\Daily_Sentiment_Score.csv",  # Uncomment if you want to use sentiment
        split_ratio=0.8,
        n_in=10,
        sentiment_scenario=5,  # 1 = Normal, 2 = {Sigma i=1 to n when Xi/2}
        drop_columns=True,
        drop_columns_list=["Change%", "Volume"],  # Kolom yang akan di-drop dari dataset
        start_date="2014-01-03",  # Minimum 2014-01-03
        end_date="2024-08-06",  # Maximum 2024-08-06
    )
    use_returns = True # Jika False maka akan menggunakan Close
    return_type = "log"  # return_type bisa "absolute" atau "relative" atau "log"
    use_custom_params = (
        True  # Jika ingin menggunakan parameter custom jangan lupa set to True
    )
    params = {
        'n_estimators': 3000,
        'max_depth': 7,
        'min_child_weight': 2,
        'learning_rate': 0.48
    }  # custom params, sesuaikan sesuai parameter model yang dipakai

    ####################################################

    dataproc = Dataproc(config)

    if use_custom_params and params:
        model = ModelFactory.use_model(
            model_type, dataproc, params
        )  # , params untuk parameter model
    else:
        model = ModelFactory.use_model(
            model_type, dataproc
        )  # , params untuk parameter model

    print(model.X_train.shape)
    model.create_model(use_returns=use_returns, return_type=return_type)
    model.show_summary()
    model.plot_prediction()

    print(model.y_val[:10])
    # model.save_model() #Jika ingin menyimpan model
    WriteEvaluation(
        model.evaluation, model_type, model.get_params(), use_returns, return_type
    )


# Buat TA
# 1. Skenario Sentiment Bisa Per Case
# 2. Skenario lag Data
# 3. Tune dan Tanpa tune Model
# 4. Model Serupa
# 5. Saham Dalam IHSG

# TODO
# Bikin Scenario 1 - 3 Sentiment -- TBA -- Scenario 2 Done
# seperate Sentiment Model -- TBA
# Optuna Tuning -- TBA
# Making Unit Test -- TBA
# load model -- TBA
# Show in Streamlit -- Done
# More Advance Write Evaluation for etl to csv  -- Done
# Modular Sentiment Per Scenario -- Done
# Add Sentiment Dataset -- Done
# Combine Sentiment and Stock Data -- DONE
# add function filter time data -- DONE
