# adaptive_engine.py
from typing import Optional
import joblib
import numpy as np

DIFFICULTY_ORDER = ["Easy", "Medium", "Hard"]

class RuleBasedEngine:
    """
    Simple sliding-window rule-based difficulty adjuster.
    - If last N accuracy >= up_thresh -> increase difficulty by one step.
    - If last N accuracy <= down_thresh -> decrease difficulty by one step.
    - Otherwise keep same.
    Also uses average time as tie-breaker (fast & correct encourages up).
    """
    def __init__(self, window_size: int = 5, up_thresh: float = 0.8, down_thresh: float = 0.5, fast_time_threshold: float = 6.0):
        self.window_size = window_size
        self.up_thresh = up_thresh
        self.down_thresh = down_thresh
        self.fast_time_threshold = fast_time_threshold

    def next_difficulty(self, current: str, last_n_accuracy: float, last_n_avg_time: Optional[float] = None) -> str:
        idx = DIFFICULTY_ORDER.index(current)
        if last_n_accuracy >= self.up_thresh:
            # consider time
            if last_n_avg_time is None or last_n_avg_time <= self.fast_time_threshold:
                return DIFFICULTY_ORDER[min(len(DIFFICULTY_ORDER)-1, idx + 1)]
            else:
                # if slow but accurate, keep same
                return current
        elif last_n_accuracy <= self.down_thresh:
            return DIFFICULTY_ORDER[max(0, idx - 1)]
        else:
            return current

class MLModelEngine:
    """
    Wrapper around a trained sklearn model that predicts next difficulty index (0,1,2)
    Features expected: [current_idx, last_n_accuracy, last_n_avg_time]
    """
    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)

    def next_difficulty(self, current: str, last_n_accuracy: float, last_n_avg_time: float) -> str:
        current_idx = DIFFICULTY_ORDER.index(current)
        x = np.array([[current_idx, last_n_accuracy, last_n_avg_time]])
        pred_idx = int(self.model.predict(x)[0])
        return DIFFICULTY_ORDER[max(0, min(pred_idx, len(DIFFICULTY_ORDER)-1))]
