import re
import argparse
from config import *
from docker_runtime import DockerRuntime
# from k3s_orchestration import K3sRuntime


parser = argparse.ArgumentParser()
one_arg = parser.add_mutually_exclusive_group()
one_arg.add_argument("-d", "--docker-compose", action="store_true")
one_arg.add_argument("-k", "--k3s", action="store_true")
cli_args = parser.parse_args()


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
        provided_input = re.sub("\.|\?|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\-|\_|\+|\=|\;|\:|'|\"|\{|\}|\[|\|\<|\>|\`|\~|\\\|\/|\|", ",", provided_input)
        provided_input = re.sub("[a-z]", "", provided_input)
        provided_input = re.sub(",", " ", provided_input).split()
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


def compose_network_block():
    with open(COMPOSE_FILE, "a") as compose_file:
        compose_file.write(f"""
networks:
    {COMPOSE_NETWORK}:
        driver: bridge""")


def determine_runtime_engine(cli_arg):
    if cli_arg.docker_compose:
        return DockerRuntime()
    # return K3sRuntime()


def main():
    runtime = determine_runtime_engine(cli_args)
    DockerRuntime()
    compose_service_keyword()
    selected_services: list[Service] = prompt()
    for service in selected_services:
        ask(service)
        compose_service_block(service)
    compose_network_block()
    # runtime.main()
    DockerRuntime().main()


if __name__ == "__main__":
    main()
