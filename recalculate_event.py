"""
Description: This script demonstrate how to reply the events from a log and recalculate results
Author: Xiaoying Nie
Date: 2025-02-11
Version: 1.0
"""

import json
EVENT_LOG_FILE = "event_log.txt"


class WorkerService:
    def __init__(self):
        self.state = 0  # simulate the state

    def process_event(self, event):
        # Idempotency check: skip if the event has already been processed
        if event.get("processed"):
            return
        # simulate event processing logic
        if event["type"] == "add":
            self.state += event["value"]
        elif event["type"] == "subtract":
            self.state -= event["value"]

        event["processed"] = True

    def get_state(self):
        return self.state


def read_events(log_file):
    """
    read events from the log
    """
    with open(log_file, "r") as file:
        for line in file:
            yield json.loads(line)


def recalculate():
    """
    recalculate the results
    """
    worker = WorkerService()
    events = read_events(EVENT_LOG_FILE)

    for event in events:
        worker.process_event(event)
    print(f"Recalculated state: {worker.get_state()}")


# Execute recalculation
recalculate()









