from data.jobs import JobList


class User(object):

    def __init__(self, user_id):
        self.user_id = user_id
        self.job_list = JobList()

        self.job_num_pending = 0
        self.job_num_pending_limit = float("inf")
        self.job_num_running = 0
        self.job_num_running_limit = float("inf")

        self.core_num_pending = 0
        self.core_num_pending_limit = float("inf")
        self.core_num_running = 0
        self.core_num_running_limit = float("inf")

        self.cputime = 0
        self.cputime_limit = float("inf")

        self.events = []
        return
    #   End __init__

    def output(self):
        print("User", self.user_id, "'s jobs:")
        for job in self.job_list.jobs:
            for event in job.events:
                event.output()
        return
    #   End output
#   End User


class UserList(object):

    def __init__(self):
        self.users = []
        return
    #   End __init__

    def push(self, user):
        self.users.append(user)
        return
    #   End push

    def pop(self, user):
        if not self.users:
            print("User list pop error: "
                  "Popping from an empty list. "
                  "Terminating.")
            raise UserListEmptyPopError
        if user not in self.users:
            print("User list pop error: "
                  "Popping user not found."
                  "Terminating.")
            raise UserListIllegalPopError
        self.users.remove(user)
        return
    #   End Pop
#   End UserList


class UserListError(Exception):
    pass


class UserListEmptyPopError(UserListError):
    pass


class UserListIllegalPopError(UserListError):
    pass


class UserGroup(object):

    def __init__(self, group_id):
        self.group_id = group_id
        self.user_list = UserList()
        return
    #   End __init__
#   End UserGroup
