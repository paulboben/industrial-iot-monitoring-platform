import os
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest

MODEL_PATH = "storage/model.joblib"

class AnomalyModel:
    def __init__(self):
        self.model = None
        self.load()

    def load(self):
        if os.path.exists(MODEL_PATH):
            self.model =joblib.load(MODEL_PATH)
            print("model loaded")
        else:
            print("No model found, Train a new one.")

    def train(self, samples):
        X = np.array(samples)
        self.model = IsolationForest(contamination=0.05) 
        self.model.fit(X) 
        joblib.dump(self.model, MODEL_PATH)

    def predict(self, values):
        if self.model is None:
            return ("no_model", -1)

        X = np.array(values).reshape(1, -1)
        pred = self.model.predict(X)[0]
        score = self.model.decision_function(X)[0]

        if pred == -1:
            return ("anomaly", score)
        return ("normal", score)