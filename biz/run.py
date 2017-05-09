import gl
from data.queues import *
from data.jobs import *
from data.cores import *


def simulate():
    while (gl.queue_waiting.try_has_job() or
           gl.queue_arrived.try_has_job() or
           gl.queue_running.try_has_job()):
        gl.current_time += 1
        #   Handle finish
        while (gl.queue_running.try_has_job() and
               gl.queue_running.get_head().try_finish(gl.current_time)):
            handle_finish(gl.queue_running.get_head(), gl.current_time)

        #   Handle arrive
        while (gl.queue_waiting.try_has_job() and
               gl.queue_waiting.get_head().try_arrive(gl.current_time)):
            handle_arrive(gl.queue_waiting.get_head(), gl.current_time)
            gl.queue_arrived.sort_by_start_time()

        #   Handle pend
        while (gl.queue_arrived.try_has_job() and
               gl.queue_arrived.get_head().try_run(gl.current_time)):
            #   Sort queues in priority order.
            gl.queues_pending.sort(key=lambda x: x.priority, reverse=True)
            for queue in gl.queues_pending:
                if queue.try_suitable(gl.queue_arrived.get_head()):
                    if ((gl.queue_arrived.get_head().user not in queue.user_job_num_pending) or
                       queue.user_job_num_pending[gl.queue_arrived.get_head().user] < queue.user_job_num_pending_limit):
                        handle_pend(gl.queue_arrived.get_head(), queue, gl.current_time)
                    else:
                        requeue(gl.queue_arrived.get_head(), 60)
                    break

                else:
                    continue
            else:
                raise JobNoSuitableQueueError

        #   Handle run/abandon
        for queue in gl.queues_pending:
            while (queue.try_has_job() and
                   queue.get_head().try_run and
                   len(gl.cores_vacant.cores) >= queue.get_head().num_processors):
                #   Cannot finish. Abandon current job.
                if queue.get_head().stop_time < gl.current_time + queue.get_head().run_time:
                    handle_abandon(queue.get_head(), queue, gl.current_time)
                #   Can finish.
                else:
                    if ((queue not in gl.queue_job_num) or
                       (gl.queue_job_num[queue] < queue.queue_job_num)):
                        handle_run(queue.get_head(), gl.current_time)
                        gl.queue_running.sort_by_finish_time()
                    else:
                        requeue(queue.get_head, 60)

    gl.finish_time = gl.current_time
    print("Finish time:", gl.finish_time)
    return


def handle_arrive(job, time):
    job.status = JobStatus.ARRIVED
    job.queue_from = gl.queue_arrived

    gl.queue_arrived.load(job)
    gl.queue_waiting.unload(job)

    event = JobEventArrive(job, time)
    job.events.append(event)
    event.output()
    return
#   End handle_arrive


def handle_pend(job, queue, time):
    job.status = JobStatus.PENDING
    job.queue_from = queue

    job.queue_from.job_num_pending += 1
    job.queue_from.core_num_pending += job.num_processors

    if job.user not in job.queue_from.user_job_num_pending:
        job.queue_from.user_job_num_pending[job.user] = 1
    else:
        job.queue_from.user_job_num_pending[job.user] += 1

    if job.user not in job.queue_from.user_core_num_pending:
        job.queue_from.user_core_num_pending[job.user] = job.num_processors
    else:
        job.queue_from.user_core_num_pending[job.user] += job.num_processors

    queue.load(job)
    gl.queue_arrived.unload(job)

    job_event = JobEventPend(job, queue, time)
    job.events.append(job_event)
    job_event.output()
    queue_event = QueueEventLoad(queue, job, time)
    queue.events.append(queue_event)
    return
#   End handle_pend


def handle_run(job, time):
    run(job, time)

    job.queue_from.job_num_running += 1
    job.queue_from.job_num_pending -= 1
    job.queue_from.core_num_running += job.num_processors
    job.queue_from.core_num_pending -= job.num_processors

    gl.queue_running.load(job)
    job.queue_from.unload(job)

    job_event = JobEventRun(job, time)
    job.events.append(job_event)
    job_event.output()
    queue_event = QueueEventUnload(job.queue_from, job, time)
    job.queue_from.events.append(queue_event)
    return
#   End handle_run


def handle_finish(job, time):
    stop(job, time)

    job.queue_from.job_num_running -= 1
    job.queue_from.core_num_running -= job.num_processors

    gl.queue_finished.load(job)
    gl.queue_running.unload(job)

    event = JobEventFinish(job, time)
    job.events.append(event)
    event.output()
    return
#   End handle_finish


def handle_abandon(job, queue, time):
    job.queue_from.job_num_pending -= 1
    job.queue_from.core_num_pending -= job.num_processors

    job.status = JobStatus.ABANDONED
    gl.queue_abandoned.load(job)
    queue.unload(job)

    event = JobEventAbandon(job, queue, time)
    job.events.append(event)
    return
#   End handle_abandon


def run(job, time):
    if job.status != JobStatus.PENDING:
        raise JobIllegalRunError

    for i in range(job.num_processors):
        core_event = CoreEventOccupy(gl.cores_vacant.get_head(), job, time)
        gl.cores_vacant.get_head().events.append(core_event)
        gl.cores_vacant.get_head().occupy(job)
        job.core_list.push(gl.cores_vacant.get_head())
        gl.cores_vacant.pop(gl.cores_vacant.get_head())

    job.real_start_time = time
    job.real_wait_time = time - job.start_time
    job.status = JobStatus.RUNNING
    return
#   End run


def stop(job, time):
    if job.status != JobStatus.RUNNING:
        raise JobIllegalStopError

    for i in range(job.num_processors):
        core_event = CoreEventRelease(job.core_list.get_head(), time)
        job.core_list.get_head().events.append(core_event)
        job.core_list.get_head().release()
        gl.cores_vacant.push(job.core_list.get_head())
        job.core_list.pop(job.core_list.get_head())

    job.real_end_time = time
    job.real_run_time = time - job.real_start_time
    job.status = JobStatus.FINISHED
    return
#   End stop


def requeue(job, time_diff):
    job.start_time += time_diff
    job.queue_from.sort_by_start_time()

    event = JobEventRequeue(job, gl.current_time, time_diff)
    job.events.append(event)
    return
#   End requeue
