# 🧮 Technical Note

**Project Title:** Math Adventures — AI-Powered Adaptive Learning Prototype
**Author:** Uday Kiran Bhushamoni
**Internship:** Artificial Intelligence Engineer – *The Product Works*
**Date:** November 3, 2025

---

## 🎯 Objective

The goal of this prototype is to design an **AI-powered adaptive learning system** that dynamically adjusts question difficulty based on learner performance. The focus area is **mathematics**, where the system personalizes learning pace and challenge level using performance tracking and adaptive logic.

The project demonstrates how artificial intelligence can enhance engagement and retention in digital learning environments by continuously optimizing difficulty according to the learner’s abilities.

---

## 🧱 System Architecture

### **1. Frontend Interface**

* Built using **Streamlit**, providing an interactive, browser-based interface.
* Users can select:

  * Starting difficulty (Easy / Medium / Hard)
  * Mathematical operations (addition, subtraction, multiplication, division)
  * Session length (number of questions)
  * Optional ML-based engine toggle

### **2. Backend Modules**

| Module                | Purpose                                                                 |
| --------------------- | ----------------------------------------------------------------------- |
| `puzzle_generator.py` | Dynamically generates math puzzles based on current difficulty.         |
| `tracker.py`          | Tracks learner performance, accuracy, and response time.                |
| `adaptive_engine.py`  | Core adaptive logic (rule-based or ML-driven).                          |
| `main.py`             | Streamlit app integrating all modules for user interaction.             |
| `model_trainer.py`    | Optional script to train and save a lightweight ML model (`model.pkl`). |

---

## ⚙️ Adaptive Logic

### **Rule-Based Engine**

* Calculates learner performance using:

  * Accuracy of last N responses (default: 5)
  * Average response time
* Decision logic:

  * **Increase difficulty** if accuracy ≥ 80% and average time < 5s
  * **Decrease difficulty** if accuracy < 40% or response time > 10s
  * Otherwise, **maintain same difficulty**

### **ML-Based Engine (Optional)**

* Uses a small predictive model (Logistic Regression or Decision Tree) trained on previous learner data (`model.pkl`).
* Inputs: recent accuracy, time per question
* Output: next difficulty label (`Easy`, `Medium`, or `Hard`)

---

## 📊 Performance Metrics

The system records:

* **Total questions attempted**
* **Overall accuracy**
* **Average response time**
* **Distribution of attempts by difficulty**
* **Recent activity log**

Learners can view this data at the end of each session via the **“📊 View Session Summary”** sidebar button.

---

## 💡 Key Features Implemented

* **Adaptive Difficulty Adjustment:** Real-time progression based on performance.
* **Progress Bar:** Displays visual progress through the session.
* **Encouraging Feedback:** Shows “✅ Correct!” or “❌ Incorrect” without revealing the correct answer.
* **Color-Coded Difficulty Indicators:** Easy 🟢 | Medium 🟡 | Hard 🔴.
* **Reset Anytime:** Learners can restart sessions from the sidebar at any time.
* **Summary-on-Demand:** Performance summary available only after completing all questions.
* **Difficulty Transition Chart:** Visual representation of how difficulty evolved.
* **Session Export:** Downloadable CSV log for analytics.

---

## 🧠 Design Rationale

* **Engagement:** Encouraging feedback and progress tracking make the learner experience interactive.
* **Focus:** Correct answers are hidden until session completion to preserve learning authenticity.
* **Flexibility:** Supports both rule-based and ML-driven adaptivity.
* **Transparency:** Data-driven summary helps evaluate learner performance objectively.

---

## 🧩 Scalability & Extensions

* Can be expanded to other subjects (e.g., vocabulary, coding challenges).
* Incorporate **reinforcement learning** for more complex personalization.
* Add **user profiling** to adjust difficulty per learner’s history.
* Integrate **database backend** (e.g., Firebase or SQLite) for multi-user tracking.
* Deploy on **Streamlit Cloud** or **Render** for web access.

---

## 📈 Expected Impact

This prototype demonstrates how adaptive intelligence can make learning platforms:

* More **personalized**
* More **engaging**
* More **effective** in improving knowledge retention

It serves as a foundational model for developing AI-driven educational tools that continuously adapt to each learner’s progress.

---

**Submitted by:**
**Uday Kiran Bhushamoni**
📧 [udaykiranbhushamoni@gmail.com](mailto:udaykiranbhushamoni@gmail.com)
📅 November 3, 2025
🧠 Artificial Intelligence Engineer Internship — *The Product Works*
