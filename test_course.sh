token='Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNTk2MzE2MywianRpIjoiZmE4NjI1OGItZTYzZS00YjI5LTk0NGQtNTQwMWZkYjE3MTMxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzI1OTYzMTYzLCJjc3JmIjoiMWM3ZWZjN2UtZjUyYy00ZDlhLTk5ZWYtZWRmYTMzYWU5YjMzIiwiZXhwIjoxNzI2NTY3OTYzfQ.DY1nMbK9kjJXlXCzNZrH__otK4lziMdG-cPJRzXjTSE'

http -f :5000/teacher/new \
    name='C 语言程序设计' \
    start='2024-09-10' \
    "$token"

http :5000/teacher/list \
    "$token"
