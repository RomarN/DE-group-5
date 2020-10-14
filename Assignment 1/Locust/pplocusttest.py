from locust import HttpUser, task, between


class WebsiteTestUser(HttpUser):
    wait_time = between(0.5, 3.0)

    def on_start(self):
        self.client.post("/training-dbpp/fires")



    def on_stop(self):
        pass


    @task(1)
    def read_table(self):
        self.client.get("/training-dbpp/fires")
