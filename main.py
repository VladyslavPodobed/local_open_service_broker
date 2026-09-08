import re
import argparse
import subprocess
from typing import Any
from container_runtime import ContainerRuntime
from docker_runtime import DockerRuntime


class UserInput:

    def __init__(self) -> None:
        self.service_to_number_mappings: dict[str, int] = {
            "postgres": 1,
            "mysql": 2,
            "redis": 3,
            "nginx": 4
        }
        self.selected_services: list[str] = []
        self.offered_services = """
        Select the number of the respective service/s that you need:
            [1] - PostgreSQL
            [2] - MySQL
            [3] - Redis
            [4] - Nginx
        e.g.
            if u need PostgreSQL - $: 1
            if u need PostgreSQL and MySQL - $: 1 2
        """
        self.config_questions: dict[str, bool] = {
            # True is for inputs that must be int - done by the convert_str_to_int function and checked by the convert_str_to_int fucntion
            "Input port that should be open on the host: ": True,
            "Input port that should be open on the container: ": True,
            "Input db's password: ": False
        }
        self.selected_services_and_config: dict[str, dict[str, Any]] = {}

    # the function is used in user_selects_services; it exists so that I can jsut add any number of services to the "offered_services" var
    # knowing that the max number that will be accepted from user's input is not greater than the number belonging to the last service
    # e.g. last service is Apache and has the number [100], if user input "101", that specific number will be ignored as there's no service with corresponding number
    def count_number_of_offered_services(self, str_to_check: str) -> list[int]:
        # "r" in the findall function declares RegEx patterns as raw string
        number_with_brackets = re.findall(r"\[.+\]", str_to_check)
        number_without_brackets: list = []
        for i in number_with_brackets:
            i = i.strip("[]")
            i = int(i)
            number_without_brackets.append(i)
        return number_without_brackets

    def user_selects_services(self) -> list[int]:
        selected_services_str = input()
        selected_services_list = re.sub(r"a-z[,.!+|\-=/?:;\'\\]", "", selected_services_str).split(" ")
        selected_services_set = set()
        for i in selected_services_list:
            try:
                i = int(i)
                if i <= self.count_number_of_offered_services(self.offered_services)[-1]:
                    selected_services_set.add(i)
            except ValueError:
                continue
        selected_services_list = list(selected_services_set)
        return selected_services_list

    def determine_selected_services(self, user_response: list[int], service_to_number_mappings: dict[str, int]) -> list[str]:
        for key_in_dict in service_to_number_mappings:
            for selected_service_number in user_response:
                if selected_service_number == service_to_number_mappings.get(key_in_dict):
                    # print(f"determine_selected_services returned: --- {key_in_dict}")
                    self.selected_services.append(key_in_dict)
        return self.selected_services

    def convert_str_to_int(self, string_being_converted: str, question_being_asked: str) -> int:
        while True:
            try:
                return int(string_being_converted)
            except ValueError:
                print("The value must contain just numbers (e.g. 1162)")
                string_being_converted = input(question_being_asked)

    def prompt_for_service_config(self, config_questions: dict[str, bool], service: str) -> dict[str, Any]:
        config: dict[str, Any] = {
            "HOST_PORT": "",
            "CONTAINER_PORT": "",
            "DB_PASSWORD_VALUE": ""
        }
        for (question, key_in_final_dict) in zip(config_questions, config):
            print(f"{service} - {question}")
            prompt_to_input_config = input("")
            if bool(config_questions[question]):
                prompt_to_input_config = self.convert_str_to_int(prompt_to_input_config, question)
            config[key_in_final_dict] = prompt_to_input_config
        return config

    def map_services_to_configs(self, services: list[str]) -> dict[str, dict[str, Any]]:
        print(services)
        for each_service in services:
            self.selected_services_and_config[each_service] = self.prompt_for_service_config(self.config_questions, each_service)
        return self.selected_services_and_config

    def main(self):
        print(self.offered_services)
        selected_services = self.determine_selected_services(self.user_selects_services(), self.service_to_number_mappings)
        self.map_services_to_configs(selected_services)
        return self.selected_services_and_config


