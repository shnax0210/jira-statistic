import argparse
import os

from collect_ticket_history import collect_ticket_history
from file_helpers import remove_file, save_to_csv_file
from read_jira_tickets import JiraTicketsReader

ap = argparse.ArgumentParser()

ap.add_argument("-u", "--url", required=True, help="Base url to jira")
ap.add_argument("-jql", "--jql", required=True, help="jql for tickets to gather statistic")
ap.add_argument("-r", "--result", required=True, help="Path to file where result should be written")
args = vars(ap.parse_args())

jira_user = os.environ['jiraUser']
jira_password = os.environ['jiraPassword']

jiraRider = JiraTicketsReader(jira_user, jira_password, args["url"], 200)

remove_file(args["result"])
for ticket in jiraRider.read_tickets(args["jql"]):
    save_to_csv_file(collect_ticket_history(ticket), args["result"])
