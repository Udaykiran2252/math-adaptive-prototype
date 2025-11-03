# main.py
import streamlit as st
from puzzle_generator import generate_puzzle
from tracker import SessionTracker
from adaptive_engine import RuleBasedEngine, MLModelEngine
import time
import os
import random
import pandas as pd

# --- Streamlit Page Config ---
st.set_page_config(page_title="Math Adventures — AI-Powered Adaptive Learning", layout="centered")

# --- Session State Initialization ---
if "tracker" not in st.session_state:
    st.session_state.tracker = SessionTracker()
if "current_difficulty" not in st.session_state:
    st.session_state.current_difficulty = "Easy"
if "engine" not in st.session_state:
    st.session_state.engine = None
if "model_path" not in st.session_state:
    st.session_state.model_path = None
if "show_summary" not in st.session_state:
    st.session_state.show_summary = False
if "feedback" not in st.session_state:
    st.session_state.feedback = None

# --- App Title ---
st.title("🧮 Math Adventures — AI-Powered Adaptive Learning Prototype")

# --- SIDEBAR: Session Setup ---
with st.sidebar:
    st.header("⚙️ Session Setup")
    name = st.text_input("Learner name", value="Student")
    start_level = st.selectbox("Starting difficulty", ["Easy", "Medium", "Hard"], index=0)
    ops = st.multiselect(
        "Select operations to include",
        ["addition", "subtraction", "multiplication", "division"],
        default=["addition", "subtraction"],
    )
    use_ml = st.checkbox("Use ML Engine (optional)", value=False)
    if use_ml:
        model_file = st.text_input("Model path (train via model_trainer.py)", value="model.pkl")
    else:
        model_file = ""
    max_questions = st.number_input(
        "Number of questions this session", min_value=5, max_value=50, value=10, step=1
    )

    # --- RESET BUTTON (Works Anytime) ---
    if st.button("🚀 Start / Reset Session"):
        st.session_state.tracker = SessionTracker()
        st.session_state.current_difficulty = start_level
        st.session_state.show_summary = False
        st.session_state.feedback = None

        for key in ["current_question", "answer_input", "q_start_time"]:
            if key in st.session_state:
                del st.session_state[key]

        if use_ml and model_file and os.path.exists(model_file):
            st.session_state.engine = MLModelEngine(model_file)
            st.session_state.model_path = model_file
        else:
            st.session_state.engine = RuleBasedEngine()
            st.session_state.model_path = None

        st.success("🔄 Session has been reset. You can start fresh!")
        st.rerun()

    # --- Session Tracker Button (Appears After Completion) ---
    if len(st.session_state.tracker.trials) >= max_questions:
        st.markdown("---")
        st.success("✅ Session Completed!")
        if st.button("📊 View Session Summary", key="summary_button"):
            st.session_state.show_summary = True
    else:
        st.session_state.show_summary = False

# --- Ensure Adaptive Engine Exists ---
if st.session_state.engine is None:
    st.session_state.engine = RuleBasedEngine()

# --- Header Info ---
st.subheader(f"Learner: {name}")

# --- Difficulty Display with Color ---
diff = st.session_state.current_difficulty
if diff == "Easy":
    st.markdown("🟢 **Current Difficulty: Easy**")
elif diff == "Medium":
    st.markdown("🟡 **Current Difficulty: Medium**")
else:
    st.markdown("🔴 **Current Difficulty: Hard**")

# --- Progress Bar ---
progress = len(st.session_state.tracker.trials)
if max_questions > 0:
    st.progress(progress / max_questions)
st.write(f"**Question {progress + 1 if progress < max_questions else max_questions} of {max_questions}**")

# --- MAIN: Puzzle Section ---
if len(st.session_state.tracker.trials) >= max_questions:
    st.info("🎯 Session complete! You can now view your summary from the sidebar.")
else:
    if st.button("🧩 Get Next Puzzle"):
        op_choice = random.choice(ops) if ops else None
        p = generate_puzzle(st.session_state.current_difficulty, operation=op_choice)
        st.session_state.current_question = p
        st.session_state.q_start_time = time.time()
        st.session_state.feedback = None
        st.rerun()

if "current_question" in st.session_state:
    p = st.session_state.current_question
    st.markdown(f"### Question: {p['question']}")
    ans = st.text_input("Your answer", key="answer_input")

    if st.button("Submit Answer"):
        t_taken = time.time() - st.session_state.q_start_time
        try:
            user_ans = int(ans.strip())
        except:
            user_ans = None

        correct_answer = p["answer"]
        st.session_state.tracker.log_trial(
            question=p["question"],
            correct_answer=correct_answer,
            user_answer=user_ans if user_ans is not None else -99999,
            time_taken=t_taken,
            difficulty=p["difficulty"],
            operation=p["operation"],
        )

        # --- Gentle feedback without revealing the answer ---
        if user_ans == correct_answer:
            st.session_state.feedback = "✅ Correct! Great job — keep it up!"
        else:
            st.session_state.feedback = "❌ Incorrect. Don't worry, you'll get the next one!"

        # --- Adaptive Difficulty Decision ---
        last_n = st.session_state.tracker.last_n_accuracy(5)
        last_n_trials = st.session_state.tracker.trials[-5:]
        last_n_avg_time = sum(t.time_taken for t in last_n_trials) / len(last_n_trials) if last_n_trials else 0

        engine = st.session_state.engine
        try:
            next_diff = engine.next_difficulty(
                st.session_state.current_difficulty, last_n, last_n_avg_time
            )
        except TypeError:
            next_diff = engine.next_difficulty(
                st.session_state.current_difficulty, last_n, last_n_avg_time or 8.0
            )

        st.session_state.current_difficulty = next_diff

        for key in ["current_question", "answer_input"]:
            if key in st.session_state:
                del st.session_state[key]

        st.rerun()

# --- Instant Feedback Message ---
if st.session_state.feedback:
    if "✅" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.warning(st.session_state.feedback)

# --- SHOW SUMMARY ONLY WHEN BUTTON CLICKED ---
if st.session_state.get("show_summary", False):
    st.markdown("---")
    st.header("📈 Session Summary")
    tracker = st.session_state.tracker

    st.write(f"**Total Questions Answered:** {len(tracker.trials)}")
    st.write(f"**Overall Accuracy:** {tracker.accuracy() * 100:.1f}%")
    st.write(f"**Average Time per Question:** {tracker.avg_time():.2f} seconds")
    st.write("**Attempts by Difficulty:**", tracker.counts_by_difficulty())

    if tracker.trials:
        st.markdown("### 🧾 Recent Attempts")
        for t in tracker.trials[-10:]:
            st.write(
                f"{t.question} | Your answer: {t.user_answer} | Correct: {t.correct_answer} | "
                f"{'✅' if t.correct else '❌'} | Time: {t.time_taken:.2f}s | Level: {t.difficulty}"
            )

        # --- Difficulty Progress Chart ---
        st.markdown("### 📊 Difficulty Transition Overview")
        diff_numeric = [1 if t.difficulty == "Easy" else 2 if t.difficulty == "Medium" else 3 for t in tracker.trials]
        st.line_chart(diff_numeric)

        # --- Export Button ---
        df = pd.DataFrame([t.__dict__ for t in tracker.trials])
        st.download_button("⬇️ Download Session Data", df.to_csv(index=False), "session_log.csv")

st.markdown("---")
st.caption("Tip: Use model_trainer.py to train a small ML model (model.pkl) and test the ML-based engine.")
