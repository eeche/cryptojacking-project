from locust import HttpUser, TaskSet, task

class UserBehavior(TaskSet):
    @task
    def home(self):
        self.client.get("/")

    @task
    def upload(self):
        files = {'file': open('test_file.txt', 'rb')}
        self.client.post("/upload", files=files)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 5000
    max_wait = 9000

