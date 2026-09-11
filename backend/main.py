from fastapi import FastAPI, HTTPException
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Student Management API",
    description="Student Management System API",
    version="1.0.0"
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY is missing")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


@app.get("/")
def root():
    return {
        "message": "Student Management API is running"
    }


@app.post("/students")
def create_student(
    name: str,
    course: str,
    marks: int
):
    if not name.strip():
        raise HTTPException(400, "Name is required")

    if not course.strip():
        raise HTTPException(400, "Course is required")

    if marks < 0 or marks > 100:
        raise HTTPException(400, "Marks must be between 0 and 100")

    response = (
        supabase
        .table("students")
        .insert({
            "name": name.strip(),
            "course": course.strip(),
            "marks": marks
        })
        .execute()
    )

    return {
        "message": "Student created successfully",
        "data": response.data
    }


@app.get("/students")
def get_students():
    response = (
        supabase
        .table("students")
        .select("*")
        .execute()
    )

    return {
        "message": "Students fetched successfully",
        "data": response.data
    }


@app.get("/students/{student_id}")
def get_student(student_id: int):
    response = (
        supabase
        .table("students")
        .select("*")
        .eq("id", student_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(404, "Student not found")

    return {
        "message": "Student fetched successfully",
        "data": response.data[0]
    }


@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    name: str,
    course: str,
    marks: int
):
    if not name.strip():
        raise HTTPException(400, "Name is required")

    if not course.strip():
        raise HTTPException(400, "Course is required")

    if marks < 0 or marks > 100:
        raise HTTPException(400, "Marks must be between 0 and 100")

    response = (
        supabase
        .table("students")
        .update({
            "name": name.strip(),
            "course": course.strip(),
            "marks": marks
        })
        .eq("id", student_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(404, "Student not found")

    return {
        "message": "Student updated successfully",
        "data": response.data
    }


@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    check_response = (
        supabase
        .table("students")
        .select("*")
        .eq("id", student_id)
        .execute()
    )

    if not check_response.data:
        raise HTTPException(404, "Student not found")

    response = (
        supabase
        .table("students")
        .delete()
        .eq("id", student_id)
        .execute()
    )

    return {
        "message": "Student deleted successfully",
        "data": check_response.data
    }
