from functools import lru_cache
import numpy as np
from sklearn.linear_model import LogisticRegression

@lru_cache(maxsize=1)
def model():
    # Synthetic, educational baseline data. Replace with validated organizational data for production.
    X = np.array([
        [0.02, 0.01, 0.80, 0.05, 0.00],
        [0.10, 0.08, 0.60, 0.15, 0.02],
        [0.20, 0.15, 0.40, 0.20, 0.04],
        [0.35, 0.30, 0.25, 0.40, 0.10],
        [0.55, 0.48, 0.20, 0.65, 0.18],
        [0.75, 0.68, 0.10, 0.80, 0.35],
        [0.90, 0.85, 0.05, 0.95, 0.55],
        [0.45, 0.20, 0.45, 0.50, 0.25],
        [0.65, 0.35, 0.30, 0.75, 0.30],
        [0.15, 0.05, 0.70, 0.10, 0.01],
    ])
    y = np.array([0,0,0,0,1,1,1,0,1,0])
    clf = LogisticRegression(max_iter=500)
    clf.fit(X, y)
    return clf


def compute_risk(open_rate: float, click_rate: float, report_rate: float, repeat_click_rate: float, completion_rate: float):
    features = np.array([[open_rate, click_rate, report_rate, repeat_click_rate, completion_rate]])
    clf = model()
    probability = float(clf.predict_proba(features)[0, 1])
    score = round(probability * 100, 1)
    reasons = []
    if click_rate >= 0.30:
        reasons.append("High simulation click rate")
    elif click_rate >= 0.15:
        reasons.append("Moderate simulation click rate")
    if report_rate < 0.10:
        reasons.append("Low reporting rate")
    if repeat_click_rate >= 0.15:
        reasons.append("Repeat-click behavior is elevated")
    if completion_rate < 0.30:
        reasons.append("Training completion is low")
    if not reasons:
        reasons.append("Behavioral indicators are currently low-risk")
    severity = "LOW" if score < 35 else "MEDIUM" if score < 60 else "HIGH" if score < 80 else "CRITICAL"
    return {"score": score, "severity": severity, "model": "Synthetic Logistic Regression baseline", "rationale": "; ".join(reasons)}
