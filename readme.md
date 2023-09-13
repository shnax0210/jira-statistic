# Utility to gather jira data regarding tickets and their changes

## How to run

- install python 3.9
- install dependencies: pip3 install -r requirements.txt
- Set "jiraUser" and "jiraPassword" env variables with real jira user and password that has access to needed tickets
- Run `python3 jira-statistic-cmd-adapter.py -u "https://base-jira-url.com" -jql "some jql" -r "result.csv"`

Notes: replace env variables and script parameters with real value

Arguments description:

- "-u" - base jira url
- "-jql" - jql to gather statistic for
- "-r" - path to file where result should be put