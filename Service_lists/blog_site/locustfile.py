import os
from locust import HttpUser, TaskSet, task


class UserBehavior(TaskSet):
    @task
    def home(self):
        self.client.get("/")

    @task
    def upload(self):
        file_path = os.path.join(os.path.dirname(__file__), 'test_file.txt')
        if not os.path.isfile(file_path):
            print(f"File {file_path} does not exist.")
        files = {'file': open(file_path, 'rb')}
        self.client.post("/upload", files=files)


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 5000
    max_wait = 9000
