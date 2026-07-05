import re
from retry import retry


# why dict:
# in case more mappings r added,
dictionary_with_mappings: dict[str, int] = {
    "postgresql": 1,
    "mysql": 2,
    "redis": 3,
    "nginx": 4
}
selected_services: list[str] = []
offered_services = """
Select the number of the respective service/s that you need:
    [1] - PostgreSQL
    [2] - MySQL
    [3] - Redis
    [4] - Nginx
e.g.
    if u need PostgreSQL - $: 1
    if u need PostgreSQL and MySQL - $: 1 2
"""
dictinonary_with_config_questions: dict[str, bool] = {
    "Input port that should be open on the host: ": True,
    "Input port that should be open on the container: ": True, 
    "Input db's password: ": False
}


# the function is used in user_selects_services; it exists so that I can jsut add any number of services to the "offered_services" var
# knowing that the max number that will be accepted from user's input is not greater than the number belonging to the last service
# e.g. last service is Apache and has the number [100], if user input "101", that specific number will be ignored as there's no service with corresponding number
def determine_amount_of_offered_services(str_to_check):
    # "r" in the findall function declares RegEx patterns as raw string
    number_with_brackets = re.findall(r"\[.+\]", str_to_check)
    number_without_brackets: list = []
    for i in number_with_brackets:
        i = i.strip("[]")
        i = int(i)
        number_without_brackets.append(i)

    return number_without_brackets


def user_selects_services() -> set[int]:
    selected_services_str = input()
    selected_services_list = re.sub(r"a-z[,.!+|\-=/?:;\'\\]", "", selected_services_str).split(" ")
    selected_services_set = set()

    for i in selected_services_list:
        try:
            i = int(i)
            if i <= determine_amount_of_offered_services(offered_services)[-1]:
                selected_services_set.add(i)
        except ValueError:
            continue

    return selected_services_set


def determine_selected_services(user_response: set[int], dictionary_with_mappings: dict[str, int]) -> list[str]:
    global selected_services

    for key_in_dict in dictionary_with_mappings:
        for int_in_set in user_response:
            if int_in_set == dictionary_with_mappings.get(key_in_dict):
                print(f"determine_selected_services returned: --- {key_in_dict}")
                selected_services.append(key_in_dict)

    return selected_services
# I get a list containing names of selected services <- why do I need it?


@retry()
def convert_str_to_int(string_being_converted):
    var_of_correct_type_int = 0

    try:
        var_of_correct_type_int = int(string_being_converted)

        return var_of_correct_type_int

    except ValueError:
        if type(var_of_correct_type_int) is not int:
            print('ssdaddsadsasdasdasddas')



def user_inputs_config() -> dict:
    # for question in dict_being_iterated_over:
    #     var_of_type_int = input(question)
    #     var_of_type_int = convert_str_to_int(var_of_type_int)
    #     print(type(var_of_type_int))
    PORT_HOST = input("input port host")
    print(PORT_HOST)
    dict_with_config = {}
    dict_with_config.update({
        "PORT_HOST": PORT_HOST
        # "POST_CONTAINER": POST_CONTAINER,
        # "ENV_DB_PASSWORD": ENV_DB_PASSWORD
    })
    test = type(dict_with_config["PORT_HOST"])
    print(test)

    return dict_with_config["PORT_HOST"]

# user_inputs_config(dictinonary_with_config_questions)


def main():
    global dictionary_with_mappings
    determine_selected_services(user_selects_services(), dictionary_with_mappings)
    user_inputs_config()


# print(offered_services)
main()


