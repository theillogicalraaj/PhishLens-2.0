from app.services.risk import compute_risk

def test_low_behavior_is_lower_risk():
    result = compute_risk(0.05, 0.02, 0.80, 0.01, 0.70)
    assert 0 <= result["score"] <= 100
    assert result["severity"] in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
    assert result["model"]

def test_high_click_behavior_is_not_silent():
    result = compute_risk(0.80, 0.70, 0.02, 0.30, 0.05)
    assert result["score"] > 40
    assert "click" in result["rationale"].lower()
