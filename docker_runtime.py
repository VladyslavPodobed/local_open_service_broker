import subprocess
import docker
import json
from typing import Any
from models import Result
from container_runtime import ContainerRuntime


docker_client = docker.from_env()


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
        running_containers: list = docker_client.containers.list(all = True, sparse=True)
        return Result(success=True, return_value=running_containers)

    def inspect_containers(self) -> Result:
        containers_config: dict[str, Any] = {}
        for container in self.list_running_containers().return_value:
            container_attrs = container.attrs
            # e.g. of ouput of "container.attrs":
# {
#      "postgres": {
#           "Id": "0e48249c061f43d646e5953e12250a4f5d3e0702abfa3f54906a95f386e71b83",
#           "Names": [
#                "/postgres"
#           ],
#           "Image": "postgres:latest",
#           "ImageID": "sha256:06cad38a5d9f5d24b4d83d86def30795d5e4b757fedbf5281172b576dedcd941",
#           "ImageManifestDescriptor": {
#                "mediaType": "application/vnd.oci.image.manifest.v1+json",
#                "digest": "sha256:cd78ca58eb75f929698e117a589488ccb2bd45107247fe02400b50ff6c418324",
#                "size": 3439,
#                "annotations": {
#                     "com.docker.official-images.bashbrew.arch": "amd64",
#                     "org.opencontainers.image.base.digest": "sha256:38a76d01668772e381ad2826d876627c89e7133e2f8a0f5d567306798b0f2a16",
#                     "org.opencontainers.image.base.name": "debian:trixie-slim",
#                     "org.opencontainers.image.created": "2026-08-13T19:14:26Z",
#                     "org.opencontainers.image.revision": "e00e1bd34ec5c8a8e7ad89b273b3d42efaf6d5bc",
#                     "org.opencontainers.image.source": "https://github.com/docker-library/postgres.git#e00e1bd34ec5c8a8e7ad89b273b3d42efaf6d5bc:18/trixie",
#                     "org.opencontainers.image.url": "https://hub.docker.com/_/postgres",
#                     "org.opencontainers.image.version": "18.6"
#                },
#                "platform": {
#                     "architecture": "amd64",
#                     "os": "linux"
#                }
#           },
#           "Command": "docker-entrypoint.sh postgres",
#           "Created": 1787507237,
#           "Ports": [
#                {
#                     "IP": "127.0.0.1",
#                     "PrivatePort": 1191,
#                     "PublicPort": 1191,
#                     "Type": "tcp"
#                }
#           ],
#           "Labels": {
#                "com.docker.compose.config-hash": "65f2cd827985ab7055ce6d477d908d760676b44bacbff80b2b851e6f348057fd",
#                "com.docker.compose.container-number": "1",
#                "com.docker.compose.depends_on": "",
#                "com.docker.compose.image": "sha256:06cad38a5d9f5d24b4d83d86def30795d5e4b757fedbf5281172b576dedcd941",
#                "com.docker.compose.oneoff": "False",
#                "com.docker.compose.project": "generated",
#                "com.docker.compose.project.config_files": "/home/uuser/platform_engineering_project/generated/docker-compose.yml",
#                "com.docker.compose.project.working_dir": "/home/uuser/platform_engineering_project/generated",
#                "com.docker.compose.service": "postgres",
#                "com.docker.compose.version": "2.40.3",
#                "desktop.docker.io/ports.scheme": "v2",
#                "desktop.docker.io/ports/1191/tcp": "127.0.0.1:1191",
#                "desktop.docker.io/wsl-distro": "Ubuntu"
#           },
#           "State": "running",
#           "Status": "Up Less than a second",
#           "HostConfig": {
#                "NetworkMode": "generated_default"
#           },
#           "NetworkSettings": {
#                "Networks": {
#                     "generated_default": {
#                          "IPAMConfig": null,
#                          "Links": null,
#                          "Aliases": null,
#                          "MacAddress": "b3:52:a2:ba:b5:7a",
#                          "DriverOpts": null,
#                          "GwPriority": 0,
#                          "NetworkID": "845c058fe849683d9e4d92440b3845ed078cf527ea072951fb433c629b4ba728",
#                          "EndpointID": "66be1217fdb19b025eb09d7cabcfad030c910b3485aa8711738caa4f29568bf7",
#                          "Gateway": "172.18.0.1",
#                          "IPAddress": "172.18.0.2",
#                          "IPPrefixLen": 16,
#                          "IPv6Gateway": "",
#                          "GlobalIPv6Address": "",
#                          "GlobalIPv6PrefixLen": 0,
#                          "DNSNames": null
#                     }
#                }
#           },
#           "Mounts": [
#                {
#                     "Type": "volume",
#                     "Name": "24c736685e9325736ac11b3a25be80dda70271dfc536af0aff4a6ee71372cad1",
#                     "Source": "",
#                     "Destination": "/var/lib/postgresql",
#                     "Driver": "local",
#                     "Mode": "",
#                     "RW": true,
#                     "Propagation": ""
#                }
#           ]
#      },
#      "mysql": {
#           "Id": "55029c874290ba4d74ff171198f6a8a041054844ae38a1f4dea3ff2746e5c566",
#           "Names": [
#                "/mysql"
#           ],
#           "Image": "mysql:latest",
#           "ImageID": "sha256:66aec17cd21a956029b83f083b813073859e8355dc1a00e55df6ba02f0e32345",
#           "ImageManifestDescriptor": {
#                "mediaType": "application/vnd.oci.image.manifest.v1+json",
#                "digest": "sha256:973c5e8e4d2f12ecc3da9ca9d8d4189b6a7e3d17584c66fca6dae6993c0417ed",
#                "size": 2864,
#                "annotations": {
#                     "com.docker.official-images.bashbrew.arch": "amd64",
#                     "org.opencontainers.image.base.digest": "sha256:431feabc43183b2f10e1401b0dfd504d8bbd32a851824c137a3e7a334fc054c8",
#                     "org.opencontainers.image.base.name": "oraclelinux:9-slim",
#                     "org.opencontainers.image.created": "2026-07-27T22:06:36Z",
#                     "org.opencontainers.image.revision": "288e46ff450920468d5a1fcb618d359068704c3d",
#                     "org.opencontainers.image.source": "https://github.com/docker-library/mysql.git#288e46ff450920468d5a1fcb618d359068704c3d:innovation",
#                     "org.opencontainers.image.url": "https://hub.docker.com/_/mysql",
#                     "org.opencontainers.image.version": "26.7.0"
#                },
#                "platform": {
#                     "architecture": "amd64",
#                     "os": "linux"
#                }
#           },
            ...
#      }
# }
            containers_config[container_attrs["Names"][0].lstrip('/')] = container_attrs
        return Result(success=True, return_value=containers_config)

    def are_all_containers_up(self, selected_services: list[str]) -> Result:
        pass
            

    def are_all_containers_healthy(self):
        pass


