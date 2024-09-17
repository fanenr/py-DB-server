http -f :5000/teacher/log \
    username='lilaoshi' \
    password='12345' |
    jq -r '.token' >teacher.token

http -f :5000/student/log \
    username='zhangsan' \
    password='12345' |
    jq -r '.token' >student.token
