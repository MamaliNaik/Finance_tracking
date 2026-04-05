
#  Finance Tracking System (Django + DRF)

##  Overview

A role-based Finance Tracking System built using Django and Django REST Framework. This application allows users to manage income and expenses, track financial activity, and analyze data efficiently.

The system supports different user roles with controlled access and provides RESTful APIs for seamless integration.

---

##  Features

*  Custom User Authentication (Role-Based)
*  Track Income & Expenses
*  Search Transactions by Category
*  Date-wise Financial Records
*  Monthly Aggregation & Analysis
*  Role-Based Access Control (RBAC)
*  REST API Support (CRUD operations)
*  Notes support for transactions

---

## 🧱 Tech Stack

 **Backend:** Django, Django REST Framework
 **Database:** SQLite (default, can be changed)
 **Authentication:** Django Custom User Model
**API:** RESTful APIs

---

##  User Roles

* **Viewer**

  * Can view transactions
* **Analyst**

  * Can analyze financial data
* **Admin**

  * Full access (CRUD operations)

---

##  Models

### User Model

* Extends Django's AbstractUser
* Includes role field:

  * viewer
  * analyst
  * admin

### Transaction Model

* user → ForeignKey
* amount→ Float
* type → Income / Expense
* category → String
* date → Date
* notes → Optional text

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

git clone <your-repo-url>
cd finance_tracking

### 2️⃣ Create Virtual Environment

python -m venv venv
venv\Scripts\activate   # Windows


### 3️⃣ Install Dependencies


pip install -r required.txt


### 4️ Apply Migrations


python manage.py makemigrations
python manage.py migrate


### 5️ Run Server

python manage.py runserver


---

