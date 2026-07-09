import re
from typing import Any


class UserInput:
    def __init__(self) -> None:
        self.dictionary_with_mappings: dict[str, int] = {
            "postgresql": 1,
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
        self.dict_with_config_questions: dict[str, bool] = {
            # True is for inputs that must be int - done by the convert_str_to_int function and checked by the convert_str_to_int fucntion
            "Input port that should be open on the host: ": True,
            "Input port that should be open on the container: ": True, 
            "Input db's password: ": False
        }
        self.dict_with_selected_services_and_config: dict[str, dict[str, Any]] = {}


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


    def determine_selected_services(self, user_response: list[int], dictionary_with_mappings: dict[str, int]) -> list[str]:
        for key_in_dict in dictionary_with_mappings:
            for int_in_set in user_response:
                if int_in_set == dictionary_with_mappings.get(key_in_dict):
                    print(f"determine_selected_services returned: --- {key_in_dict}")
                    self.selected_services.append(key_in_dict)

        return self.selected_services


    def convert_str_to_int(self, string_being_converted: str, question_being_asked: str) -> int:
        while True:
            try:

                return int(string_being_converted)
            except ValueError:
                print("The value must contain just numbers (e.g. 1162)")
                string_being_converted = input(question_being_asked)


    def prompt_for_service_config(self, dict_of_config_question: dict[str, bool]) -> dict[str, Any]:
        dict_with_config: dict[str, Any] = {
            "HOST_PORT": "",
            "CONTAINER_PORT": "",
            "DB_PASSWORD": ""
        }
        for (question, key_in_final_dict) in zip(dict_of_config_question, dict_with_config):
            print(question)
            prompt_to_input_config = input("")
            if bool(dict_of_config_question[question]):
                prompt_to_input_config = self.convert_str_to_int(prompt_to_input_config, question)
            dict_with_config[key_in_final_dict] = prompt_to_input_config

        return dict_with_config


    def map_services_to_configs(self, services: list[str]) -> dict[str, dict[str, Any]]:
        for each_service in services:
            self.dict_with_selected_services_and_config[each_service] = self.prompt_for_service_config(self.dict_with_config_questions)

        return self.dict_with_selected_services_and_config


    def main(self):
        print(self.offered_services)
        selected_services = self.determine_selected_services(self.user_selects_services(), self.dictionary_with_mappings)
        self.map_services_to_configs(selected_services)


if __name__ == "__main__":
    UserInput().main()