class FillOutComposeFile:

    # should be a class var instead of instance var as I expect the var to have the same value across all instances
    # must be defined before "__init__"
    config_file_path = "./generated/docker_compose.yml"

    compose_network = "observability_network"
    
    def __init__(self) -> None:
        pass

    def first_line_in_compose_file(self) -> None:
        try:
            with open(self.config_file_path, "w") as compose_file:
                compose_file.write("services:")
        except FileNotFoundError as e:
            raise SystemExit(f"couldn't find docker-compose.yml in './generated/': {e}")

    def postgres_compose(self, SERVICE_NAME: str, HOST_PORT: int, CONTAINER_PORT: int, DB_PASSWORD_VALUE: str) -> str:
        return f"""
    {SERVICE_NAME}:
        image: {SERVICE_NAME}:latest
        container_name: '{SERVICE_NAME}'
        restart: on-failure
        ports:
            - "127.0.0.1:{HOST_PORT}:{CONTAINER_PORT}"
        environment:
            POSTGRES_PASSWORD: '{DB_PASSWORD_VALUE}'
        networks:
            - {self.compose_network}
"""

    def mysql_compose(self, SERVICE_NAME: str, HOST_PORT: int, CONTAINER_PORT: int, DB_PASSWORD_VALUE: str) -> str:
        return f"""
    {SERVICE_NAME}:
        image: {SERVICE_NAME}:latest
        container_name: '{SERVICE_NAME}'
        restart: on-failure
        ports:
            - "127.0.0.1:{HOST_PORT}:{CONTAINER_PORT}"
        environment:
            MYSQL_ROOT_PASSWORD: '{DB_PASSWORD_VALUE}'
        networks:
            - {self.compose_network}
"""

    def define_compose_network(self):
        with open(self.config_file_path, "a") as compose_file:
            compose_file.write(f"""
networks:
    {self.compose_network}:
        driver: bridge
""")
        
    def fill_out_compose_file(self, services_and_config: dict[str, dict[str, Any]]) -> str:
        for service in services_and_config:
            if service == 'postgres':
                config = services_and_config[service]
                with open(self.config_file_path, "a") as compose_file:
                    compose_file.write(self.postgres_compose(
                        SERVICE_NAME=f"{service}",
                        HOST_PORT=config["HOST_PORT"],
                        CONTAINER_PORT=config["CONTAINER_PORT"],
                        DB_PASSWORD_VALUE=config["DB_PASSWORD_VALUE"])
                    )
            elif service == 'mysql':
                config = services_and_config[service]
                with open(self.config_file_path, "a") as compose_file:
                    compose_file.write(self.mysql_compose(
                        SERVICE_NAME=f"{service}",
                        HOST_PORT=config["HOST_PORT"],
                        CONTAINER_PORT=config["CONTAINER_PORT"],
                        DB_PASSWORD_VALUE=config["DB_PASSWORD_VALUE"])
                    )


class Observability:
    def __init__(self) -> None:
        pass

    def spin_up_observability(self):
        docker_compose_up = subprocess.run(['docker', 'compose', '-p', 'generated', 'up', '-d'], capture_output=True)
        if docker_compose_up.returncode != 0:
            raise SystemExit("couldn't spin up the observability stack containers")
        print('observability stack is up')


services_and_config = None


parser = argparse.ArgumentParser()
unique_arg = parser.add_mutually_exclusive_group()
unique_arg.add_argument('-d', '--docker', action='store_true')
unique_arg.add_argument('-p', '--podman', action="store_true")
cli_args = parser.parse_args()

runtime: ContainerRuntime = DockerRuntime()

if __name__ == "__main__":
    services_and_config = UserInput().main()
    build_docker_template = FillOutComposeFile()
    build_docker_template.first_line_in_compose_file()
    build_docker_template.fill_out_compose_file(services_and_config)
    build_docker_template.define_compose_network()
    Observability().spin_up_observability()
    runtime.verify_dependency()
    runtime.spin_up_containers()
    spun_up_containers_and_attributes = runtime.inspect_containers()
    runtime.are_all_containers_up(services_and_config, spun_up_containers_and_attributes)
    runtime.are_all_containers_healthy(spun_up_containers_and_attributes)

