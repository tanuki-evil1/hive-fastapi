from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, NTLM
from app.config import settings


class ADClient:
    def __init__(self, username: str, password: str) -> None:
        self.server = Server(settings.AD_SERVER, get_info=ALL)
        self.username = username
        self.password = password

    def connect(self):
        return Connection(self.server, user=fr"Domain\{self.username}", password=self.password, authentication=NTLM)

    def get_user_data(self):
        with self.connect() as conn:
            conn.search(
                search_base=f'dc={settings.AD_DOMAIN},dc={settings.AD_SUFFIX}',
                search_filter=f'(sAMAccountName={self.username})',
                attributes=['givenName', 'sn', 'mail', 'name', 'sAMAccountName']
            )
            if conn.entries:
                return conn.entries[0].entry_attributes_as_dict
            return None

    def authenticate(self) -> bool:
        with self.connect() as conn:
            if conn.bind():
                return True
            return False
