## 🎓 Student Management System

A Student Management System built with Gradio + FastAPI + Supabase.

## 🌐 Live Demo
Frontend: https://student-management-system-1-g1ah.onrender.com

Backend API: https://student-management-api-hv43.onrender.com

## 🚀 Features

Create student
View all students
Find student by ID
Update student
Delete student

## 🛠️ Tech Stack

Python
Gradio
FastAPI
Supabase
Render

## 📁 Project Structure

student-management/

├── backend/
│   ├── main.py
│   └── requirements.txt

├── frontend/
│   ├── app.py
│   └── requirements.txt

└── README.md

## ⚙️ Environment Variables

Backend
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

Frontend
API_URL=https://your-backend.onrender.com

☁️ Render Deployment
Backend

Root Directory

backend


Build Command

pip install -r requirements.txt


Start Command

uvicorn main:app --host 0.0.0.0 --port $PORT

Frontend

Root Directory

frontend


Build Command

pip install -r requirements.txt


Start Command

python app.py

🔄 GitHub Update
git add .
git commit -m "Update project"
git push origin main

🔐 Security

Do not upload .env or Supabase credentials to GitHub.
