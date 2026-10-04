from dataclasses import dataclass
from enum import StrEnum


MANIFEST_FILE = "./generated/manifest.yml"


COMPOSE_FILE = "./generated/docker_compose.yml"
COMPOSE_NETWORK = "open_broker_network"


class ServiceName(StrEnum):
    POSTGRES = "postgres"
    MYSQL = "mysql"
    REDIS = "redis"
    NGINX = "nginx"


# gotta use it somehow
# assign Service.service_questions based on its value
class ServiceType(StrEnum):
    DB = "db"
    PROXY = "proxy"


@dataclass
class ServiceQuestion:
    question: str = ""
    must_be_int: bool = False
    config_key: str = ""


DB_QUESTIONS = [ServiceQuestion("What port should be open on host: ", True, "published"), ServiceQuestion("Input db password: ", False, "db_password")]
PROXY_QUESTIONS = []


@dataclass
class BaseServiceConfig:
    # have a bridge network to allow for port mappings in case a service's default port is already taken on host
    published: int = 0
    network: str = COMPOSE_NETWORK


@dataclass
class DBConfig(BaseServiceConfig):
    db_password: str = ""


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
    Service(
        1,
        ServiceName.POSTGRES,
        ServiceType.DB,
        DB_QUESTIONS,
        DBConfig(),
        """
    postgres:
        image: postgres:latest
        ports:
            - target: 5432
              published: {published}
        environment:
            POSTGRES_PASSWORD: "{db_password}"
        networks:
            - {network}
""",
    ),
    Service(
        2,
        ServiceName.MYSQL,
        ServiceType.DB,
        DB_QUESTIONS,
        DBConfig(),
        """
    mysql:
        image: mysql:latest
        ports:
            - target: 3306
              published: {published}
        environment:
            MYSQL_ROOT_PASSWORD: "{db_password}"
        networks:
            - {network}
""",
    ),
    Service(
        3,
        ServiceName.REDIS,
        ServiceType.DB,
        DB_QUESTIONS,
        DBConfig(),
        """
    redis:
        image: redis:latest
        ports:
            - target: 6379
              published: {published}
        # environment:
            # NOT_REAL_PASSWORD_ENV: "{db_password}"
        networks:
            - {network}
""",
    ),
    Service(
        4,
        ServiceName.NGINX,
        ServiceType.PROXY,
        PROXY_QUESTIONS,
        ProxyConfig(),
        """
    nginx:
        image: nginx:latest
        ports:
            - target: 80
              published: 80
            - target: 443
              published: 443
        networks:
            - {network}
""",
    ),
]
