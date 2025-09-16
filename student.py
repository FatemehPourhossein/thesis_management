from storage import load_json, save_json
from datetime import datetime
import hashlib

STUDENTS_FILE = "data/students.json"
COURSES_FILE = "data/courses.json"
THESIS_FILE = "data/thesis.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class Student:
    def __init__(self, code, name, password, email=""):
        self.code = code
        self.name = name
        self.password = password
        self.email = email

    @classmethod
    def register(cls):
        students = load_json(STUDENTS_FILE)
        code = input("کد دانشجویی جدید: ")

        # جلوگیری از تکراری بودن
        for s in students:
            if s["student_code"] == code:
                print("این کد قبلاً ثبت شده.")
                return None

        name = input("نام کامل: ")
        pwd = input("رمز عبور: ")
        email = input("ایمیل (اختیاری): ")

        hashed = hash_password(pwd)

        new_stu = {
            "name": name,
            "student_code": code,
            "password": hashed,
            "email": email
        }

        students.append(new_stu)
        save_json(STUDENTS_FILE, students)
        print("ثبت‌نام انجام شد.")
        return cls(code, name, hashed, email)

    @classmethod
    def login(cls):
        students = load_json(STUDENTS_FILE)
        code = input("کد دانشجویی: ")
        pwd = input("رمز عبور: ")
        hashed = hash_password(pwd)

        for s in students:
            if s["student_code"] == code and s["password"] == hashed:
                print("سلام", s["name"])
                return cls(s["student_code"], s["name"], s["password"], s.get("email",""))
        print("کد یا رمز اشتباه بود")
        return None

    def list_courses(self):
        courses = load_json(COURSES_FILE)
        print("لیست دروس:")
        for c in courses:
            print(c["course_ID"], "-", c["course_title"], "ظرفیت:", c["capacity"])

    def request_thesis(self):
        courses = load_json(COURSES_FILE)
        thesis = load_json(THESIS_FILE)
        cid = input("کد درس انتخابی: ")

        for c in courses:
            if c["course_ID"] == cid:
                if c["capacity"] <= 0:
                    print("ظرفیت پر است.")
                    return
                for t in thesis:
                    if t["student_code"] == self.code and t["course_ID"] == cid:
                        print("قبلا درخواست داده ای")
                        return
                req = {
                    "student_code": self.code,
                    "course_ID": cid,
                    "status": "pending",
                    "request_date": datetime.now().isoformat()
                }
                thesis.append(req)
                save_json(THESIS_FILE, thesis)
                print("درخواست ثبت شد.")
                return
        print("درس پیدا نشد")

    def view_requests(self):
        thesis = load_json(THESIS_FILE)
        mine = [t for t in thesis if t["student_code"] == self.code]
        if not mine:
            print("درخواستی نداری.")
            return
        for r in mine:
            print(r["course_ID"], "وضعیت:", r["status"])

    def resubmit_request(self):
        thesis = load_json(THESIS_FILE)
        rejected = [t for t in thesis if t["student_code"]==self.code and t["status"]=="rejected"]
        if not rejected:
            print("درخواست رد شده ای نداری")
            return
        cid = input("کد درسی که میخوای دوباره بدی: ")
        for r in thesis:
            if r["student_code"]==self.code and r["course_ID"]==cid:
                r["status"] = "pending"
                save_json(THESIS_FILE, thesis)
                print("دوباره ارسال شد")
                return
        print("چنین درخواستی پیدا نشد")

    def request_defense(self):
        thesis = load_json(THESIS_FILE)
        my = [t for t in thesis if t["student_code"]==self.code and t["status"]=="approved"]
        if not my:
            print("پایان نامه تایید شده نداری")
            return
        t = my[0]
        approved_at = datetime.fromisoformat(t.get("approval_date", datetime.now().isoformat()))
        days = (datetime.now() - approved_at).days
        if days < 90:
            ch = input(f"هنوز {days} روز گذشته. ادامه بدم؟ (y/n): ")
            if ch.lower() != "y":
                return
        t["status"] = "defense_pending"
        t["defense_date"] = datetime.now().isoformat()
        save_json(THESIS_FILE, thesis)
        print("درخواست دفاع ثبت شد.")
