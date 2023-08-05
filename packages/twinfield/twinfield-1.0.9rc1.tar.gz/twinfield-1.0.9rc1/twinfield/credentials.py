import logging
from xml.etree import ElementTree as ET
import os
import requests
from . import templates
from .exceptions import EnvironmentVariablesError


def twinfield_login():
    """
    Returns
    -------
    login
        class SessionParameters with credentials from environment
    """
    user = os.environ.get("TW_USER_LS")
    password = os.environ.get("TW_PW_LS")
    organisation = os.environ.get("TW_ORG_LS")

    login = SessionParameters(user=user, pw=password, organisation=organisation)

    logging.debug(f"ingelogd met gebruiker {user}")

    return login


class SessionParameters:
    def __init__(self, user: str, pw: str, organisation: str):
        """
        Parameters
        ----------
        user: str
            username of twinfield
        pw: str
            twinfield password
        organisation: str
            twinfield organisation
        """

        self.user = user
        self.password = pw
        self.organisation = organisation
        self.check_environment_variables()

        self.url = "https://login.twinfield.com/webservices/session.asmx"
        self.header = {"Content-Type": "text/xml", "Accept-Charset": "utf-8"}

        self.ns = {
            "env": "http://schemas.xmlsoap.org/soap/envelope/",
            "tw": "http://www.twinfield.com/",
        }

        self.ns_txt = {k: "{" + v + "}" for k, v in self.ns.items()}

        self.body = templates.import_xml(
            os.path.join("xml_templates", "template_login.xml")
        ).format(user, pw, organisation)
        self.session_id, self.cluster = SessionParameters.get_session_info(
            self, self.url, self.header, self.body
        )

    def parse_session_id(self, root) -> str:
        """
        Parameters
        ----------
        root
            root level of soap login response

        Returns
        -------
        session_id: str
            session_id needed for every twinfield request.
        """

        header = root.find("env:Header/tw:Header", self.ns)
        session_id = header.find("tw:SessionID", self.ns).text
        logging.debug(f"session id: {session_id}")

        return session_id

    def parse_cluster(self, root):
        """

        Parameters
        ----------
        root: root level of soap login response

        Returns: cluster of twinfield endpoint
        -------

        """

        header = root.find("env:Body/tw:LogonResponse", self.ns)
        cluster = header.find("tw:cluster", self.ns).text
        cluster = cluster.split("https://")[1].split(".twinfield.com")[0]
        logging.debug(f"cluster: {cluster}")

        return cluster

    def get_session_info(self, url, header, body) -> list:
        """

        Parameters
        ----------
        url
            twinfield endpoint for getting a new session
        header
            headers to be send in request
        body
            soap message as body

        Returns
        -------
        session id and cluster
        """

        response = requests.post(url=url, headers=header, data=body)

        if response:
            session_id = SessionParameters.parse_session_id(
                self, root=ET.fromstring(response.text)
            )  # lees de response uit
            cluster = SessionParameters.parse_cluster(
                self, root=ET.fromstring(response.text)
            )  # lees de response uit

        else:
            session_id, cluster = None, None
            logging.info("niet gelukt om data binnen te halen")

        return [session_id, cluster]

    def check_environment_variables(self):
        # Test if environment variables are set for Twinfield login

        if not all([self.user, self.password, self.organisation]):
            raise EnvironmentVariablesError(
                "One of the environment variables TW_USERS_LS, TW_PW_LS, TW_ORG_LS is not set"
            )
