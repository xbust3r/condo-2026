from urllib.parse import urlparse
import re

class URL:
    def __init__(self, url):
        self.url = url
        self.domain = self.get_domain()

    def get_domain(self):
        try:
            resultado = urlparse(self.url)
            dominio = resultado.netloc
            return dominio
        except Exception as e:
            print(f"Error: {e}")
            return None

    def is_valid(self):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return re.match(regex, self.url) is not None

