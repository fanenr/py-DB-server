teacher_token=$(cat teacher.token)
teacher_header="Authorization: Bearer $teacher_token"

http -f :5000/teacher/new \
    name='C 语言程序设计' \
    start='2024-09-10' \
    "$teacher_header"

http :5000/teacher/list \
    "$teacher_header"

http -f :5000/teacher/grade \
    cid='1' sid='1' score='80' \
    "$teacher_header"

student_token=$(cat student.token)
student_header="Authorization: Bearer $student_token"

http -f :5000/student/take \
    cid='1' "$student_header"

http :5000/student/list \
    "$student_header"
