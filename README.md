# ⚙️ Real-Time Process Monitoring System

A Python-based real-time process monitoring tool that tracks system processes, visualizes resource usage, and provides an interactive dashboard for better system insights.

---

## 🚀 Overview

This project monitors system processes in real time, providing detailed insights into CPU usage, memory consumption, and overall process behavior.

It helps in understanding how operating systems manage processes and resources dynamically.

---

## 🧠 Key Features

- 📊 Real-time process monitoring  
- ⚡ CPU and memory usage tracking  
- 🧾 Process-level insights (PID, name, usage stats)  
- 📈 Interactive dashboard for visualization  
- 🔄 Continuous live updates  

---

## 🛠️ Tech Stack

- **Python**
- **psutil** – system and process information  
- **matplotlib** – data visualization  
- **Tkinter / Streamlit** *(depending on your implementation)*  

---

## 📂 Project Structure


OS-Project/

│── realtime_process_monitoring_dashboard.py # Main dashboard UI

│── realtime_process_monitor_short_comments.py # Core monitoring logic

│── requirements.txt # Dependencies

│── README.md


---

## ⚙️ Installation & Setup

### 1. Clone the repository:
```bash
git clone https://github.com/Shraddhagupta37/OS-Project.git
cd OS-Project
```

### 2. Create a virtual environment:
```python -m venv .venv```

### 3. Activate the environment:

#### Windows

```.venv\Scripts\activate```

#### Mac/Linux

```source .venv/bin/activate```

### 4. Install dependencies:
```pip install -r requirements.txt```

---

## ▶️ How to Run
```python realtime_process_monitoring_dashboard.py```

---

## 📊 How It Works

- Uses psutil to fetch real-time system and process data

- Continuously updates CPU and memory usage

- Displays results in a structured dashboard

- Visualizes process-level resource consumption


## 🎯 Learning Outcomes

- Understanding of process management in operating systems

- Working with real-time data streams

- Building interactive dashboards in Python

- Practical usage of system-level libraries


## 🔮 Future Improvements

- Add process filtering & search

- Add alerts for high CPU/memory usage

- Improve UI/UX of the dashboard

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

## ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub!
