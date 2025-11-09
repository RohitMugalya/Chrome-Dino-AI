import os
import pandas as pd


class DinoAI:
    def __init__(self):
        self.jump_successful = 1
        self.jump_failed = 0
        self.features = ["take_off_distance"]
        self.target = "jump_status"
        self.dataset_path = "observations.csv"
        self.dataset_headers = self.features + [self.target]
        self.observations = self.load_observations()

    def load_observations(self):
        if os.path.exists(self.dataset_path):
            df = pd.read_csv(self.dataset_path)
            return df
        else:
            return pd.DataFrame(columns=self.dataset_headers)

    def save_observations(self):
        self.observations.to_csv(self.dataset_path, index=False)

    def record_observation(self, take_off_distance: float, jump_status: int):
        observation = {self.features[0]: take_off_distance, self.target: jump_status}
        self.observations.loc[len(self.observations)] = observation