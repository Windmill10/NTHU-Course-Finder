import copy
import re
from bs4 import BeautifulSoup


class Course:
    def __init__(self, course_id, name, time, instructor, description):
        self.course_id = course_id
        self.name = name
        self.time = time
        self.instructor = instructor
        self.description = description

    def __repr__(self):
        print(self.course_id, self.name, self.time, self.instructor, self.description)


l = temp = []

with open("CSdept.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")
    elements = soup.find_all("td", {"class": "word"})
    #elements[0].
    for i, element in enumerate(elements):
        text = element.text.strip()
        temp.append(text)
        #print(text)
        if text.find("11220CS") == 0 and len(temp) > 5:
            #print(text, text.find("112"))
            print(temp)
            l.append(Course(temp[0], temp[1], temp[2], temp[3], temp[4]))
            #print(temp[0], temp[1], temp[2], temp[3], temp[4])
            #l.append(temp)
            temp = []
            temp.append(text)

        #print(f"[{i+1}] {element.text.strip()}")
    print(l[0])
    #for course in l:
        #print(str(course))