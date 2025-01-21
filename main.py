import streamlit as st
import requests
from typing import List
import json
import download_data
class Course:
    def __init__(self, 科號: str, 課程中文名稱: str, 課程英文名稱: str, 學分數: str, 人限: str,
                 新生保留人數: str, 通識對象: str, 通識類別: str, 授課語言: str, 備註: str,
                 停開註記: str, 教室與上課時間: str, 授課教師: str, 擋修說明: str, 課程限制說明: str,
                 第一二專長對應: str, 學分學程對應: str, 不可加簽說明: str, 必選修說明: str):
        self.id = 科號
        self.chinese_title = 課程中文名稱
        self.english_title = 課程英文名稱
        self.credit = 學分數
        self.size_limit = 人限
        self.freshman_reservation = 新生保留人數
        self.object = 通識對象
        self.ge_type = 通識類別
        self.language = 授課語言
        self.note = 備註
        self.suspend = 停開註記
        self.class_room_and_time = 教室與上課時間
        self.teacher = 授課教師
        self.prerequisite = 擋修說明
        self.limit_note = 課程限制說明
        self.expertise = 第一二專長對應
        self.program = 學分學程對應
        self.no_extra_selection = 不可加簽說明
        self.required_optional_note = 必選修說明

@st.cache_data(ttl=24*60*60)  # Cache for 24 hours
def load_course_data():
    try:
        with open("course_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Course(**course) for course in data]
    except FileNotFoundError:
        st.warning("找不到課程資料，請先下載")
        if download_data.download_course_data():
            with open("course_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Course(**course) for course in data]
        return []

courses = load_course_data()

st.title("NTHU Course Explorer")

st.markdown("""
<style>
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .card:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    }
    .card h3 {
        margin: 0;
        color: #0073e6;
        font-size: 18px;
    }
    .divider {
        margin: 15px 0;
        border-top: 1px solid #ddd;
    }
    .expander-content {
        background-color: #f1f1f1;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 8px;
    }
    .ge-tag {
        background-color: #0073e6;
        color: white;
        padding: 3px 8px;
        border-radius: 5px;
        font-size: 12px;
        font-weight: bold;
        margin-right: 5px;
    }
    .empty {
            }
</style>
""", unsafe_allow_html=True)

st.sidebar.header("篩選條件")
filter_options = st.sidebar.multiselect(
    "篩選條件:", 
    ["課程代號", "課名", "時間", "教師名稱"],
    default=["課名", "時間"],
    placeholder="選擇篩選條件"
)
additional_enrollment = st.sidebar.checkbox("允許加簽")
show_all = st.sidebar.checkbox("顯示所有課程", value=False)

filtered_courses: List[Course] = courses
additional_filter = False

if "課程代號" in filter_options:
    course_id = st.sidebar.text_input("輸入課程代號:", placeholder="如: 11220CS, CS, GE, PE...")
    if course_id:
        filtered_courses = [course for course in filtered_courses if course_id in course.id]
        if course_id in ["GE", "GEC"]:
            additional_filter = True

if additional_filter:
    additional_filter_values = st.sidebar.multiselect("選擇額外篩選條件:", ["人文學", "自然", "社會", "向度1", "向度2", "向度3", "向度4"])
    if additional_filter_values:
        filtered_courses = [course for course in filtered_courses if any(value in course.ge_type or value[-1] in course.ge_type for value in additional_filter_values)]

if "課名" in filter_options:
    chinese_title = st.sidebar.text_input("輸入課名 (中文)", placeholder="如: 資料結構")
    if chinese_title:
        filtered_courses = [course for course in filtered_courses if chinese_title in course.chinese_title]
        
if "時間" in filter_options:
    time_input = st.sidebar.text_input("輸入時間:", placeholder="如: M1M2M3, R6R7").strip()
    if time_input:
        time_slots = [t.strip().upper() for t in time_input.replace(",", " ").split()]
        filtered_courses = [
            course for course in filtered_courses 
            if any(time in course.class_room_and_time.upper() for time in time_slots)
        ]

if "教師名稱" in filter_options:
    teacher = st.sidebar.text_input("輸入教師名稱:", placeholder="如: 姜諧潾")
    if teacher:
        filtered_courses = [course for course in filtered_courses if teacher in course.teacher]

if additional_enrollment:
    filtered_courses = [course for course in filtered_courses if course.no_extra_selection == ""]

if not show_all:
    num_courses_to_show = st.sidebar.slider("顯示數量:", 1, len(filtered_courses), 10)
else:
    num_courses_to_show = len(filtered_courses)


if num_courses_to_show == 0 or not filtered_courses:
    st.error("沒有符合篩選條件的課程，請嘗試更換篩選條件")
else:
    for course in filtered_courses[:num_courses_to_show]:
        with st.container():
            ge_tag = f"<span class='ge-tag'>{course.ge_type}</span>" if course.ge_type else f"<span class='empty'></span>"
            st.markdown(
                f"""
                <div class='card'>
                    <h3>{course.chinese_title} ({course.english_title})</h3>
                    <div>
                        {ge_tag}
                        <strong>課程代號:</strong> {course.id} | <strong>學分:</strong> {course.credit} | <strong>教師:</strong> {course.teacher.split()[0]}
                    </div>
                    <strong>教室與時間:</strong> {" | ".join(course.class_room_and_time.split())}
                """,
                unsafe_allow_html=True
            )
            # Expander for detailed information
            with st.expander("查看詳細資訊"):
                st.markdown(f"<div class='expander-content'><strong>備註:</strong> {course.note or '無'}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='expander-content'><strong>先修課程:</strong> {course.prerequisite or '無'}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='expander-content'><strong>選課限制:</strong> {course.limit_note or '無'}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='expander-content'><strong>專長:</strong> {course.expertise or '無'}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='expander-content'><strong>開課系所:</strong> {course.program or '無'}</div>", unsafe_allow_html=True)
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
