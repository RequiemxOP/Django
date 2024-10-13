# Task 3
import threading
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class RequestCounterMiddleware(MiddlewareMixin):
    request_count = 0
    lock = threading.Lock()  # Lock for thread safety

    def process_request(self, request):
        with self.lock:
            RequestCounterMiddleware.request_count += 1

    @classmethod
    def get_request_count(cls):
        with cls.lock:
            return cls.request_count

    @classmethod
    def reset_request_count(cls):
        with cls.lock:
            cls.request_count = 0
