from src.database.config import supabase
import bcrypt

def hash_password(password):
    # Hash the password using bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))



def check_teacher_exists(username):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    return len(response.data) > 0



def create_teacher(username,password,name):
    data ={
        "username": username,
        "password": hash_password(password),
        "name": name
    }
    response = supabase.table("teachers").insert(data).execute()
    return response.data



def teacher_login(username,password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_password(password, teacher["password"]):
            return teacher
    return None


def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data

def create_student(name, face_embeddings=None, voice_embeddings=None):
    data = {
        "name": name,
        "face_embeddings": face_embeddings,
        "voice_embeddings": voice_embeddings
    }
    response = supabase.table("students").insert(data).execute()
    return response.data




# subjects:-

def create_subject(subject_code, subject_name, subject_section, teacher_id):
    data = {
        "subject_code": subject_code,
        "name": subject_name,
        "section": subject_section,
        "teacher_id": teacher_id
    }
    response = supabase.table("subjects").insert(data).execute()
    return response.data


def get_teacher_subjects(teacher_id):
    response = supabase.table("subjects").select("*,subject_students(count),attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data
    for sub in subjects:
        sub['total_students'] = sub.get('subject_students', [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', []) 
        unique_sessions = len(set(log['timestamp'] for log in attendance if log and "timestamp" in log))
        sub['total_class'] = unique_sessions
        
        sub.pop('subject_students', None)
        sub.pop('attendance_logs', None)
    return subjects

def enroll_student_to_subject(student_id, subject_id):
    data = {
        "student_id": student_id,
        "subject_id": subject_id
    }
    response = supabase.table("subject_students").insert(data).execute()
    return response.data

def unenroll_student_from_subject(student_id, subject_id):
    response = supabase.table("subject_students").delete().eq("student_id", student_id).eq("subject_id", subject_id).execute()
    return response.data



def get_student_attendance_logs(student_id):
    response = supabase.table("attendance_logs").select("*, subjects(*)").eq("student_id", student_id).execute()
    return response.data

def get_student_subjects(student_id):
    response = supabase.table("subject_students").select("*, subjects(*)").eq("student_id", student_id).execute()
    return response.data


def create_attendance_logs(logs):
    response = supabase.table("attendance_logs").insert(logs).execute()
    return response.data

def get_teacher_attendance_logs(teacher_id):
    response = supabase.table("attendance_logs").select("*, subjects!inner(*)").eq("subjects.teacher_id", teacher_id).execute()
    return response.data