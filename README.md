# 🌍 Country Currency & Exchange API

A RESTful API built with **Django + Django REST Framework** that fetches country and currency data from external APIs, computes estimated GDP, stores results in a local database, and exposes endpoints for CRUD operations, statistics, and a summary image.

This project was developed as part of the **HNG 13 Backend Stage Two** task.

---

## 🚀 Features

* Fetches all countries from [REST Countries API](https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies)
* Fetches currency exchange rates from [Open Exchange Rate API](https://open.er-api.com/v6/latest/USD)
* Stores and updates data in a Django database
* Computes **estimated GDP = population × random(1000–2000) ÷ exchange_rate**
* Provides CRUD endpoints for countries
* Returns total countries and last refresh timestamp
* Generates and serves a summary image containing:

  * Total number of countries
  * Top 5 countries by estimated GDP
  * Timestamp of last refresh
* Logs every request (method, URL, headers, and body) for debugging

---

## 🧩 Tech Stack

* **Backend:** Django 4.2 + Django REST Framework
* **Database:** SQLite (default, supported by PythonAnywhere)
* **Language:** Python 3.8+
* **External APIs:**

  * REST Countries API
  * Open Exchange Rates API

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Abraham-Franklin/HNG_13_Stage_Two.git
cd HNG_13_Stage_Two
```

### 2️⃣ Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in your project root and add:

```bash
DEBUG=True
SECRET_KEY=your_secret_key_here
```

(Don’t worry about database credentials — SQLite works by default.)

---

## 🧠 Run Locally

### Apply Migrations

```bash
python manage.py migrate
```

### Start the Server

```bash
python manage.py runserver
```

The API will be available at:

```
http://127.0.0.1:8000/
```

---

## 🧾 API Endpoints

### 🔄 Refresh and Cache Countries

**POST** `/countries/refresh/`
Fetches new data, updates the database, and regenerates the summary image.

### 🌍 List All Countries

**GET** `/countries/`
Supports filters and sorting:
`?region=Africa` | `?currency=NGN` | `?sort=gdp_desc`

### 🔎 Get Country by Name

**GET** `/countries/<name>/`

### ❌ Delete Country

**DELETE** `/countries/<name>/`

### 📊 Status Endpoint

**GET** `/status/`
Returns:

```json
{
  "total_countries": 250,
  "last_refreshed_at": "2025-10-22T18:00:00Z"
}
```

### 🖼️ Summary Image

**GET** `/countries/image/`
Returns a generated summary image located at `cache/summary.png`.

---

## 🧮 Request Logging

Every request (URL, method, headers, and body) is logged to:

```
core/request_logs.txt
```

This file is **ignored by Git** via `.gitignore`.

---

## 🌐 Deployment (PythonAnywhere)

1. Upload your project to PythonAnywhere.
2. Set up a **virtualenv** and install requirements:

   ```bash
   pip install -r requirements.txt
   ```
3. In **Web App settings**, set the WSGI path to your Django project’s `wsgi.py`.
4. Run migrations and collect static files:

   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```
5. Reload the web app — your API should be live 🎉

---

## 🧪 Example CURL Tests

### Refresh Countries

```bash
curl -X POST http://127.0.0.1:8000/countries/refresh/
```

### Get All Countries

```bash
curl -X GET http://127.0.0.1:8000/countries/
```

### Get Country by Name

```bash
curl -X GET http://127.0.0.1:8000/countries/Nigeria/
```

### Delete Country

```bash
curl -X DELETE http://127.0.0.1:8000/countries/Ghana/
```

### Get Status

```bash
curl -X GET http://127.0.0.1:8000/status/
```

### Get Summary Image

```bash
curl -X GET http://127.0.0.1:8000/countries/image/
```

---

## 🧑‍💻 Author

**Name:** Abraham Franklin Okumbor
**Email:** [okumborfranklin@gmail.com](mailto:okumborfranklin@gmail.com)
**Stack:** Python (Django REST Framework)

---

## 🏁 License

This project is licensed under the MIT License — you’re free to use, modify, and distribute it with attribution.

---

### 🌟 Acknowledgements

* [HNG Internship 13](https://hng.tech/)
* [REST Countries API](https://restcountries.com/)
* [Open Exchange Rate API](https://open.er-api.com/)
* Django & DRF communities
