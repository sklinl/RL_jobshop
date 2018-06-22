import numpy as np
import glob
import os
import math
path = '//140.114.60.83/個人-林聖凱(sklin)/jobshop\\jobshop\\instances'
os.path.exists(os.path.join(path, 'ft06.txt'))
with open(os.path.join(path, 'ft06.txt')) as f:
    line = f.readlines()
    print(line)


# data
num_jobs = int(line[1].split()[0])
num_machines = int(line[1].split()[1])

name = "machine_time_" # This has to be a string, variables like my_var1, my_var2 will be created.
value = "[]" # This also has to be a string, even when you want to assign integers! When you want to assign a string "3", you'd do this: value = "'3'"
amount = num_machines # This must be an integer. This many variables will be created (my_var1, my_var2 ... my_var5).
for i in range(1, amount+1):
    command_variable = ""
    command_variable = name + str(i) + " = " + value
    exec(command_variable)

processing_time = []
for i in range(3, 3+num_jobs):
    each_time = [int(line[i].split()[j]) for j in range(num_machines)]
    processing_time.append(each_time)
sort_machine = []
for i in range(4+num_jobs, 4+num_jobs+num_machines):
    each_time = [int(line[i].split()[j]) for j in range(num_machines)]
    sort_machine.append(each_time)

time = 0
def reset():
    state_reset = np.zeros(shape=[num_machines, num_jobs])
    # state_reset[-1] = [1, 2, 3, 4, 5, 6]
    return state_reset

# return which machine can use and whether done or not
def check_job():
    now = []
    for i in range(6):
        try:
            now.append(sort_machine[i][0])
        except:
            print('job_{} is done'.format(i))

    machine = np.unique(now)
    if len(machine) != 0:
        done = False
    else:
        done = True

    return machine, done


def step(observation, action):
    state = observation
    queue = [row[0] for row in sort_machine]
    job_and_machine = np.argmax(action)
    job = math.ceil(job_and_machine / num_jobs)
    if job_and_machine // num_jobs == 0:
        machine = num_machines
    else:
        machine = job_and_machine // num_jobs

    if job == 7:     # machine special time: RL decide rest
        for i in range(1, 1+num_machines):
            name = "machine_time_"
            command = ''
            command = name + str(i) + '.' + 'append(1)'
            exec(command)
    else:
        if machine = queue[job-1]:
            state[machine - 1][job - 1] = 1
            sort_machine[job - 1].pop(0)
            for _ in range(processing_time[job - 1][5 - 1]):
                sort_machine[job - 1].insert(0, 0)
            name = "machine_time_"
            command = ''
            command = name + str(machine) + '.append(processing_time[job-1][machine-1])'
            exec(command)
        else:
            for i in range(num_jobs):
                if sort_machine[i] == 0:
                    sort_machine[i].pop(0)
            for i in range(1, 1 + num_machines):
                name = "machine_time_"
                command = ''
                command = name + str(i) + '.' + 'append(1)'
                exec(command)
    if np.sum(state) == num_jobs*num_machines:
        done = True
        total_time = []
        for i in range(1, 1 + num_machines):
            # name = "machine_time_"
            # command = ''
            command = 'total_time.append(machine_time_{})'.format(i+1)
            exec(command)
        max_time = np.max([np.sum(i) for i in total_time]) # rewards
    else:
        done = False
        max_time = 0 # rewards

    return state, max_time, done

