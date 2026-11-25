from locust import HttpUser, task, between


class BlogUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def open_home(self):
        self.client.get("/", name="Главная страница")
