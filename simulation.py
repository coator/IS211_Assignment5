import argparse
import csv
import itertools


class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def peek(self):
        return self.items[len(self.items) - 1]


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

    def queuepull():
        with open(args.fileloc, newline='') as csvfile:
            current_list = []
            reader = csv.reader(csvfile, delimiter=' ')
            for row in reader:
                current_list.append(tuple(', '.join(row).split(',')))
            return current_list

    url_queue = Queue()
    queue_list = queuepull()
    queue_list_divided = []
    while 0 < len(queue_list):
        if url_queue.is_empty() or url_queue.items[0].current_request[0] == queue_list[0][0]:
            request_check = queue_list.pop(0)
            request = Request(request_check)
            url_queue.enqueue(request)
        else:
            templist = []
            for i in range(url_queue.size()):
                templist.append(url_queue.dequeue())
            queue_list_divided.append(templist)
            request_check = queue_list.pop(0)
            request = Request(request_check)
            url_queue.enqueue(request)
    templist = []
    for i in range(url_queue.size()):
        templist.append(url_queue.dequeue())
    queue_list_divided.append(templist)

    if args.servers == 1:
        simulateOneServer(queue_list_divided)
    elif args.servers > 1:
        simulateManyServers(queue_list_divided, args.servers)
    else:
        print('an error has occurred, servers value must be greater than 0')


def simulateOneServer(queuelist):
    url_queue = Queue()
    current_server = Server()
    count = len(queuelist)
    sum_total_wait_times = []
    for queries in queuelist:
        for i in queries:
            url_queue.enqueue(i)
        if not current_server.busy():
            waiting_times = []
            while not url_queue.is_empty():
                next_task = url_queue.dequeue()
                waiting_times.append(next_task.wait_time())
                current_server.start_next(next_task)

            current_server.tick()
            sum_total_wait_times.append(waiting_times)

            average_wait = sum(waiting_times) / len(queries)
            print("Average wait %6.2f secs %3d queries remaining." % (average_wait, count))
            count -= 1
    sum_total_wait_times = sum(sum_total_wait_times, [])
    sum_total_wait_times = sum(sum_total_wait_times)
    print("Average wait %6.2f for single server" % (sum_total_wait_times / len(queuelist)))


def simulateManyServers(queuelist, int_server):
    seq = list(range(0, int_server))
    seq = {name: Server(name=name) for name in seq}
    round_robin = itertools.cycle(seq)
    url_queue = Queue()
    current_server = seq[next(round_robin)]
    count = len(queuelist)
    sum_total_wait_times = []
    for queries in queuelist:
        for i in queries:
            url_queue.enqueue(i)
        if not current_server.busy():
            waiting_times = []
            while not url_queue.is_empty():
                next_task = url_queue.dequeue()
                waiting_times.append(next_task.wait_time())
                current_server.start_next(next_task)
            current_server = seq[next(round_robin)]
            current_server.tick()
            sum_total_wait_times.append(waiting_times)

            average_wait = sum(waiting_times) / len(queries)
            print("Average wait %6.2f secs %3d queries remaining." % (average_wait, count))
            count -= 1
    sum_total_wait_times = sum(sum_total_wait_times, [])
    sum_total_wait_times = sum(sum_total_wait_times)
    print("Average wait %6.2f for total of %1d servers used" % (sum_total_wait_times / len(queuelist) / int_server,
                                                                int_server))


main()
