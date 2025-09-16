from storage import load_json, save_json
from datetime import datetime
import hashlib

TEACHERS_FILE = "data/teachers.json"
THESIS_FILE = "data/thesis.json"
DEFENDED_FILE = "data/defended_thesis.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class Teacher:
    def __init__(self, code, name, password, email="", cap_sup=5, cap_judge=10):
        self.code = code
        self.name = name
        self.password = password
        self.email = email
        self.cap_sup = cap_sup
        self.cap_judge = cap_judge

    @classmethod
    def login(cls):
        teachers = load_json(TEACHERS_FILE)
        code = input("کد استادی: ")
        pwd = input("رمز عبور: ")
        hashed = hash_password(pwd)
        for t in teachers:
            if t["teacher_code"] == code and t["password"] == hashed:
                print("خوش آمدید استاد", t["name"])
                return cls(t["teacher_code"], t["name"], t["password"], t.get("email",""),
                           t.get("capacity_supervise",5), t.get("capacity_judge",10))
        print("کد یا رمز اشتباه است")
        return None

    #بررسی درخواست‌های پایان نامه
    
    def check_requests(self):
        thesis = load_json(THESIS_FILE)
        myreqs = [t for t in thesis if self.code in t.get("course_ID","")] 
        if not myreqs:
            print("درخواستی نداری")
            return

        for r in myreqs:
            print("دانشجو:", r["student_code"], "درس:", r["course_ID"], "وضعیت:", r["status"])

        cid = input("کد درس برای تایید/رد: ")
        stcode = input("کد دانشجو: ")
        action = input("تایید یا رد؟ (a/r): ")

        for r in thesis:
            if r["student_code"]==stcode and r["course_ID"]==cid and r["status"]=="pending":
                if action=="a":
                    r["status"] = "approved"
                    r["approval_date"] = datetime.now().isoformat()
                    print("درخواست تایید شد")
                else:
                    r["status"] = "rejected"
                    print("درخواست رد شد")
                save_json(THESIS_FILE, thesis)
                return

    #مدیریت درخواست دفاع
    
    def manage_defense(self):
        thesis = load_json(THESIS_FILE)
        pending_def = [t for t in thesis if t["status"]=="defense_pending"]
        if not pending_def:
            print("درخواست دفاعی وجود ندارد")
            return
        for r in pending_def:
            print("دانشجو:", r["student_code"], "درس:", r["course_ID"])

        stcode = input("کد دانشجو: ")
        cid = input("کد درس: ")
        date = input("تاریخ دفاع (مثلا 1404-03-10): ")
        judges = input("کد داوران (با , جدا کن): ").split(",")

        for r in thesis:
            if r["student_code"]==stcode and r["course_ID"]==cid and r["status"]=="defense_pending":
                r["status"] = "defense"
                r["defense_date"] = date
                r["judges"] = judges
                save_json(THESIS_FILE, thesis)
                print("جلسه دفاع ثبت شد")
                return

    #ثبت نمره داور
    
    def judge_score(self):
        thesis = load_json(THESIS_FILE)
        defense = [t for t in thesis if t["status"]=="defense"]
        if not defense:
            print("پایان نامه‌ای برای داوری نداری")
            return
        for r in defense:
            print("دانشجو:", r["student_code"], "درس:", r["course_ID"], "تاریخ:", r.get("defense_date","-"))

        stcode = input("کد دانشجو: ")
        cid = input("کد درس: ")
        score = int(input("نمره بده (0 تا 20): "))

        for r in thesis:
            if r["student_code"]==stcode and r["course_ID"]==cid and r["status"]=="defense":
                r["status"] = "done"
                r["score"] = score

                # انتقال به defended_thesis.json
                
                defended = load_json(DEFENDED_FILE)
                defended.append({
                    "student_code": stcode,
                    "course_ID": cid,
                    "score": score,
                    "judges": r.get("judges", []),
                    "supervisor": self.name,
                    "year": datetime.now().year,
                    "semester": "اول",
                    "files": r.get("files", {})
                })
                save_json(DEFENDED_FILE, defended)

                save_json(THESIS_FILE, thesis)
                print("نمره ثبت شد و پایان نامه مختومه شد.")
                return
