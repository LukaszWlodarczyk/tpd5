from random import randint
import numpy as np

processes = []
burst_time = []
initial_burst_time = {}
completed_tasks = []
waiting_time = {}
quantum = 2
current_total_time = 0
n_processes = 10


def create_n_processes(n):
    global initial_burst_time
    for x in range(n):
        processes.append(x)
        burst = randint(1, 100)
        burst_time.append(burst)
        initial_burst_time[x] = burst
        waiting_time[x] = 0


def is_finished():
    if len(processes) == 0:
        return True


def find_shortest():
    min_burst = np.Inf
    position = None
    for iter, burst in enumerate(burst_time):
        if burst < min_burst and burst != 0:
            min_burst = burst
            position = iter
    return position, min_burst


def find_random():
    position = randint(0, len(burst_time)-1)
    return position, burst_time[position]


def add_waiting_time(process, delta):
    for key, value in waiting_time.items():
        if key == process or key in completed_tasks:
            continue
        waiting_time[key] += delta


def do_quantum():
    global current_total_time
    # position, burst = find_shortest()
    position, burst = find_random()
    to_str = f"Task: {processes[position]}, burst time before: {burst_time[position]}\n"
    if burst <= quantum:
        add_waiting_time(processes[position], burst)
        current_total_time += burst
        burst_time.pop(position)
        completed_tasks.append(processes[position])
        processes.pop(position)
        to_str += f"Task done."
    else:
        add_waiting_time(processes[position], quantum)
        current_total_time += quantum
        burst_time[position] -= quantum
        to_str += f"burst time after: {burst_time[position] }"
    return to_str


def calculate_total_time_in_system(process):
    return initial_burst_time[process] + waiting_time[process]


def calculate_average_time_in_system():
    total = 0
    for x in range(n_processes):
        total += calculate_total_time_in_system(x)
    return round(total/n_processes, 2)


def calculate_average_waiting_time_in_system():
    total = 0
    for x in range(n_processes):
        total += waiting_time[x]
    return round(total/n_processes, 2)


if __name__ == "__main__":
    create_n_processes(n_processes)
    while not is_finished():
        do_quantum()

    print(f"Total time: {current_total_time}")
    print(f"Completed tasks queue: {completed_tasks}")
    print(f"Processes waiting time: {waiting_time}")
    print(f"Initial burst time: {initial_burst_time}")
    for x in range(n_processes):
        print(f"Process {x} time in system: {calculate_total_time_in_system(x)}")
    print(f"Average process time in system: {calculate_average_time_in_system()}")
    print(f"Average waiting process time in system: {calculate_average_waiting_time_in_system()}")