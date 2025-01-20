import streamlit as st
import requests
import re
from typing import List

class Course:
    def __init__(self, id: str, chinese_title: str, english_title: str, credit: str, size_limit: str, freshman_reservation: str, object: str, ge_type: str, language: str, note: str, suspend: str, class_room_and_time: str, teacher: str, prerequisite: str, limit_note: str, expertise: str, program: str, no_extra_selection: str, required_optional_note: str):
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

    def __repr__(self) -> str:
        return f"Course({self.id}, {self.chinese_title}, {self.english_title}, {self.credit}, {self.size_limit}, {self.freshman_reservation}, {self.object}, {self.ge_type}, {self.language}, {self.note}, {self.suspend}, {self.class_room_and_time}, {self.teacher}, {self.prerequisite}, {self.limit_note}, {self.expertise}, {self.program}, {self.no_extra_selection}, {self.required_optional_note})"

url: str = 'https://api.nthusa.tw/courses'
response: requests.Response = requests.get(url)
courses_data: List[dict] = response.json()
courses: List[Course] = [Course(**course) for course in courses_data]

st.title("NTHU Course Explorer")

# Inject custom CSS to reduce space between lines
st.markdown("""
    <style>
    .small-font {
        font-size: 12px;
        line-height: 1.8;
        margin: 0;
        padding: 0;
    }
    .small-font hr {
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)

filter_options: List[str] = st.multiselect("篩選條件:", ["課程代號", "課名", "時間"])

additional_enrollment = st.checkbox("是否可以加簽")
filtered_courses: List[Course] = courses

if "課程代號" in filter_options:
    course_id: str = st.text_input("輸入課程代號: (如: 11220CS, CS, GE, PE...)")
    if course_id:
        filtered_courses = [course for course in filtered_courses if course_id in course.id]

if "課名" in filter_options:
    chinese_title: str = st.text_input("輸入課名 (中文)")
    if chinese_title:
        filtered_courses = [course for course in filtered_courses if chinese_title in course.chinese_title]

if "時間" in filter_options:
    time: str = st.text_input("輸入時間 (如: M1M2M3)")
    if time:
        filtered_courses = [course for course in filtered_courses if time in course.class_room_and_time]
if additional_enrollment:
    filtered_courses = [course for course in filtered_courses if course.no_extra_selection == ""]
num_courses_to_show: int = st.number_input("顯示數量:", min_value=0, max_value=len(filtered_courses), value=min(10, len(filtered_courses)))


st.write(f"顯示 {num_courses_to_show}/{len(filtered_courses)} 門課程")

for course in filtered_courses[:num_courses_to_show]:
    room_and_time: List[str] = course.class_room_and_time.split()
    st.markdown(f"<p class='small-font'>{course.id}: {course.chinese_title}</p>", unsafe_allow_html=True)
    if room_and_time:
        st.markdown(f"<p class='small-font'>{' '.join(room_and_time[:-1])}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='small-font'>{room_and_time[-1]}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='small-font'>{course.teacher.split()[0]}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='small-font'>{course.credit}學分</p>", unsafe_allow_html=True)
    st.markdown("<hr class='small-font'>", unsafe_allow_html=True)
