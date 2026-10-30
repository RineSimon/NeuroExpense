# 🧠 NeuroExpense

[![Django](https://img.shields.io/badge/Framework-Django%205.x-092e20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Language-Python%203.10+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

**NeuroExpense** is a state-of-the-art personal finance management system designed for the modern user. It serves as your "Financial Command Center," bridging the gap between complex accounting software and simple note-taking apps.

The "Neuro" prefix signifies the application's focus on cognitive financial health—providing the psychological feedback needed to spend wisely through visual cues, progress bars, and color-coded alerts.

---

## 🌟 Key Features

-   **Intelligent Tracking**: High-friction manual logging to create financial awareness.
-   **Glassmorphism UI**: A premium, modern interface with translucent effects and smooth animations.
-   **Advanced Analytics**: Real-time spending projections, daily averages, and weekly comparisons.
-   **Professional Reporting**: Generate high-fidelity PDF and CSV reports of your financial data.
-   **Budget Management**: Set and track monthly thresholds for different spending categories.
-   **Security First**: Built with Django's robust security features, including CSRF protection and session management.

---

## 🛠️ Tech Stack

-   **Backend**: Python / Django 5.x (Robust ORM & Security)
-   **Frontend**: HTML5, Vanilla CSS (Glassmorphism), Vanilla JavaScript
-   **Visualization**: Chart.js (Interactive financial charts)
-   **Database**: SQLite3 (Portable & Fast)
-   **Reporting**: xhtml2pdf & ReportLab (High-fidelity document generation)

---

## 🚀 Quick Start

### Prerequisites
-   Python 3.10 or higher
-   Git

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/bharathkrish2608/NeuroExpense.git
    cd NeuroExpense
    ```

2.  **Set up Virtual Environment**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    pip install pillow  # For receipt image processing
    ```

4.  **Database Setup**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python populate_categories.py  # Populates initial spending categories
    ```

5.  **Create Superuser (Optional)**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the Server**
    ```bash
    python manage.py runserver
    ```
    Visit `http://127.0.0.1:8000/` in your browser.

---

## 📂 Module Breakdown

### 🏠 Accounts
Handles user authentication, profile management (currency preferences, avatars), and UI theme toggles.

### 💸 Expenses
The core module for logging transactions, managing categories with unique icons/colors, and tracking receipts.

### 📊 Analytics
The "Brain" of the project. Processes raw transaction data into actionable insights like predicted month-end totals and spending trends.

### 📄 Reports
Data export hub supporting professional PDF statements and spreadsheet-ready CSV downloads.

---

## 🎨 Design Aesthetic
NeuroExpense uses a centralized "Glassmorphism" system defined by:
-   **Translucent Backgrounds**: Layered effects using `backdrop-filter`.
-   **Dynamic Animations**: Subtle hover scales and animated data growth in charts.
-   **Responsive Layouts**: Seamless transition from mobile hamburger menus to full desktop dashboards.

---

## 📝 Developer Notes
-   **Database Agnostic**: While it uses SQLite by default, the project is ready for PostgreSQL/MySQL by simply updating the `settings.py` configuration.
-   **Performance**: Utilizes Django's `select_related` for optimized SQL queries.
-   **Scalability**: Modular architecture allows for easy addition of new financial tracking modules.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---
Created with ❤️ by [Bharath](https://github.com/bharathkrish2608)
