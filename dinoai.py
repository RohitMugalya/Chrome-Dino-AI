import os
import pandas as pd


class DinoAI:
    def __init__(self):
        self.jump_successful = 1
        self.jump_failed = 0
        self.dataset_path = "observations.csv"
        self.dataset_headers = ["take_off_distance", "jump_status"]
        self.observations = self.load_observations()

    def load_observations(self):
        if os.path.exists(self.dataset_path):
            df = pd.read_csv(self.dataset_path)
            return df.values.tolist()
        else:
            return []

    def save_observations(self):
        df = pd.DataFrame(self.observations, columns=self.dataset_headers)
        df.to_csv(self.dataset_path, index=False)

    def record_observation(self, take_off_distance, jump_status):
        self.observations.append([take_off_distance, jump_status])
