# afitop100
## AFI Top 100  

**Requirements**  
Tested under python version 3.8.2+  
YMMV with older versions

---  

The [AFI Top 100 movies of all time](https://www.afi.com/afis-100-years-100-movies/) is a movie ranking list by the [American Film Institute](https://www.afi.com/about-afi/).  

This package will scrape the [Wikipedia page](https://en.wikipedia.org/wiki/AFI%27s_100_Years...100_Movies) via the Wikipedia API that contains the AFI listing and make the data avaialble as structured data.  

As of the writing of this README, there are two lists avaialbe. The list published in 1998 and the list that was updated in 2007. This package will grab both of these lists and provide the following data fields from the film.py dataclass:  

- title: str
- release_year: int
- director: str
- afi_rank_1998: int or None
- afi_rank_2007: int or None
- rank_delta: int or None  
  
Take a look at the unittests in afitop100/test for some examples on how to consume the modules in this package and/or see the documentation below.
  
---
*CLI Usage Example:*  
afitop100 *[optional switches]*  
  
**Year:**  
Default: **all** films from **both** 1998 and 2007  
-y 1998 -> Only return films from the 1998 list  
-y 2007 -> Only return films from the 2007 list  
  
**Output:**  
Default: json  
-o json -> return the list as pretty printed json  
-o csv -> return the list in a csv format  

---
*Library Usage Example:*  
```
from afitop100 import AFITop100
"""
Get the AFI Top 100 List data in json format
"""
afi = AFITop100()               # instance of the AFITop100 Client
afi.scrape_afi_list()           # scrape the AFI Top 100 from Wikipedia
print(afi.get_afi_list_json())  # pretty print the list
```

