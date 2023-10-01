class Config_Manager:

    def __init__(self, *args):
        for arg in args:
            setattr(self, arg, None)
