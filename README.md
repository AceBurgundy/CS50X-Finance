# 💰 CS50X-Finance

**CS50X-Finance** is a full-stack web application built with **Flask** that simulates buying, selling, and tracking stocks using real-time stock data via API. It features user authentication, transaction history, portfolio tracking, and stock lookup functionality.

> 📘 This project was my **first introduction to APIs**, developed as part of the **CS50X Introduction to Computer Science** course by Harvard.

## 🧠 Key Features

### 📈 Stock Portfolio Management

* View current holdings, prices, and total portfolio value
* Real-time price updates via API integration

### 🛒 Buy & Sell Stocks

* Search stocks by symbol and place buy/sell orders
* Handles balance checks, ownership validation, and transaction logging

### 🔍 Stock Quote Lookup

* Retrieve real-time quotes for any valid stock symbol
* API-powered lookup with validation and error handling

### 💵 Cash Management

* Users start with a fixed amount of cash
* Additional feature: simulate adding funds to your account

### 📜 Transaction History

* View all buy/sell history with timestamps and prices
* Tracks individual transactions, not just current holdings

### 👤 User Authentication

* Secure user registration and login system
* Passwords hashed with `werkzeug.security`
* Session-based login management using Flask-Session

## 🛠️ Tech Stack

* **Python**
* **Flask** – Web framework
* **Jinja2** – HTML templating
* **SQLite** – Lightweight relational database
* **Flask-Session** – Session management
* **CS50 Library** – SQL helper for Python
* **API** – Real-time stock lookup using a configured API key

## 📂 Project Structure (Simplified)

```
CS50X-Finance/
├── static/              # CSS and static assets
├── templates/           # HTML templates
├── helpers.py           # Custom functions (e.g., API lookup, formatting)
├── application.py       # Flask app with all routes
├── finance.db           # SQLite database (generated)
└── requirements.txt     # Project dependencies
```

## 📌 Setup & Configuration

> ⚠️ You must have a valid API key set as an environment variable for stock lookups to work.

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/cs50x-finance.git
   cd cs50x-finance
   ```

2. **Create and activate virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set your API key**

   ```bash
   export API_KEY='your_api_key_here'  # On Windows: set API_KEY=your_api_key_here
   ```

5. **Run the application**

   ```bash
   flask run
   ```

## 🗃️ Database Tables

### `users`

* `id`, `username`, `hash`, `cash`

### `history`

* `user_id`, `symbol`, `name`, `shares`, `price`, `type`, `time`

> Transactions are recorded in the `history` table, while the `users` table tracks user details and available cash.

## 🧪 Learning Outcomes

* First exposure to **RESTful APIs** and how to integrate them in Python
* Implemented secure **user authentication** and session handling
* Learned **full-stack web development** using Flask and Jinja2
* Built and queried a **relational database** using SQL and Python
* Handled **real-world errors**, edge cases, and validations

## 👨‍💻 Author

Developed by [@AceBurgundy](https://github.com/AceBurgundy)
📚 Created as part of the **CS50X Harvard** course – *Introduction to Computer Science*

## 📄 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for more information.
