import re
from dataclasses import dataclass
from enum import StrEnum
# from docker_runtime import DockerRuntime


COMPOSE_FILE = "./generated/docker_compose.yml"
COMPOSE_NETWORK = "open_broker_network"

class ServiceName(StrEnum):
    POSTGRES = 'postgres'
    MYSQL = 'mysql'
    REDIS = 'redis'
    NGINX = 'nginx'


# gotta use it somehow
  # assign Service.service_questions based on its value
class ServiceType(StrEnum):
    DB = 'db'
    PROXY = 'proxy'


@dataclass
class ServiceQuestion:
    question: str = ''
    must_be_int: bool = False
    config_key: str = ''
DB_QUESTIONS = [
    ServiceQuestion('What port should be open on host: ', True, 'published_port'),
    ServiceQuestion('Input db password: ', False, 'db_password')
]
PROXY_QUESTIONS = [
]


@dataclass
class BaseServiceConfig:
    # have a bridge network to allow for port mappings in case a service's default port is already taken on host
    published_port: int = 0
    network:str = COMPOSE_NETWORK
@dataclass
class DBConfig(BaseServiceConfig):
    db_password: str = ''
@dataclass
class ProxyConfig(BaseServiceConfig):
    pass


@dataclass
class Service[ServiceConfig: BaseServiceConfig]:
    service_id: int
    service_name: ServiceName
    service_type: ServiceType
    service_questions: list[ServiceQuestion]
    service_config: ServiceConfig
    service_compose: str


services: list[Service] = [
    Service(1, ServiceName.POSTGRES, ServiceType.DB, DB_QUESTIONS, DBConfig(), """
    postgres:
        image: postgres:latest
        ports:
            - target_port: 5432
              published_port: {published_port}
        environment:
            POSTGRES_PASSWORD: "{db_password}"
        networks:
            - {network}:
"""),
    Service(2, ServiceName.MYSQL, ServiceType.DB, DB_QUESTIONS, DBConfig(), """
    mysql:
        image: mysql:latest
        ports:
            - target_port: 3306
              published_port: {published_port}
        environment:
            MYSQL_ROOT_PASSWORD: "{db_password}"
        networks:
            - {network}:
"""),
    Service(3, ServiceName.REDIS, ServiceType.DB, DB_QUESTIONS, DBConfig(), """
    redis:
        image: redis:latest
        ports:
            - target_port: 6379
              published_port: {published_port}
        # environment:
            # NOT_REAL_PASSWORD_ENV: "{db_password}"
        networks:
            - {network}:
"""),
    Service(4, ServiceName.NGINX, ServiceType.PROXY, PROXY_QUESTIONS, ProxyConfig(), """
    nginx:
        image: nginx:latest
        ports:
            - target_port: 80
              published_port: 80
            - target_port: 443
              published_port: 443
        networks:
            - {network}:
""")
]


def create_initial_message():
    message = "Select the number of the respective service/s that you need:"
    for service in services:
        message += f"\n[{service.service_id}] - {service.service_name}"
    message += f"""
e.g.
if u need {services[0].service_name} - $: {services[0].service_id}
if u need {services[0].service_name} {services[1].service_name} - $: {services[0].service_id} {services[1].service_id}"""
    return message
print(create_initial_message())


def prompt() -> list[Service]:
    provided_input = input()
    extracted_ids = remove_non_numbers(provided_input)
    valid_services = selected_services_exist(extracted_ids)
    return valid_services

def remove_non_numbers(provided_input) -> list[int]:
    try:
        provided_input = re.sub('\.|\?|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\-|\_|\+|\=|\;|\:|\'|\"|\{|\}|\[|\|\<|\>|\`|\~|\\\|\/|\|', ',', provided_input)
        provided_input = re.sub('[a-z]', '', provided_input)
        provided_input = re.sub(',', ' ', provided_input).split()
        provided_input = sorted(list(set(provided_input)))
        provided_input = [int(i) for i in provided_input if int(i)]
        if not provided_input:
            print("ccccan't understand your input, enter only numbers: ")
            prompt()
    except:
        print("can't understand your input, enter only numbers: ")
        prompt()
    return provided_input

all_service_ids = [service.service_id for service in services if service.service_id]

def selected_services_exist(provided_service_ids: list[int]) -> list[Service]:
    chosen_services: list[Service] = [service for service in services if service.service_id in provided_service_ids]
    if not chosen_services:
        print("none of the provided ids are valid, enter valid ids")
        prompt()
    non_existing_service_ids: list[int] = [id for id in provided_service_ids if id not in all_service_ids]
    if non_existing_service_ids:
        print(f"didn't find services with corresponding id's: {non_existing_service_ids}")
    print("services you selected:" + ", ".join([service.service_name for service in chosen_services]))
    # print(f"+ {chosen_services}")
    # print(f"- {non_existing_service_ids}")
    return chosen_services


def ask(service: Service):
    for question in service.service_questions:
        while True:
            answer = input(f"{service.service_name}: {question.question}")
            if not answer:
                print("can't have blank response, try again")
            elif question.config_key and not answer.isdigit():
                print("enter only numbers")
            else:
                setattr(service.service_config, question.config_key, answer)
                break
    # print(service.service_config)


def compose_service_keyword():
    with open(COMPOSE_FILE, "w") as compose_file:
        compose_file.write("services:")

def compose_service_block(service: Service):
    with open(COMPOSE_FILE, "a") as compose_file:
        # asdict is very slow - will use __dict__ instead
        # copy call to avoid mutation
        config = service.service_config.__dict__.copy()
        compose_file.write(service.service_compose.format(**config))


if __name__ == "__main__":
    compose_service_keyword()
    selected_services: list[Service] = prompt()
    for service in selected_services:
        ask(service)
        compose_service_block(service)
