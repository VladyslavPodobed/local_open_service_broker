import subprocess


class ComposeDown:
    def __init__(self) -> None:
        pass

    def observability_compose_down(self):
        compose_down = subprocess.run(['docker', 'compose', '-p', 'generated', 'down', '-v'], capture_output=True)

    def services_compose_down(self):
        compose_down = subprocess.run(['docker', 'compose', '-p', 'generated', '-f', './generated/docker_compose.yml', 'down'], capture_output=True)


class CheckIfDown:
    def __init__(self) -> None:
        pass

    def is_observability_down(self):
        pass


def main():
    compose_down = ComposeDown()
    compose_down.observability_compose_down()
    compose_down.services_compose_down()

main()

