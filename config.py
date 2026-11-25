import pandas as pd
from pathlib import Path 

class AppConfig:
    def __init__(self):
        self.base_path = str(Path(__file__).resolve().parent)
        self.state_file = self.base_path + r"\stateAbb.csv"

        self.US_LIST = pd.read_csv(self.state_file)

        # GUI state
        self.window = None
        self.input_stream = None
        self.secure = None

        # default cities
        self.sample_cities = [
            "Jakarta", "Dhaka", "Tokyo", "New Delhi",
            "Shanghai", "Cairo", "Kolkata", "Seoul"
        ]

# Singleton-style config instance
config = AppConfig()