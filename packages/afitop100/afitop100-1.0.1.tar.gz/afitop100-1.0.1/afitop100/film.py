from dataclasses import dataclass


@dataclass
class Film:
    """Class to hold film data. AFI List is not updated often, but as new rankings come out, we will need to add new
    attributes for each year. We may want to abstract this to make things scalable."""

    title: str
    release_year: int
    director: str
    afi_rank_1998: int
    afi_rank_2007: int
    rank_delta: int

    def __setattr__(self, name, value) -> None:
        """The year-rank is not assured to be an integer, so do some input checking and convert as needed"""
        if name == "afi_rank_1998" or name == "afi_rank_2007":
            if self.is_int_str(value):
                self.__dict__[name] = int(value)
            else:
                self.__dict__[name] = None
        else:
            self.__dict__[name] = value

    def __getitem__(self, key):
        """This makes the Film class subscriptable"""
        return getattr(self, key)

    def is_int_str(self, s: str) -> bool:
        """Determine if the given string can be represented as an integer"""
        try:
            int(s)
            return True
        except ValueError:
            return False
