from falcon_client import utils
from falcon_client import api_client
from falcon_client import oauth2
from falcon_client import policies
from falcon_client import hosts
# from falcon_client import host_group
# from falcon_client import detects
# from falcon_client import real_time_response
# from falcon_client import iocs
import sys
import requests
import configparser

DEFAULT_CONFIG_SECTION = "falcon"
DEFAULT_LOG_LEVEL = "DEBUG"
DEFAULT_LOG_FORMAT = "%(asctime)s  %(levelname)s  %(module)s  %(message)s"


class FalconClient(api_client.APIClientMixin, oauth2.AuthMixin, hosts.HostsMixin, policies.PreventionPoliciesMixin):
    """
    CrowdStrike Falcon Query API Client

    'faclon_client' package can be used to perform various Falcon NGAV action using API.
    API documentation can be found at https://falcon.crowdstrike.com/support/documentation/2/query-api

    INSTALL
    -------
    $ pip install falcon_client

    USAGE
    -----
    > from falcon_client import FalconClient
    > fc = FalconClient(config="/path/to/config")
    or
    > fc = FalconClient.basic(client_id="QueryAPI clientID", client_key="QueryAPI Client Secret")
    > fc.login()

    Only Falcon administrator can issue a Query API client and secret.

    EXAMPLES
    --------
    # Login
    fc.login()

    # Device Search by filter (device scroll)
    hosts_resp = fc.device_scroll(fql_filter='platform_name: "Linux" + first_seen: >= "2019-10-11T00:00:00Z"')
    for host in hosts_resp:
        print(host)

    # Device Search
    hosts_resp = fc.device_search(limit=10, fql_filter='platform_name: "Windows"',  q="dubai")
    for host in hosts_resp:
        print(host)

    # Device Details
    hosts_resp = fc.device_details(['12e2f255382549d579ee10d56898d404', '64177fb5a1fd40f762b73c0abc8b9cd2'])
    or
    hosts_resp = fc.device_details(limit=10, fql_filter='platform_name: "Windows"',  q="FR-Rungis")
    for host in hosts_resp:
        print(json.dumps(host, indent=2))

    # Device Containment
    # aids = set(['7983795a198d40e75145aa18418aa385', 'fb8456dfe15d46607b4e08c9893e1a06'])
    for hosts in fc.device_details(list(aids)):
        for host in hosts:
            print(json.dumps(host['hostname'], indent=2))
    success, fail, err = fc.lift_containment(list(aids))
    print("Successfully lifted containment on %s" % ",".join(success)
    print("Failed to lifted containment on %s" % ",".join(fail)

    # Logout
    fc.logout()

    """
    def __init__(self, config=None, config_file_path='~/.crowdstrike/csfalcon.ini',
                 section=DEFAULT_CONFIG_SECTION, logger=None):
        """
        Initialize the Falcon Client.
        :param config_file_path: Path to configuration file.  Default '~/.crowdstrike/falcon.ini'
        :param section: Configuration file section containing API credentials.  Default 'falcon'.
        :param config: An instance of configparser.ConfigParser, which at a minimum should contain a
        DEFAULT_CONFIG_SECTION section and API Credentials.
        """
        if (logger is None) and (hasattr(logger, 'addHandler') is False):
            self.logger = utils.add_logger_streamhandler(logger_level=DEFAULT_LOG_LEVEL)
        else:
            self.logger = logger

        if config is None:
            try:
                _config_section = section
                self.config = utils.get_config(default_section=section,
                                               config_file=config_file_path)
            except Exception:
                raise
            else:
                self.config_file = config_file_path
        else:
            try:
                assert type(config) == configparser.ConfigParser
                _config_section = DEFAULT_CONFIG_SECTION
                self.config = config
            except Exception as err:
                sys.exit(err)

        # Get Credentials
        try:
            self.client_id = self.config.get(_config_section, 'client_id', raw=True)
            self.client_key = self.config.get(_config_section, 'client_key', raw=True)
            self.cache_creds = self.config.getboolean(_config_section, 'cache_creds', fallback=True, raw=True)
            self.logger.info("Client ID: %s, Client Key: %s..." % (self.client_id, self.client_key[0:8]))
        except Exception as err:
            sys.exit(err)

        # Set requests defaults
        self.req = requests.session()
        try:
            _proxy_host = self.config.get(_config_section, 'proxy_host', fallback=None, raw=True)
            _proxy_type = self.config.get(_config_section, 'proxy_type', fallback='http', raw=True)
            _proxy_port = self.config.getint(_config_section, 'proxy_port', fallback=8080, raw=True)
            if _proxy_host:
                self.req.proxies = {'http': '{}://{}:{}'.format(_proxy_type, _proxy_host, _proxy_port),
                                    'https': '{}://{}:{}'.format(_proxy_type, _proxy_host, _proxy_port)}
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                self.req.verify = False
        except Exception as err:
            self.logger.warning("Failed to set proxy. %s" % err)

        # Set api end-points
        self.BASE_URL = self.config.get(_config_section, 'base_url', fallback=r'https://api.crowdstrike.com', raw=True)
        self.req.headers = {'User-Agent': "python-api-wrapper", 'Authorization': ""}

    @classmethod
    def basic(cls, client_id, client_key, **kwargs):
        config = configparser.ConfigParser()
        config[DEFAULT_CONFIG_SECTION] = {'client_id': client_id, 'client_key': client_key}
        config._sections[DEFAULT_CONFIG_SECTION].update(kwargs)
        return cls(config)

    def __repr__(self):
        return "falcon_client::{}".format(self.client_id)

