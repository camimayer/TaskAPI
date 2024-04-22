
class Task(object):

    def __init__(self) -> None:
        self.createdByUid: str = ""
        self.createdByName: str = ""
        self.assignedToUid: str = ""
        self.assignedToName: str = ""        
        self.description: str = ""
        self.done: bool = False