import argparse
import csv
import itertools


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

    def peek(self):
        return self.items[len(self.items)-1]


class Server:
    def __init__(self, name=str()):
        self.current_task = None
        self.time_remaining = 0
        self.name = name

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
        return self.request_timestamp


def main():
    server_queue = Queue()
    parser = argparse.ArgumentParser()
    parser.add_argument("--fileloc", type=str, help="this is the file you wish to use for the parser")
    parser.add_argument("--servers", type=int, default=1, help="this is for how many servers you wish to use")
    args = parser.parse_args()

    if args.servers == 1:
        simulateOneServer(args)
    elif args.servers > 1:
        simulateManyServers(args)
    else:
        print('an error has occurred, servers value must be greater than 0')


def simulateOneServer(args):
    waiting_times = []
    available_server = Server()
    current_queue = Queue()

    with open(args.fileloc, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        for row in reader:
            currentrow = tuple(', '.join(row).split(','))
            request = Request(currentrow)
            current_queue.enqueue(request)

    while current_queue.size() > 0:
        if (not available_server.busy()) and (not current_queue.is_empty()):
            next_task = current_queue.dequeue()
            waiting_times.append(next_task.wait_time())
            available_server.start_next(next_task.request_timestamp)

        available_server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait {0} secs in queue.".format(average_wait))


def simulateManyServers(args):
    waiting_times = []
    available_server = Server()
    current_queue = Queue()
    seq = list(range(0, args.servers))

    seq = {name: Server(name=name) for name in seq}
    round_robin = itertools.cycle(seq)

    with open(args.fileloc, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        for row in reader:
             next(round_robin)
            #TODO: I need to go ahead and incorporate the round robin to "eat" the Queries
            currentrow = tuple(', '.join(row).split(','))
            request = Request(currentrow)
            current_queue.enqueue(request)


    while current_queue.size() > 0:

        if (not available_server.busy()) and (not current_queue.is_empty()):
            next_task = current_queue.dequeue()
            g = next_task.wait_time()
            #print(g)
            waiting_times.append(g)
            available_server.start_next(next_task.request_timestamp)

        available_server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait {0} secs in queue.".format(average_wait))

main()
