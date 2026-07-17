![Python](https://img.shields.io/badge/Python-3.11-blue)

![Tests](https://img.shields.io/badge/Tests-34-success)

![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)

![CI](https://github.com/Thamizh3824/system-operations-toolkit/actions/workflows/python-tests.yml/badge.svg)

# 🚀 System Operations Toolkit

A modular Python-based command-line toolkit for log analysis, service health monitoring, system resource monitoring, and operational reporting. Designed using object-oriented principles with automated testing, CI/CD, and an HTML dashboard.

---

## 📸 Dashboard

![Dashboard](assets/dashboard.png)

---

## ✨ Features

- 📄 Parse and analyze application log files
- 🔍 Search logs by keyword
- 📅 Filter logs by date or timestamp
- 📊 Identify top recurring errors
- 🚨 Configurable alert engine using JSON thresholds
- 🌐 Monitor HTTP service availability
- 💻 Monitor CPU, Memory, Disk, and Network usage
- 📈 Generate HTML monitoring dashboard
- 📑 Export reports to CSV
- 📝 Rotating application logging
- ⚙️ JSON configuration management
- 🧪 34 automated Pytest test cases
- ✅ 100% code coverage
- 🤖 GitHub Actions CI

---

## 🏗️ Project Architecture

```text
system-operations-toolkit
│
├── config/
├── core/
│   ├── alert_engine.py
│   ├── health_checker.py
│   ├── log_analyzer.py
│   ├── report_generator.py
│   └── resource_monitor.py
│
├── models/
├── utils/
├── tests/
├── reports/
├── logs/
├── assets/
└── main.py
```

---

## ⚙️ Installation

```bash
git clone <repository-url>

cd system-operations-toolkit

python -m venv .venv

source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🚀 Usage

```bash
python main.py summary

python main.py search database

python main.py date 2026-07-15

python main.py alerts

python main.py health

python main.py monitor

python main.py dashboard
```

---

## 🧪 Testing

Run all tests

```bash
pytest
```

Run with coverage

```bash
pytest --cov=. --cov-report=term
```

Current Status

- ✅ 34 Automated Tests
- ✅ 100% Code Coverage
- ✅ GitHub Actions CI

---

## 🛠️ Technologies

- Python 3.11
- Pytest
- Requests
- psutil
- HTML/CSS
- Logging
- JSON
- Git
- GitHub Actions

---

## 📌 Future Improvements

- Docker containerization
- AWS deployment
- Email notifications
- SQLite integration
- REST API
- Grafana dashboard integration

---

## 👨‍💻 Author

**Thamizharasan T**

GitHub: https://github.com/Thamizh3824
LinkedIn: https://www.linkedin.com/in/thamizharasan-t-b6aa25291