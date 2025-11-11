# Green Grocer

A lightweight desktop app for managing a small agri-retail setup (regions, farmers, products, etc.) built with **Python + Tkinter/CustomTkinter** and a SQL database. It demonstrates full **CRUD** flows with a clean, simple UI.

## Features
- ✅ Manage core entities (e.g., **Regions**, **Farmers**)
- ✅ Full **CRUD** (Create, Read, Update, Delete) from the UI
- ✅ Role-based actions (e.g., admin can add/update/delete)
- ✅ Treeview listing with inline refresh
- ✅ Clear success/error feedback
- ✅ Simple Chart for Visual Output

## Tech Stack
- **Python** (3.10+ recommended)
- **Tkinter** / **customtkinter**
- **ttk** Treeview
- **SQL database** (connected via `db.get_connection()`)
- Standard Python ecosystem (`requirements.txt`)

> Note: The exact DB driver (e.g., `psycopg2-binary` for PostgreSQL or `mysql-connector-python` for MySQL) is specified in your `requirements.txt` and used in `db.py` via `get_connection()`.

---

## Quick Start

### 1) Clone
```bash
git clone https://github.com/krishank-kureti/Green-Grocer.git
cd Green-Grocer
```

### 2) Create & activate a virtual environment
```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4) Configure database
Set your DB settings either in **environment variables** or in `db.py`. A common approach is a `.env` file (if the project uses `python-dotenv`):

```env
DB_HOST=localhost
DB_PORT=5432      
DB_NAME=green_grocer
DB_USER=your_user
DB_PASSWORD=your_password
```

Ensure your database has the required tables (examples from the UI code):
- `Region` → columns: `Region_ID`, `Region_Name`, `Climate`, `Soil_Type`
- `Farmer` → columns: `Farmer_ID`, `Farmer_Name`, `Farm_Size`, `Contact_Info`, `Region_ID`

> If you already have a schema/migrations folder in the repo, run those. Otherwise, create the tables manually according to your DB of choice.

### 5) Run the app
```bash
python main.py
```

---

## Using the App (CRUD Walkthrough)

### Regions
- **Create:** Enter `Region ID`, `Region Name`, `Climate`, `Soil Type` → click **Add Region**.
- **Read:** Regions appear in the table.
- **Update:** Select a row → **Update Selected** → edit fields in the dialog → **OK**.
- **Delete:** Select a row → **Delete Selected** → confirm.

### Farmers
- **Create:** Enter `Farmer ID`, `Name`, `Farm Size`, `Contact`, `Region ID` → **Add Farmer**.
- **Read:** Farmers appear in the table.
- **Update:** Select a row → **Update Selected** → edit fields in the dialog → **OK**.
- **Delete:** Select a row → **Delete Selected** → confirm.
---

## Project Structure (typical)
Green-Grocer/
├── screens/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── charts.py
│   ├── farmers.py
│   ├── login.py
│   ├── orders.py
│   ├── produce.py
│   ├── queries.py
│   └── regions.py
├── .gitignore
├── db.py
├── main.py
├── requirements.txt
├── theme.py
└── utils.py