import requests

BASE_URL = "https://en.wikipedia.org"


class Wikipedia:
    """
    Retrieve a wikipedia page or section and return it in json format
    """

    def __init__(self, **kwargs: dict):
        if kwargs.get("url"):
            self.base_url = kwargs["url"]
        else:
            self.base_url = BASE_URL

    def get_wikipedia_page(self, page: str, **kwargs: dict) -> dict:
        """Given a wikipedia page, return a json represnetation of the page and the section if one is given."""

        headers = (
            {"User-Agent": kwargs["user_agent"]} if kwargs.get("user_agent") else {"User-Agent": "vscode-restclient"}
        )

        querystring = {"action": "parse", "format": "json", "page": page, "prop": "text", "formatversion": "2"}
        if kwargs.get("section"):
            querystring["section"] = kwargs["section"]

        r = requests.request("GET", f"{self.base_url}/w/api.php", headers=headers, params=querystring)
        return r.json()
