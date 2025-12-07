import os
import re
import joblib

from sklearn.linear_model import LogisticRegression
import pandas as pd

def extract_generation_number(filename):
    match = re.search(r'generation_(\d+)\.pkl', filename)
    if match:
        return int(match.group(1))
    return -1

class DinoAI:
    def __init__(self):
        self.jump_successful = 1
        self.jump_failed = 0
        self.features = ["take_off_distance"]
        self.target = "jump_status"
        self.dataset_path = "observations.csv"
        self.dataset_headers = self.features + [self.target]
        self.observations = self.load_observations()
        self.model = self.load_model()
    
    @property
    def has_learned(self):
        if hasattr(self.model, "coef_"):
            return True
        return False

    def predict_jump(self, estimated_distance: float) -> int:
        input_data = pd.DataFrame([[estimated_distance]], columns=self.features)
        prediction = self.model.predict(input_data)
        return int(prediction[0])
    
    def reinforce(self):
        if self.jump_failed not in self.observations[self.target].values:
            print("Teach DinoAI when jump fails before reinforcing.")
        if self.jump_successful not in self.observations[self.target].values:
            print("Teach DinoAI when jump succeeds before reinforcing.")

        if self.observations[self.target].nunique() > 1:
            X = self.observations[self.features]
            y = self.observations[self.target]
            print("DinoAI is learning from observations...")
            self.model.fit(X, y)
            self.save_model()
    
    def load_model(self, model_base_dir="generations/"):
        generations = os.listdir(model_base_dir)
        self.generations = [os.path.join(model_base_dir, gen) for gen in generations if os.path.isfile(os.path.join(model_base_dir, gen))]
        self.generations.sort(key=extract_generation_number)

        if not self.generations:
            return LogisticRegression()
        return joblib.load(self.generations[-1])
        
    
    def load_observations(self):
        if os.path.exists(self.dataset_path):
            df = pd.read_csv(self.dataset_path)
            return df
        else:
            return pd.DataFrame(columns=self.dataset_headers)
    
    def save_model(self, model_base_dir="generations/"):
        generation_number = len(self.generations) + 1
        if not os.path.exists(model_base_dir):
            os.makedirs(model_base_dir)
        model_path = os.path.join(model_base_dir, f"generation_{generation_number}.pkl")
        joblib.dump(self.model, model_path)

    def save_observations(self):
        self.observations.to_csv(self.dataset_path, index=False)

    def record_observation(self, take_off_distance: float, jump_status: int):
        observation = {self.features[0]: take_off_distance, self.target: jump_status}
        self.observations.loc[len(self.observations)] = observation


if __name__ == "__main__":
    dino_ai = DinoAI()
    dino_ai.load_model()
    print(dino_ai.predict_jump(300.0))