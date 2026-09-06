from abc import ABC, abstractmethod


class ContainerRuntime(ABC):

    @staticmethod
    @abstractmethod
    def verify_dependency():
        pass

    @abstractmethod
    def spin_up_containers(self):
        pass

    @abstractmethod
    def inspect_containers(self):
        pass

    @abstractmethod
    def are_all_containers_up(self):
        pass

    @abstractmethod
    def are_all_containers_healthy(self):
        pass

