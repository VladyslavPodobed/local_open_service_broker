import subprocess
import docker
from typing import Any
from models import Success, Failure
from container_runtime import ContainerRuntime


docker_client = docker.from_env()


class DockerRuntime(ContainerRuntime):

    def spin_up_containers(self) -> Success[int] | Failure:
        docker_compose_up = subprocess.run(['docker', 'compose', '-f', './generated/docker-compose.yml', 'up', '-d'], capture_output=True)
        if docker_compose_up.returncode != 0:
            print(f"couldn't spin up containers due to: {docker_compose_up.stderr}")
            return Failure(error_description = f"couldn't spin up containers due to: {docker_compose_up.stderr}")
        print('container/s are up')
        return Success(return_value = docker_compose_up.returncode)

    def inspect_containers(self) -> Success[dict] | Failure:
        running_containers_ids: list = docker_client.containers.list(all = True, sparse=True)
        containers_config: dict[str, Any] = {}
        for container in running_containers_ids:
            # removed redundant code here
            # var was literally useless = container_attrs = container.attrs
            containers_config[container.attrs["Names"][0].lstrip('/')] = container.attrs
        return Success(return_value = containers_config)

    def are_all_containers_up(self, selected_services, running_containers_names) -> Success | Failure:
        not_spun_up_services = [service for service in selected_services if service not in running_containers_names]
        if not not_spun_up_services:
            return Success(return_value=True)
        return Failure(error_description=f"containers weren't created for the following services: {not_spun_up_services}")


    def are_all_containers_healthy(self, ):
        # check "State"
        pass
        
