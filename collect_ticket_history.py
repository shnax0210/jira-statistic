from datetime import datetime

JIRA_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
TARGET_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"


def get_status(ticket):
    return ticket["fields"]["status"]["name"]


def get_assignee(ticket):
    if ticket["fields"]["assignee"]:
        return ticket["fields"]["assignee"]["displayName"]
    return None


def parse_jira_date(date):
    return datetime.strptime(date, JIRA_TIME_FORMAT).astimezone(
        datetime.now().astimezone().tzinfo)


def get_creation_time(ticket):
    return parse_jira_date(ticket["fields"]["created"])


watched_fields = [
    {
        "name": "status",
        "getCurrentValue": get_status
    },
    {
        "name": "assignee",
        "getCurrentValue": get_assignee
    }
]

all_watched_field_names = set([watched_field["name"] for watched_field in watched_fields])


def flat_map(list, func):
    return [item for sublist in list for item in func(sublist)]


def convert_raw_history_items(history):
    return [{"field": item["field"],
             "from": item["fromString"],
             "to": item["toString"],
             "time": parse_jira_date(history["created"])} for item in history["items"]]


def collect_raw_history_items(ticket):
    all_raw_history_items = flat_map(ticket["changelog"]["histories"], convert_raw_history_items)
    return [item for item in all_raw_history_items if item["field"] in all_watched_field_names]


def get_initial_value_of_watched_field(watched_field, ticket, raw_history_items):
    history_item = next((item for item in raw_history_items if item["field"] == watched_field["name"]),
                        None)
    if history_item:
        return history_item["from"]

    return watched_field["getCurrentValue"](ticket)


def build_initial_state(ticket, raw_history_items):
    result = {"key": ticket["key"]}

    for watched_field in watched_fields:
        result[watched_field["name"]] = get_initial_value_of_watched_field(watched_field, ticket, raw_history_items)
    result["startTime"] = get_creation_time(ticket)

    return result


def build_result_record(ticket_state, end_time):
    result_record = ticket_state.copy()
    result_record["startTime"] = ticket_state["startTime"].strftime(TARGET_TIME_FORMAT)
    result_record["endTime"] = end_time.strftime(TARGET_TIME_FORMAT)
    result_record["duration"] = (end_time - ticket_state["startTime"]).total_seconds() / (60 * 60)

    return result_record


def collect_ticket_history(ticket):
    result = []

    raw_history_items = collect_raw_history_items(ticket)
    current_ticket_state = build_initial_state(ticket, raw_history_items)

    for item in raw_history_items:
        result.append(build_result_record(current_ticket_state, item["time"]))

        current_ticket_state[item["field"]] = item["to"]
        current_ticket_state["startTime"] = item["time"]

    result.append(build_result_record(current_ticket_state, datetime.now().astimezone()))

    return result
