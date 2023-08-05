class IArchetype():

    def __init__(self, application_name):
        self.application_name = application_name

    def build(self):
        pass
    def publish(self, lifecycle: str):
        pass
    def deploy(self, resource:str, lifecycle: str, version: str):
        pass
    def undeploy(self, resource: str, lifecycle: str):
        pass
    def smoke_test(self, lifecycle: str):
        pass
