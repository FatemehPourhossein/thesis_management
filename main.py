from student import Student
from teacher import Teacher

def main():
    while True:
        print("\nسیستم مدیریت پایان نامه")
        print("1) ورود دانشجو")
        print("2) ثبت نام دانشجو")
        print("3) ورود استاد")
        print("0) خروج")
        c = input("انتخاب: ")

        if c == "1":
            stu = Student.login()
            if stu:
                while True:
                    print("\n____منوی دانشجو____")
                    print("1) لیست دروس")
                    print("2) درخواست پایان نامه")
                    print("3) وضعیت درخواست ها")
                    print("4) ارسال مجدد")
                    print("5) درخواست دفاع")
                    print("0) بازگشت")
                    cc = input("انتخاب: ")
                    if cc=="1": stu.list_courses()
                    elif cc=="2": stu.request_thesis()
                    elif cc=="3": stu.view_requests()
                    elif cc=="4": stu.resubmit_request()
                    elif cc=="5": stu.request_defense()
                    elif cc=="0": break

        elif c == "2":
            Student.register()

        elif c == "3":
            tea = Teacher.login()
            if tea:
                while True:
                    print("\n____منوی استاد____")
                    print("1) بررسی درخواست ها")
                    print("2) مدیریت دفاع")
                    print("3) ثبت نمره داوری")
                    print("0) بازگشت")
                    cc = input("انتخاب: ")
                    if cc=="1": tea.check_requests()
                    elif cc=="2": tea.manage_defense()
                    elif cc=="3": tea.judge_score()
                    elif cc=="0": break

        elif c=="0":
            break

if __name__=="__main__":
    main()
