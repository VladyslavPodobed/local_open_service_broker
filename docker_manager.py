import subprocess
from dataclasses import dataclass
from typing import Any


@dataclass
class Result:
    success: bool;
    return_value: Any | None = None
    error: str | None = None
        

class GeneralPurposeFunctions:

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_line_from_stdout(line_number: int) -> Result:
        sed = subprocess.run(['sed', '-n', f'{line_number}p'], capture_output=True)
        if sed.returncode != 0:
            return Result(success=False, error=f"couldn't get line number {line_number} due to: {sed.stderr}")
        else:
            return Result(success=True, return_value=sed.stdout)


class DockerManager:

    def __init__(self) -> None:
        pass
    
    @staticmethod
    def spin_up_containers() -> Result:
        docker_compose_up = subprocess.run(['docker', 'compose', '-f', './generated/docker-compose.yml', 'up', '-d'], capture_output=True)
        if docker_compose_up.returncode != 0:
            print(f"container/s couldn't be created due to: {docker_compose_up.stderr}")
            return Result(success=False, error=f"couldn't spin up containers due to: {docker_compose_up.stderr}")
        else:
            print('container/s are up')
        return Result(success=True, return_value=docker_compose_up.returncode)

    @staticmethod
    def get_container_info() -> Result:
        docker_ps = subprocess.run(['docker', 'ps'], capture_output=True)
        if docker_ps.returncode != 0:
            print(f"couldn't get container info due to: {docker_ps.stderr}")
            return Result(success=False, error=f"couldn't get info on running containers due to: {docker_ps.stderr}")
        else:
            return Result(success=True, return_value=docker_ps.stdout)


    


# how to check if containers were spun up
    # docker_compose_up.returncode != 0       <------       done
# how do I output info on each container
    # iterate over each line with "sed" somehow?
    # pass list of selected services from main.py, iterate over it n get line that contains service name for each iteration?
    #
