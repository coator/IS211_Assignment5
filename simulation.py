import argparse
import csv


class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Server:
    def __init__(self):
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task is not None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task is not None:
            return True
        else:
            return False

    def start_next(self, new_task):
        self.current_task = new_task


class Request:
    def __init__(self, request_inst):
        self.server_query_time = int(request_inst[0])
        self.request_timestamp = int(request_inst[2])
        self.current_request = request_inst

    def get_requesttime(self):
        return self.request_timestamp

    def get_current_request(self):
        return self.current_request

    def wait_time(self):
        return self.server_query_time - self.request_timestamp


def main():
    server_queue = Queue()
    parser = argparse.ArgumentParser()
    parser.add_argument("--fileloc", help="this is the file you wish to use for the parser")
    args = parser.parse_args()

    with open(args.fileloc, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        for row in reader:
            currentrow = ', '.join(row)
            currentrow = tuple(currentrow.split(','))
            request = Request(currentrow)
            server_queue.enqueue(request)

    simulateOneServer(server_queue)


def simulateOneServer(query):
    waiting_times = []
    available_server = Server()

    for current_Request in range(0,query.size()):

        if (not available_server.busy()) and (not query.is_empty()):
            next_task = query.dequeue()

            waiting_times.append(next_task.wait_time())
            available_server.start_next(next_task.request_timestamp)

        available_server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait {0} secs {1} tasks remaining.".format(average_wait, query.size()))



main()
