class Cache():
    LIFETIME_IN_NANSECS = 30 * 1000_000_000

    def __init__(self):
        self.data = {}

    def put(self, request, response):
        self.data[request] = (response, time.time_ns())

    def get(self, request):
        if request in self.data:
            dt = time.time_ns() - self.data[request][1]
            if dt > Cache.LIFETIME_IN_NANSECS:
                del self.data[request]
            else:
                return self.data[request][0]
        return None