import gl
from data.queues import *
from data.jobs import *


def try_pend():
    flag = False
    for queue in gl.queues_pending:
        flag = flag or queue.try_has_job()
    return flag


def simulate():
    while (gl.queue_waiting.try_has_job() or
           gl.queue_arrived.try_has_job() or
           gl.queue_running.try_has_job() or
           try_pend()):
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
                    if queue.try_pending_limit(gl.queue_arrived.get_head()) and \
                            queue.try_user_pending_limit(gl.queue_arrived.get_head()):
                        handle_pend(gl.queue_arrived.get_head(), queue, gl.current_time)
                    # else:
                    #    requeue(gl.queue_arrived.get_head(), 60)
                    break

                else:
                    continue
            else:
                raise JobNoSuitableQueueError

        #   Handle run/abandon
        for queue in gl.queues_pending:
            while (queue.try_has_job() and
                   queue.get_head().try_run):
                #   Cannot finish. Abandon current job.
                if queue.get_head().stop_time < gl.current_time + queue.get_head().run_time:
                    handle_abandon(queue.get_head(), gl.current_time)
                #   Can finish.
                else:
                    if (queue.try_running_limit(queue.get_head()) and
                            queue.try_user_running_limit(queue.get_head())):
                        for resource in queue.resource_pools.resource_list:
                            if resource.cores_available >= queue.get_head().num_processors:
                                handle_run(queue.get_head(), gl.current_time, resource)
                                gl.queue_running.sort_by_finish_time()
                                break
                        else:
                            break
                    break
                    # else:
                    #   requeue(queue.get_head(), 60)

        #stat()

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

    queue.total_job_num += 1
    queue.total_core_num += job.num_processors
    return
#   End handle_pend


def handle_run(job, time, resource):
    run(job, time, resource)

    job.queue_from.job_num_running += 1
    job.queue_from.job_num_pending -= 1
    job.queue_from.core_num_running += job.num_processors
    job.queue_from.core_num_pending -= job.num_processors

    gl.queue_running.load(job)
    job.queue_from.unload(job)

    job_event = JobEventRun(job, time, resource)
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


def handle_abandon(job, time):
    job.queue_from.job_num_pending -= 1
    job.queue_from.core_num_pending -= job.num_processors

    job.status = JobStatus.ABANDONED
    gl.queue_abandoned.load(job)
    job.queue_from.unload(job)

    job_event = JobEventAbandon(job, job.queue_from, time)
    job.events.append(job_event)
    queue_event = QueueEventUnload(job.queue_from, job, time)
    job.queue_from.events.append(queue_event)
    return
#   End handle_abandon


def run(job, time, resource):
    if job.status != JobStatus.PENDING:
        raise JobIllegalRunError

    core_needed = job.num_processors

    for node in resource.node_list:
        if node.core_vacant > 0:
            if core_needed <= node.core_vacant:
                current_core_num = core_needed
            else:
                current_core_num = node.core_vacant
            core_needed -= current_core_num
            node.occupy(job, current_core_num)
            job.node_usage[node] = current_core_num
            if core_needed == 0:
                break

    resource.occupy(job, job.num_processors)

    job.resource_pool_usage = resource
    job.real_start_time = time
    job.real_wait_time = time - job.start_time

    gl.sum_wait_time += job.real_wait_time
    gl.max_wait_time = max(gl.max_wait_time, job.real_wait_time)

    job.queue_from.total_wait_time += job.real_wait_time
    job.queue_from.max_wait_time = max(job.queue_from.max_wait_time, job.real_wait_time)

    job.status = JobStatus.RUNNING
    return
#   End run


def stop(job, time):
    if job.status != JobStatus.RUNNING:
        raise JobIllegalStopError

    for node in job.node_usage:
        node.cputime_sum += node.status[job] * job.run_time
        node.release(job)

    job.resource_pool_usage.release(job)

    job.real_end_time = time
    job.real_run_time = time - job.real_start_time
    job.turnaround_time = job.real_run_time + job.real_wait_time
    job.response_ratio = job.turnaround_time / job.real_run_time

    gl.sum_run_time += job.real_run_time
    gl.sum_cpu_time += job.real_run_time * job.num_processors

    gl.max_run_time = max(gl.max_run_time, job.real_run_time)
    gl.max_cpu_time = max(gl.max_cpu_time, (job.real_run_time * job.num_processors))
    gl.max_response_ratio = max(gl.max_response_ratio, job.response_ratio)

    job.queue_from.total_run_time += job.real_run_time
    job.queue_from.total_cpu_time += job.real_run_time * job.num_processors
    job.queue_from.max_run_time = max(job.queue_from.max_run_time, job.real_run_time)
    job.queue_from.max_cpu_time = max(job.queue_from.max_cpu_time, (job.real_run_time * job.num_processors))
    job.queue_from.max_response_ratio = max(job.queue_from.max_response_ratio, job.response_ratio)

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


def stat():
    #gl.cpu_occupation_status[gl.current_time] = gl.resource_all.cores_all - gl.resource_all.cores_available
    #gl.cpu_occupation_rate[gl.current_time] = (gl.resource_all.cores_all - gl.resource_all.cores_available) \
                                              #/ gl.resource_all.cores_all
    total_waiting_job_num = 0
    total_waiting_core_num = 0
    for queue in gl.queues_pending:
        for job in queue.job_list:
            total_waiting_job_num += 1
            total_waiting_core_num += job.num_processors
    gl.total_waiting_job_num[gl.current_time] = total_waiting_job_num
    gl.total_waiting_core_num[gl.current_time] = total_waiting_core_num
