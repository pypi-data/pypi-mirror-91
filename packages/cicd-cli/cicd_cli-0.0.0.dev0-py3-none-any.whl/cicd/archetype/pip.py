from cicd.archetype import IArchetype
from cicd.util import python_util

class Pip(IArchetype):
    def __init__(self, application_name):
        self.application_name = application_name
    def build(self):
        python_util.run_tests()
        python_util.build()
    def publish(self, lifecycle: str):
        print(python_util.get_version())
    def deploy(self, resource:str, lifecycle: str, version: str):
        pass
    def undeploy(self, resource: str, lifecycle: str):
        pass
    def smoke_test(self, lifecycle: str):
        pass
