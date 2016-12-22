from data.jobs import Job, JobDuplicateIDError
from data.users import User
import gl


def input_file(file_name):
    #   Now can only read from text. Can add reading .XLS later.
    #   Read from file.
    in_file = open(file_name, 'r')
    #   Read each line.
    for line in in_file.readlines():
        line = line.split()

        job_id = int(line[0])
        for job in gl.jobs_all.jobs:
            if job.job_id == job_id:
                raise JobDuplicateIDError

        user_id = int(line[1])
        #   Search for user.
        for user in gl.users_all.users:
            #   Found user.
            if user.user_id == user_id:
                current_user = user
                break
        # Cannot find. Create new user.
        else:
            current_user = User(user_id)
            gl.users_all.push(current_user)

        submit_time = int(line[2])
        start_time = int(line[3])
        stop_time = int(line[4])
        run_time = int(line[5])
        num_processors = int(line[6])
        job = Job(job_id, current_user, submit_time, start_time, stop_time, run_time, num_processors)
        gl.jobs_all.push(job)
        current_user.job_list.push(job)
    return
#   End input
