class MiddlewareTest:
    def __init__(self):
        self.packages = []

    def send(self, data):
        self.packages.append(data)

    def stop(self):
        pass

    def publish(self, data):
        self.send(data)

    def start_receiving(self, callback):
        for message in self.packages:
            callback(message)
