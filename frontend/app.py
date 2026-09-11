import os
import requests
import gradio as gr


# ==========================================
# CONFIGURATION
# ==========================================

API_URL = os.getenv(
    "API_URL",
    "https://student-management-api-hv43.onrender.com"
).rstrip("/")


# ==========================================
# HELPER
# ==========================================

def handle_response(response):
    try:
        return response.json()
    except Exception:
        return {
            "message": response.text
        }


# ==========================================
# CREATE STUDENT
# ==========================================

def create_student(name, course, marks):

    if not name or not name.strip():
        return "Please enter student name.", None

    if not course or not course.strip():
        return "Please enter course.", None

    try:
        response = requests.post(
            f"{API_URL}/students",
            params={
                "name": name.strip(),
                "course": course.strip(),
                "marks": int(marks or 0)
            },
            timeout=30
        )

        data = handle_response(response)

        if response.ok:
            return (
                data.get(
                    "message",
                    "Student created successfully"
                ),
                data.get("data")
            )

        return (
            f"Error: {response.status_code}",
            data
        )

    except requests.exceptions.ConnectionError:
        return "Could not connect to FastAPI backend.", None

    except requests.exceptions.Timeout:
        return "Backend request timed out.", None

    except Exception as e:
        return f"Error: {str(e)}", None


# ==========================================
# GET ALL STUDENTS
# ==========================================

def get_students_table():

    try:
        response = requests.get(
            f"{API_URL}/students",
            timeout=30
        )

        data = handle_response(response)

        if not response.ok:
            return [[
                f"Error: {response.status_code}",
                "",
                "",
                ""
            ]]

        students = data.get("data", [])

        return [
            [
                student.get("id"),
                student.get("name"),
                student.get("course"),
                student.get("marks")
            ]
            for student in students
        ]

    except requests.exceptions.ConnectionError:
        return [[
            "Could not connect to backend.",
            "",
            "",
            ""
        ]]

    except requests.exceptions.Timeout:
        return [[
            "Backend request timed out.",
            "",
            "",
            ""
        ]]

    except Exception as e:
        return [[
            str(e),
            "",
            "",
            ""
        ]]


# ==========================================
# GET STUDENT
# ==========================================

def get_student(student_id):

    if student_id is None:
        return {
            "message": "Please enter student ID."
        }

    try:
        response = requests.get(
            f"{API_URL}/students/{int(student_id)}",
            timeout=30
        )

        data = handle_response(response)

        if response.ok:
            return data

        return {
            "message": f"Error: {response.status_code}",
            "data": data
        }

    except requests.exceptions.ConnectionError:
        return {
            "message": "Could not connect to FastAPI backend."
        }

    except requests.exceptions.Timeout:
        return {
            "message": "Backend request timed out."
        }

    except Exception as e:
        return {
            "message": f"Error: {str(e)}"
        }


# ==========================================
# UPDATE STUDENT
# ==========================================

def update_student(
    student_id,
    name,
    course,
    marks
):

    if student_id is None:
        return "Please enter student ID.", None

    if not name or not name.strip():
        return "Please enter student name.", None

    if not course or not course.strip():
        return "Please enter course.", None

    try:
        response = requests.put(
            f"{API_URL}/students/{int(student_id)}",
            params={
                "name": name.strip(),
                "course": course.strip(),
                "marks": int(marks or 0)
            },
            timeout=30
        )

        data = handle_response(response)

        if response.ok:
            return (
                data.get(
                    "message",
                    "Student updated successfully"
                ),
                data.get("data")
            )

        return (
            f"Error: {response.status_code}",
            data
        )

    except requests.exceptions.ConnectionError:
        return "Could not connect to FastAPI backend.", None

    except requests.exceptions.Timeout:
        return "Backend request timed out.", None

    except Exception as e:
        return f"Error: {str(e)}", None


# ==========================================
# DELETE STUDENT
# ==========================================

