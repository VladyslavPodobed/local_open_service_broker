from abc import ABC, abstractmethod


class ContainerRuntime(ABC):

    @abstractmethod
    def spin_up_containers(self):
        pass

    @abstractmethod
    def list_running_containers(self):
        pass



