import subprocess
import docker
from typing import Any
from container_runtime import ContainerRuntime


docker_client = docker.from_env()


class DockerRuntime(ContainerRuntime):

    @staticmethod
    def verify_dependency() -> int:
        try:
            docker_compose_dependency = subprocess.run(['docker', 'compose', 'version'], capture_output=True)
        except FileNotFoundError as e:
            raise SystemExit(f"missing docker compose dependency {e}")
        return docker_compose_dependency.returncode

    def spin_up_containers(self) -> int:
        from main import FillOutComposeFile
        compose_file_path = FillOutComposeFile.config_file_path
        docker_compose_up = subprocess.run(['docker', 'compose', '-f', f'{compose_file_path}', 'up', '-d'], capture_output=True)
        if docker_compose_up.returncode != 0:
            error_message = print(f"couldn't spin up containers due to: {docker_compose_up.stderr}")
            raise SystemExit(error_message)
        print('container/s are up')
        return docker_compose_up.returncode

    def inspect_containers(self) -> dict:
        running_containers_ids: list = docker_client.containers.list(all = True, sparse=True)
        containers_config: dict[str, Any] = {}
        for container in running_containers_ids:
            containers_config[container.attrs["Names"][0].lstrip('/')] = container.attrs
        return containers_config

    def are_all_containers_up(self, selected_services, running_containers_names) -> bool:
        not_spun_up_services = [service for service in selected_services if service not in running_containers_names]
        if not not_spun_up_services:
            return True
        error_message = print(f"containers weren't created for the following services: {not_spun_up_services}")
        return False

    @staticmethod
    def check_container_state_param(container_attributes: dict) -> bool:
        if container_attributes["State"] != "running":
            return False
        return True

    def are_all_containers_healthy(self, running_containers: dict) -> bool:
        unhealthy_containers = [container for container in running_containers if not self.check_container_state_param(running_containers[container])]
        if not unhealthy_containers:
            return True
        error_message = print(f"the following containers are not healthy: {unhealthy_containers}")
        return False


