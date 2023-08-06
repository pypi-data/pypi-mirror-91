"""AFI Top 100 Liste Generator for Python
>>> from afitop100 import AFITop100
>>> afi = AFITop100()
>>> afi.scrape_afi_list()
>>> print(afi.get_afi_list_json())
"""

__version__ = "0.1.0"

from .afi import AFITop100
