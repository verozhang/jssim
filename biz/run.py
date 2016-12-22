import gl
from data.jobs import *
from data.cores import *


def simulate():
    while gl.current_time != gl.finish_time:
        gl.current_time += 1
        #   Handle finish
        gl.queue_running.sort_by_finish_time()
        while gl.queue_running.try_has_job() and gl.queue_running.get_head().try_finish(gl.current_time):
            handle_finish(gl.queue_running.get_head(), gl.current_time)

        #   Handle arrive
        gl.queue_waiting.sort_by_submit_time()
        while gl.queue_waiting.try_has_job() and gl.queue_waiting.get_head().try_arrive(gl.current_time):
            handle_arrive(gl.queue_waiting.get_head(), gl.current_time)

        #   Handle pend
        gl.queue_arrived.sort_by_start_time()
        while gl.queue_arrived.try_has_job() and gl.queue_arrived.get_head().try_run(gl.current_time):
            for queue in gl.queues_pending:
                if queue.try_suitable(gl.queue_arrived.get_head()):
                    handle_pend(gl.queue_arrived.get_head(), queue, gl.current_time)
                    break
                else:
                    continue
            else:
                raise JobNoSuitableQueueError

        for queue in gl.queues_pending:
            while queue.try_has_job() and queue.get_head().try_run and len(gl.cores_vacant.cores) >= queue.get_head().num_processors:
                if queue.get_head().stop_time < gl.current_time + queue.get_head().run_time:
                    handle_abandon(queue.get_head(), queue, gl.current_time)
                else:
                    handle_run(queue.get_head(), queue, gl.current_time)
    return


def handle_arrive(job, time):
    event = JobEventArrive(job, time)
    job.events.append(event)

    job.status = JobStatus.ARRIVED
    gl.queue_arrived.load(job)
    gl.queue_waiting.unload(job)
    return
#   End handle_arrive


def handle_pend(job, queue, time):
    event = JobEventPend(job, queue, time)
    job.events.append(event)

    job.status = JobStatus.PENDING
    queue.load(job)
    gl.queue_arrived.unload(job)
    return
#   End handle_pend


def handle_run(job, queue, time):
    run(job, time)
    gl.queue_running.load(job)
    queue.unload(job)
    event = JobEventRun(job, time)
    job.events.append(event)
    return
#   End handle_run


def handle_finish(job, time):
    event = JobEventFinish(job, time)
    job.events.append(event)

    stop(job, time)
    gl.queue_finished.load(job)
    gl.queue_running.unload(job)
    return
#   End handle_finish


def handle_abandon(job, queue, time):
    event = JobEventAbandon(job, queue, time)
    job.events.append(event)

    job.status = JobStatus.ABANDONED
    gl.queue_abandoned.load(job)
    queue.unload(job)
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
