# tracker.py
import time
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Trial:
    question: str
    correct_answer: int
    user_answer: int
    correct: bool
    time_taken: float
    difficulty: str
    operation: str

@dataclass
class SessionTracker:
    trials: List[Trial] = field(default_factory=list)

    def log_trial(self, question: str, correct_answer: int, user_answer: int, time_taken: float, difficulty: str, operation: str):
        self.trials.append(Trial(
            question=question,
            correct_answer=correct_answer,
            user_answer=user_answer,
            correct=(user_answer == correct_answer),
            time_taken=time_taken,
            difficulty=difficulty,
            operation=operation
        ))

    def accuracy(self) -> float:
        if not self.trials: return 0.0
        return sum(1 for t in self.trials if t.correct) / len(self.trials)

    def avg_time(self) -> float:
        if not self.trials: return 0.0
        return sum(t.time_taken for t in self.trials) / len(self.trials)

    def last_n_accuracy(self, n: int = 5) -> float:
        window = self.trials[-n:]
        if not window: return 0.0
        return sum(1 for t in window if t.correct) / len(window)

    def counts_by_difficulty(self) -> Dict[str,int]:
        d = {}
        for t in self.trials:
            d[t.difficulty] = d.get(t.difficulty, 0) + 1
        return d
