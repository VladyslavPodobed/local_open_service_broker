from abc import ABC, abstractmethod


class ContainerRuntime(ABC):
    @abstractmethod
    def spin_up_containers(self):
        pass

    @abstractmethod
    def all_containers_healthy(self, containers):
        pass

    @abstractmethod
    def main(self):
        pass
