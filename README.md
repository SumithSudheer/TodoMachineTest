# User Management System (Machine Test)

A **User Management System** built with **Django REST Framework (backend)** and a **minimal JavaScript frontend**.  
The application demonstrates **authentication**, **profile management**, and **CRUD operations** for tasks/notes.

---

## 🌐 Live Demo

- **Backend (Django API):** `https://07465ff631b9.ngrok-free.app`  
- **Frontend (JS App):** `https://5949a4030571.ngrok-free.app/`  
- **API Docs (Swagger / DRF Browsable API):** `https://07465ff631b9.ngrok-free.app/api/docs/`

---

## 🛠 Features

### 1. Authentication
- User Registration (username, email, password)
- Login & Logout (JWT Token)
- Authenticated endpoints for profile & CRUD

### 2. Profile Management
- View profile
- Update profile
- Reset password

Profile fields:
- Full name
- Date of birth
- Email
- Address
- Gender
- Mobile number

### 3. CRUD Module (Tasks / Notes)
- Create, List, Update, Delete tasks
- Fields: title, description, attachment, created_at, modified_at
- Only accessible by logged-in user

### 4. Frontend
- Minimal HTML + JS + jQuery
- Register/Login
- View/update profile
- CRUD operations for tasks/notes

---

## 💻 Setup Instructions


```bash
git https://github.com/SumithSudheer/TodoMachineTest.git
docker compose up --build
```
