from tinderlibs.middleware.queues_middleware import QueuesMiddleware
import signal

middleware = None


def get_middleware():
    global middleware
    if middleware is None:
        middleware = QueuesMiddleware()
    return middleware


def sigint_handler(_sig, _frame):
    middleware.stop()


signal.signal(signal.SIGINT, sigint_handler)
