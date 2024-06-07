from locust import HttpUser, task, between

class EcommerceUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def load_home(self):
        self.client.get("/")

    @task
    def view_product(self):
        # Assuming there's a product with ID 1
        self.client.get("/product/1")

    @task
    def search_product(self):
        self.client.get("/search?q=laptop")

    @task
    def view_cart(self):
        self.client.get("/cart")