def delete_student(student_id):

    if student_id is None:
        return "Please enter student ID.", None

    try:
        response = requests.delete(
            f"{API_URL}/students/{int(student_id)}",
            timeout=30
        )

        data = handle_response(response)

        if response.ok:
            return (
                data.get(
                    "message",
                    "Student deleted successfully"
                ),
                data.get("data")
            )

        return (
            f"Error: {response.status_code}",
            data
        )

    except requests.exceptions.ConnectionError:
        return "Could not connect to FastAPI backend.", None

    except requests.exceptions.Timeout:
        return "Backend request timed out.", None

    except Exception as e:
        return f"Error: {str(e)}", None


# ==========================================
# GRADIO UI
# ==========================================

with gr.Blocks(
    title="Student Management System"
) as demo:

    gr.Markdown(
        """
        # 🎓 Student Management System

        Manage student records using **Gradio + FastAPI + Supabase**.
        """
    )

    # ======================================
    # CREATE
    # ======================================

    with gr.Tab("➕ Create Student"):

        gr.Markdown("### Add New Student")

        create_name = gr.Textbox(
            label="Student Name",
            placeholder="Enter student name"
        )

        create_course = gr.Textbox(
            label="Course",
            placeholder="Enter course"
        )

        create_marks = gr.Number(
            label="Marks",
            precision=0,
            value=0
        )

        create_button = gr.Button(
            "Create Student",
            variant="primary"
        )

        create_message = gr.Textbox(
            label="Message"
        )

        create_result = gr.JSON(
            label="Student Data"
        )

        create_button.click(
            fn=create_student,
            inputs=[
                create_name,
                create_course,
                create_marks
            ],
            outputs=[
                create_message,
                create_result
            ]
        )

    # ======================================
    # ALL STUDENTS
    # ======================================

    with gr.Tab("📋 All Students"):

        gr.Markdown("### All Students")

        refresh_button = gr.Button(
            "🔄 Refresh Students"
        )

        students_table = gr.Dataframe(
            headers=[
                "id",
                "name",
                "course",
                "marks"
            ],
            datatype=[
                "number",
                "str",
                "str",
                "number"
            ],
            label="Students",
            interactive=False
        )

        refresh_button.click(
            fn=get_students_table,
            outputs=students_table
        )

    # ======================================
    # FIND
    # ======================================

    with gr.Tab("🔍 Find Student"):

        gr.Markdown("### Find Student By ID")

        find_id = gr.Number(
            label="Student ID",
            precision=0
        )

        find_button = gr.Button(
            "Find Student",
            variant="primary"
        )

        find_result = gr.JSON(
            label="Student"
        )

        find_button.click(
            fn=get_student,
            inputs=find_id,
            outputs=find_result
        )

    # ======================================
    # UPDATE
    # ======================================

    with gr.Tab("✏️ Update Student"):

        gr.Markdown("### Update Student")

        update_id = gr.Number(
            label="Student ID",
            precision=0
        )

        update_name = gr.Textbox(
            label="Student Name"
        )

        update_course = gr.Textbox(
            label="Course"
        )

        update_marks = gr.Number(
            label="Marks",
            precision=0
        )

        update_button = gr.Button(
            "Update Student",
            variant="primary"
        )

        update_message = gr.Textbox(
            label="Message"
        )

        update_result = gr.JSON(
            label="Updated Student"
        )

        update_button.click(
            fn=update_student,
            inputs=[
                update_id,
                update_name,
                update_course,
                update_marks
            ],
            outputs=[
                update_message,
                update_result
            ]
        )

    # ======================================
    # DELETE
    # ======================================

    with gr.Tab("🗑️ Delete Student"):

        gr.Markdown("### Delete Student")

        delete_id = gr.Number(
            label="Student ID",
            precision=0
        )

        delete_button = gr.Button(
            "Delete Student",
            variant="stop"
        )

        delete_message = gr.Textbox(
            label="Message"
        )

        delete_result = gr.JSON(
            label="Deleted Student"
        )

        delete_button.click(
            fn=delete_student,
            inputs=delete_id,
            outputs=[
                delete_message,
                delete_result
            ]
        )


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 7860)
    )

    demo.launch(
        server_name="0.0.0.0",
        server_port=port
    )

