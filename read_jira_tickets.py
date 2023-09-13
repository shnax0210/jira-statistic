import requests


class JiraTicketsReader:
    def __init__(self, login, password, jira_base_url, batch_size=50):
        self.login = login
        self.password = password
        self.jira_base_url = jira_base_url
        self.batch_size = batch_size

    def read_tickets(self, jql):
        with self.__create_session() as session:
            return self.__read_tickets(session, jql)

    def __create_session(self):
        session = requests.Session()
        session.auth = (self.login, self.password)
        return session

    def __add_url_prefix(self, relative_path):
        return self.jira_base_url + relative_path

    @staticmethod
    def __check_if_there_are_more_tickets_to_read(search_result):
        next_start_at = search_result['startAt'] + search_result['maxResults']
        return next_start_at < search_result['total'], next_start_at

    def __read_tickets(self, session, query):
        are_there_more_tickets_to_read = True
        start_at = 0

        while are_there_more_tickets_to_read:
            search_result = session.get(self.__add_url_prefix('/rest/api/latest/search'),
                                        params={'jql': query, "startAt": start_at,
                                                "maxResults": self.batch_size, "expand": "changelog"}).json()

            for ticket in search_result['issues']:
                yield ticket

            are_there_more_tickets_to_read, start_at = self.__check_if_there_are_more_tickets_to_read(search_result)
