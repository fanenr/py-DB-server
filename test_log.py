import requests

BASE_URL = "http://127.0.0.1:5000/"
TEACHER_LOG_URL = BASE_URL + "teacher/log"


def main():
    data = {"username": "lilaoshi", "password": "12345"}
    res = requests.post(url=TEACHER_LOG_URL, data=data)
    print(res.text)

    json = res.json()
    token = json["access_token"]
    headers = {"Authorization": "Bearer " + token}

    res = requests.get(url="http://127.0.0.1:5000/test", headers=headers)
    print(res.text)


if __name__ == "__main__":
    main()
