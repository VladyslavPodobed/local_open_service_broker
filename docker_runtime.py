import subprocess
import docker
from config import COMPOSE_FILE
from time import sleep
from container_runtime import ContainerRuntime


docker_client = docker.from_env()


class DockerRuntime(ContainerRuntime):
    def spin_up_containers(self):
        docker_compose_up = subprocess.run(["docker", "compose", "-f", COMPOSE_FILE, "up", "-d"], capture_output=True)
        if docker_compose_up.returncode != 0:
            raise SystemExit(f"couldn't spin up containers: {docker_compose_up.stderr}")

    def containers_config(self) -> list:
        sleep(2)
        return [container.attrs for container in docker_client.containers.list()]

    def container_is_healthy(self, container_config: dict) -> bool:
        return bool(container_config["State"]["Running"])

    def all_containers_healthy(self, containers: list):
        unhealthy_containers = [container["Id"][:12] for container in containers if not self.container_is_healthy(container)]
        if unhealthy_containers:
            print(f"""couldn't spin up some containers
currently running containers: {[container["Id"][:12] for container in containers]}""")

    def main(self):
        self.spin_up_containers()
        containers_config = self.containers_config()
        self.all_containers_healthy(containers_config)
