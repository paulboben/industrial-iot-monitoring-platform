from fastapi import FastAPI
from model import AnomalyModel
from schemas import TrainRequest, PredictionRequest

app = FastAPI()

model = AnomalyModel()

@app.get("/")
def root():
    return {"message": "ML Backend Running"}

@app.post("/train")
def train_model(req: TrainRequest):
    model.train(req.samples)
    return {"status": "trained", "samples_used": len(req.samples)}

@app.post("/predict")
def predict_model(req: PredictionRequest):
    result, score = model.predict(req.values)
    return {
        "status": result,
        "score": float(score),
        "input": req.values
    }