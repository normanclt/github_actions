import pickle
import json
from typing import *
from icecream.icecream import ic


class Activity_Logger(object):
    _instance = None

    def __new__(cls, data: dict, filename: str, clear: bool = False):
        if cls._instance == None or clear:
            ic("Creating Instance")
            cls._instance = object.__new__(cls)
        else:
            ic()
            print("Existing instance found!")
        ic()
        print("Instance Returned")
        return cls._instance

    def __init__(self, data: dict, filename: str, clear: bool = False):
        self.data = data
        self.filename = filename
        self.write_to_disk()

    def write_to_disk(self):
        with open(self.filename, "a") as output_stream:
            output_stream.seek(0, 0)
            output_stream.write(f"{self.data},\n")

    def get_latest_activity(self) -> str:
        with open(self.filename, "r") as input_stream:
            input_stream.seek(0, 0)
            latest_activity = input_stream.readline().strip("\n").strip(",")
            if latest_activity == "":
                return None
            return eval(latest_activity)

    def get_activities(self, activity_line_number: int | None):
        if activity_line_number == None:
            with open(self.filename, "r") as output_stream:
                activities = output_stream.readlines()
                return output_stream.readlines()
        with open(self.filename, "r") as output_stream:
            return output_stream.readlines()[activity_line_number].strip("\n").strip(",")
