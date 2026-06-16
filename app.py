import re

# why dict:
# in case more mappings r added,
dictionary_with_mappings: dict[str, bool] = {
    "postgresql_needed": False,
    "mysql_needed": False,
    "redis_needed": False,
    "nginx_needed": False
}

def prompt_to_select_needed_services():
    unfiltered_user_selected_services = input("""
Select the number of the respective service/s that you need:
    [1] - PostgreSQL
    [2] - MySQL
    [3] - Redis
    [4] - Nginx
e.g.
    if u need PostgreSQL - $: 1
    if u need PostgreSQL and MySQL - $: 1 2
""")

    filtered_user_selected_services = []
    unfiltered_user_selected_services = re.sub(r"[,.!+|\-=/?:;\'\\]", "", unfiltered_user_selected_services).split(" ")
    for i in unfiltered_user_selected_services:
        i = int(i)
        filtered_user_selected_services.append(i)
    # convert list into set to get unique values
    filtered_user_selected_services = list(set(filtered_user_selected_services))

    return filtered_user_selected_services



print(prompt_to_select_needed_services())


    # unfiltered_user_selected_services = unfiltered_user_selected_services.split(" ")
    # print(type(unfiltered_user_selected_services))
    # filtered_user_selected_services = []
    # for i in unfiltered_user_selected_services:

# print(prompt_to_select_needed_services(dictionary_with_mappings))
