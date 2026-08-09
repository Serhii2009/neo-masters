import time
import random
from queue import Queue
from itertools import count

SERVICE_TYPES = [
    "Password reset",
    "Hardware repair",
    "Software installation",
    "Network issue",
    "Account activation",
]

request_queue = Queue()
request_id = count(1)


def generate_request() -> dict:
    request = {
        "id": next(request_id),
        "type": random.choice(SERVICE_TYPES),
        "created_at": time.strftime("%H:%M:%S"),
    }
    request_queue.put(request)

    print(f"New request #{request['id']} ({request['type']}) added to the queue.")
    return request


def process_request() -> None:
    if request_queue.empty():
        print("The queue is empty, there is nothing to process.")
        return

    request = request_queue.get()
    print(
        f"Processing request #{request['id']} "
        f"({request['type']}, created at {request['created_at']})..."
    )

    time.sleep(0.5)
    request_queue.task_done()
    print(f"Request #{request['id']} has been completed.")


def main() -> None:
    cycles = 5

    for cycle in range(1, cycles + 1):
        print(f"\nCycle {cycle} of {cycles}")

        for _ in range(random.randint(1, 3)):
            generate_request()

        process_request()
        print(f"Requests waiting in the queue: {request_queue.qsize()}")

    print("\nProcessing the remaining requests")
    while not request_queue.empty():
        process_request()

    print("\nAll requests have been processed, the service center is closed.")


main()
