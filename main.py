import streamlit as st
import requests
from typing import List

class Course:
    def __init__(self, id: str, chinese_title: str, english_title: str, credit: str, size_limit: str, 
                 freshman_reservation: str, object: str, ge_type: str, language: str, note: str, 
                 suspend: str, class_room_and_time: str, teacher: str, prerequisite: str, limit_note: str, 
                 expertise: str, program: str, no_extra_selection: str, required_optional_note: str):
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

url: str = 'https://api.nthusa.tw/courses'
response: requests.Response = requests.get(url)
courses_data: List[dict] = response.json()
courses: List[Course] = [Course(**course) for course in courses_data]

st.title("NTHU Course Explorer")

# Inject custom CSS for styling
st.markdown("""
<style>
    .card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
    }
    .card h3 {
        margin: 0;
        color: #0073e6;
        font-size: 16px
    }
    .divider {
        margin: 10px 0;
        border-top: 1px solid #ddd;
    }
    .expander-content {
        background-color: #f1f1f1;
        padding: 10px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Filters
filter_options: List[str] = st.multiselect("篩選條件:", ["課程代號", "課名", "時間"])
additional_enrollment = st.checkbox("是否可以加簽")

filtered_courses: List[Course] = courses

if "課程代號" in filter_options:
    course_id: str = st.text_input("輸入課程代號:", placeholder="如: 11220CS, CS, GE, PE...")
    if course_id:
        filtered_courses = [course for course in filtered_courses if course_id in course.id]

if "課名" in filter_options:
    chinese_title: str = st.text_input("輸入課名 (中文)", placeholder="如: 資料結構")
    if chinese_title:
        filtered_courses = [course for course in filtered_courses if chinese_title in course.chinese_title]

if "時間" in filter_options:
    time: str = st.text_input("輸入時間:", placeholder="如: M1M2M3")
    if time:
        filtered_courses = [course for course in filtered_courses if time in course.class_room_and_time]

if additional_enrollment:
    filtered_courses = [course for course in filtered_courses if course.no_extra_selection == ""]

# Display filtered courses
num_courses_to_show: int = st.number_input("顯示數量:", min_value=1, max_value=len(filtered_courses), value=min(10, len(filtered_courses)))
st.write(f"顯示 {num_courses_to_show}/{len(filtered_courses)} 門課程")

for course in filtered_courses[:num_courses_to_show]:
    with st.container():
        # Header information
        st.markdown(f"<div class='card'><h3>{course.chinese_title} ({course.english_title})</h3>", unsafe_allow_html=True)
        st.markdown(f"<strong>課程代號:</strong> {course.id} | <strong>學分:</strong> {course.credit} | <strong>教師:</strong> {course.teacher.split()[0]}", unsafe_allow_html=True)
        st.markdown(f"<strong>教室與時間:</strong> {course.class_room_and_time}", unsafe_allow_html=True)
        
        with st.expander("查看詳細資訊"):
            st.markdown(f"<div class='expander-content'><strong>備註:</strong> {course.note or '無'}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='expander-content'><strong>先修課程:</strong> {course.prerequisite or '無'}</div>", unsafe_allow_html=True)
        
        st.markdown("</div><div class='divider'></div>", unsafe_allow_html=True)
