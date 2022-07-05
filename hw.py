#!/usr/bin/env python
# coding: utf-8

# In[1]:


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
    
    def __str__(self):  #
        middle = self.middle_grade_stud()  # использует метод от self
        act_courses = [i for i in self.act_courses]
        finished = self.finished
        return f'Имя: {self.name}\nФамилия: {self.surname}\n'                f'Средняя оценка за домашние задания: {middle}\n'                f'Курсы в процессе обучения: {", ".join([str(x) for x in [*act_courses]])}\n'                f'Завершенные курсы:  '                f'{", ".join([str(x) for x in [*finished]])}'
    
    def middle_grade_stud(self):  # Исправил порядок расчета средней т.к. в предыдущей версии путой список считался бы как за 0
        middle = sum([sum(i) for i in list(self.act_courses.values())]) +                  sum([sum(i) for i in list(self.finished.values())])
        m2 = []
        [[m2.append(i) for i in b] for b in self.act_courses.values()]
        if len(m2) != 0:
            return middle / len(m2)
        else:
            return f'У студента {self.name} нет оценок'
    
    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return 'Плохой кандидат для сравнения'
        if isinstance(self.middle_grade_stud(), float) and isinstance(other.middle_grade_lect(), float):
            if self.middle_grade_stud() > other.middle_grade_lect():
                return f'{self.name} круче чем {other.name}'
            return f'{other.name} круче чем {self.name}'
        elif not isinstance(self.middle_grade_stud(), float) and isinstance(other.middle_grade_lect(), float):
            return f'{other.name} круче чем {self.name}'
        return f'{self.name} круче чем {other.name}'
    
    def grade_to_lecturer(self, lecturer, course, grade):  # Регистрирует оценку и в группе лекторов и в селфе лектора
        course = course.capitalize()
        if course in self.act_courses:
            if course in lecturer.courses and course in Lecturer.courses:
                lecturer.courses[course].append(grade)
                Lecturer.courses[course][list(Lecturer.courses[course]).index(f'{lecturer.name} {lecturer.surname}') + 1].append(grade)
                return f'Студент {self.name} поставил лектору {lecturer.name} {grade} по предмету {course}'
            else:
                return f'Преподаватель {lecturer.name} {lecturer.surname} не относится к курсу {course}'
        else:
            return f'У студента не такого курса'

class Mentor: 
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []
        
class Lecturer(Mentor):
    courses = {}
    list = []
    
    def __init__(self, name, surname, course):
        super().__init__(name, surname, course)
        self.courses = {self.course: []}
        Lecturer.list.append(f'{self.name} {self.surname}')
        if self.course not in Lecturer.courses:
            Lecturer.courses[self.course] = [f'{self.name} {self.surname}', []]
        if f'{self.name} {self.surname}' not in Lecturer.courses[self.course]:
            Lecturer.courses[self.course].append(f'{self.name} {self.surname}')
            Lecturer.courses[self.course].append([])

    def __str__(self):
        middle = self.middle_grade_lect()  
        return f'Имя: {self.name}\n'                f'Фамилия: {self.surname}\n'                f'Средняя оценка за лекции: {middle}'

    def middle_grade_lect(self):  
        middle = sum([sum(i) for i in self.courses.values()])
        m2 = []
        [[m2.append(i) for i in b] for b in self.courses.values()]
        if len(m2) != 0:
            return middle / len(m2)
        else:
            return f'У лектора {self.name} нет оценок'

    def __lt__(self, other):
        if not isinstance(other, Student):
            return f' Плохой кандидат для сравнения'  
        if isinstance(self.middle_grade_lect(), float) and isinstance(other.middle_grade_stud(), float):
            if self.middle_grade_lect() > other.middle_grade_stud():
                return f'{self.name} круче чем {other.name}'
            return f'{other.name} круче чем {self.name}'
        elif not isinstance(self.middle_grade_lect(), float) and isinstance(other.middle_grade_stud(), float):
            return f'{other.name} круче чем {self.name}'
        return f'{self.name} круче чем {other.name}'
        


class Reviewer(Mentor):
    
    courses = {}
    list = []

    def __init__(self, name, surname, course):
        super().__init__(name, surname, course)
        self.courses = {self.course: []}
        Reviewer.list.append(f'{self.name} {self.surname}')
        if self.course not in Reviewer.courses:
            Reviewer.courses[self.course] = [f'{self.name} {self.surname}', []]
        if self.name + ' ' + self.surname not in Reviewer.courses[self.course]:
            Reviewer.courses[self.course].append(f'{self.name} {self.surname}')
            Reviewer.courses[self.course].append([])

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'

    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
        if course not in Reviewer.courses:
            Reviewer.courses[course] = [f'{self.name} {self.surname}', []]
        if self.name + ' ' + self.surname not in Reviewer.courses[course]:
            Reviewer.courses[course].append(f'{self.name} {self.surname}')
            Reviewer.courses[course].append([])

    def grade_to_student(self, student, course, grade):  # в список оценок оценщика вписывается студент, которому он поставил оценку)
        course = course.capitalize()
        if isinstance(student, Student) and course in self.courses and course in student.act_courses:
            if course in student.act_courses and course in Student.courses:
                student.act_courses[course].append(grade)
                # сложное вычисление т.к. основной словарь Student.courses состоит из 'язык':[имя1, [оценки], имя2, [оценки]] и нужен поиск именно списка следующего после имени.
                Student.courses[course][list(Student.courses[course]).index(f'{student.name} {student.surname}') + 1].append(grade)
                Reviewer.courses[course][list(Reviewer.courses[course]).index(f'{self.name} {self.surname}') + 1].append(grade)
                self.courses[course].append(f'{student.name} {student.surname}')
                self.courses[course].append([])
                self.courses[course][self.courses[course].index(f'{student.name} {student.surname}')+1].append(grade)
                return f'Лектор {self.name} поставил студенту {student.name} {grade} по предмету {course}'
            else:
                return 'Несоответствие курсов'
        else:
            return 'Несоответствие курсов'


def middle_grade(group, course):
    print(group.courses)
    if course in group.courses:
        marks_quantity = 0
        marks_sum = 0
        for mark in range(1, len(group.courses[course]), 2):
            marks_quantity += len(group.courses[course][mark])
            marks_sum += sum(group.courses[course][mark])
        if marks_quantity != 0:
            return f'Средний бал среди всех по курсу {course} составляет {marks_sum / marks_quantity}'
        else:
            return 'Нет оценок'
    else:
        return f'Курса {course} нет в списке'
    
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


# In[ ]:




