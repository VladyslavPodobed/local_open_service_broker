import subprocess
import json
from models import Result
from container_runtime import ContainerRuntime


class DockerRuntime(ContainerRuntime):

    def spin_up_containers(self) -> Result:
        docker_compose_up = subprocess.run(['docker', 'compose', '-f', './generated/docker-compose.yml', 'up', '-d'], capture_output=True)
        if docker_compose_up.returncode != 0:
            print(f"couldn't spin up containers due to: {docker_compose_up.stderr}")
            return Result(success=False, error=f"couldn't spin up containers due to: {docker_compose_up.stderr}")
        else:
            print('container/s are up')
        return Result(success=True, return_value=docker_compose_up.returncode)

    def list_running_containers(self) -> Result:
        docker_ps = subprocess.run(['docker', 'ps', '--format', '{{json .}}'], capture_output=True, text=True)
        if docker_ps.returncode != 0:
            print(f"couldn't get container info due to: {docker_ps.stderr}")
            return Result(success=False, error=f"couldn't get info on running containers due to: {docker_ps.stderr}")
        else:
            return Result(success=True, return_value=json.dumps(json.loads(docker_ps.stdout), indent=5))

