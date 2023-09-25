class Sync_Provider:
    def synchronize(self, sync_check_requirement: bool):
        pass


class Rsync_Provider():
    # insert rsync configuration and singleton
    _instance = None

    def __new__(cls, data: dict, filename: str, clear: bool = False):
        if cls._instance == None or clear:
            print("Creating Instance")
            cls._instance = object.__new__(cls)
        else:
            print("Existing instance found!")
        print("Instance Returned")
        return cls._instance

    def synchronize(self, fn_sync_check_requirement):
        #
        return fn_sync_check_requirement()


class Repo_Provider():
    # insert repo configuration
    _instance = None

    def __new__(cls, data: dict, filename: str, clear: bool = False):
        if cls._instance == None or clear:
            print("Creating Instance")
            cls._instance = object.__new__(cls)
        else:
            print("Existing instance found!")
        print("Instance Returned")

    # compare github01 latest commit on main and log
    # leverage function to synch_check_requirement
    #

    def synchronize(self, fn_sync_check_requirement):
        # implement synchronization logic
        pass
