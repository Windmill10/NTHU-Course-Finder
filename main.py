import requests
import streamlit as st
class Course:
    def __init__(self, id, chinese_title, english_title, credit, size_limit, freshman_reservation, object, ge_type, language, note, suspend, class_room_and_time, teacher, prerequisite, limit_note, expertise, program, no_extra_selection, required_optional_note):
        self.id = id
        self.chinese_title = chinese_title
        self.english_title = english_title
        self.credit = credit
        self.size_limit = size_limit
        self.freshman_reservation = freshman_reservation
        self.object = object
        self.ge_type = ge_type
        self.language = language
        self.note = note
        self.suspend = suspend
        self.class_room_and_time = class_room_and_time
        self.teacher = teacher
        self.prerequisite = prerequisite
        self.limit_note = limit_note
        self.expertise = expertise
        self.program = program
        self.no_extra_selection = no_extra_selection
        self.required_optional_note = required_optional_note

    def __repr__(self):
        return f"Course({self.id}, {self.chinese_title}, {self.english_title}, {self.credit}, {self.size_limit}, {self.freshman_reservation}, {self.object}, {self.ge_type}, {self.language}, {self.note}, {self.suspend}, {self.class_room_and_time}, {self.teacher}, {self.prerequisite}, {self.limit_note}, {self.expertise}, {self.program}, {self.no_extra_selection}, {self.required_optional_note})"

url = 'https://api.nthusa.tw/courses'
response = requests.get(url)
courses_data = response.json()
courses = [Course(**course) for course in courses_data]

st.title("NTHU Course Filter")
filter_option = st.selectbox("Select filter option:", ["Course ID", "Chinese Title", "Time"])
if filter_option == "Course ID":
    course_id = st.text_input("Enter Course ID:")
    filtered_courses = [course for course in courses if course_id in course.id]
if filter_option == "Chinese Title":
    chinese_title = st.text_input("Enter Chinese Title:")
    filtered_courses = [course for course in courses if chinese_title in course.chinese_title]
if filter_option == "Time":
    time = st.text_input("Enter Time:")
    filtered_courses = [course for course in courses if time in course.class_room_and_time]

st.write(f"Found {len(filtered_courses)} courses")

for course in filtered_courses:
    st.write(course)


# import requests
# from bs4 import BeautifulSoup

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
# }

# r = requests.get("https://www.ccxp.nthu.edu.tw/ccxp/COURSE/JH/7/7.6/7.6.1/JH761004.php?toChk=2&amp;ACIXSTORE=s5kh0k7c1r7uctrvgeg682s3g1"
#                     , headers=headers)
# r.encoding = r.apparent_encoding

# with open("result.html", "w") as file:
#     file.write(r.text)

# print(r.text)

# soup = BeautifulSoup(r.text, 'html.parser')
# #quote_elements = soup.find_all('div', id="overDiv")
# #print(quote_elements)
