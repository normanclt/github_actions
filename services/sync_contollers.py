# this will manage syncs
# integrate activity logger, source_connectors
# sync_providers
# compare identifiers between source_connectors and push_providers
from services.push_providers import Rsync_Provider
from services.config_manager import Config_Manager
from services.activity_logger import Activity_Logger
from services.resource_connectors import Resource_Connector


class Sync_Controller():
    _instance = None

    def __new__(cls, config_manager: Config_Manager, clear: bool = False):
        if cls._instance == None or clear:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, config_manager: Config_Manager, clear: bool = False):
        self.config_manager = config_manager

    def _configure_resource_connector(self):
        self.resource_connector = Resource_Connector()
