from locust import HttpUser, task, between

class DataAnalysisUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def load_home(self):
        self.client.get("/")

    @task
    def execute_notebook(self):
        self.client.post("/api/contents/test_notebook.ipynb")

