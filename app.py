import re
import timeit

# why dict:
# in case more mappings r added,
dictionary_with_mappings: dict[str, bool] = {
    "postgresql_needed": False,
    "mysql_needed": False,
    "redis_needed": False,
    "nginx_needed": False
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


def user_selects_services():
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

    return print(selected_services_set)


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


def main():
    user_selects_services()


print(offered_services)
main()
