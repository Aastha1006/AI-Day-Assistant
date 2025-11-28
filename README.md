# ⭐ **README.md for AI Day Assistant**

```markdown
# 🤖 AI Day Assistant  
An AI-powered productivity assistant built using Python, NLP, and Streamlit.  
It converts messy tasks into a structured day plan with priorities, categories, time estimates, and interactive task management.

---

## 🚀 Features

### ✔ AI Task Understanding (Zero-shot Classification)
- Automatically categorizes tasks (Bug Fix, Documentation, Testing, Learning, Deployment, etc.)
- Uses a zero-shot classification model to understand any type of task without training.

### ✔ Smart Priority Assignment
- AI assigns High/Medium/Low priority based on task type and user preference.
- Supports manual priority overrides.

### ✔ Time Estimation  
- Predicts estimated time per task using rule-based logic + task patterns.

### ✔ Interactive Task Dashboard
- Checkboxes to mark tasks as completed.
- Dynamic UI updates.
- Fireworks celebration when all tasks are completed. 🎉

### ✔ Persistent Storage  
- Tasks remain saved even after refreshing.
- Reset options:
  - Clear tasks for same user
  - Start fresh with a new user

### ✔ Friendly AI Assistant Interface
- Greets user by name.
- Provides motivational summaries.
- Modern gradient UI with emojis and clean design.

---

## 🧠 Tech Stack

**Languages & Libraries**
- Python  
- Streamlit  
- Transformers (Zero-shot model)  
- Pandas  
- NumPy  

**Other**
- Session State Management  
- Custom CSS for gradients and animations  

---

## 📌 Project Architecture

```

AI Day Assistant
│
├── app.py                # Main Streamlit application
├── requirements.txt      # Libraries needed
├── saved_tasks.json      # Persistent user tasks (auto-generated)
└── README.md             # Project documentation

````

---

## 🛠 Installation & Setup

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/Aastha1006/AI-Day-Assistant.git
cd AI-Day-Assistant
````

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the app

```bash
streamlit run app.py
```

The app will open in your browser at:

```
http://localhost:8501
```

---

## 🧪 Demo (Screenshots)

Example:

*![Home Page](assests/home.png)
)
* AI summary card
* Task planner UI
* Celebration screen

---

## 🌟 Why This Project Stands Out

* Uses NLP and zero-shot learning (real AI, not a basic ML model).
* Fully interactive UI built from scratch.
* Clean, modern design with gradients.
* Useful real-world application for productivity.
* Built without external AI APIs — model runs locally.

---

## 📄 License

This project is open-source and free to use.

---

## 🙋‍♀️ Author

**Aastha Ukey**

* GitHub: [https://github.com/Aastha1006](https://github.com/Aastha1006)
* LinkedIn: [https://linkedin.com/in/aastha-ukey-508905240](https://linkedin.com/in/aastha-ukey-508905240)

```
