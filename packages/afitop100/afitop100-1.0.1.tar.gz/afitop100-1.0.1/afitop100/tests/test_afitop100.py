from unittest import TestCase
from afitop100.afi import AFITop100
import json

FILM_TITLE = "Citizen Kane"


class TestAFITop100(TestCase):
    def setUp(self):
        self.afitop100 = AFITop100()
        self.afitop100.scrape_afi_list()

    def test_get_top_100_of_all_time(self):
        self.assertGreater(len(self.afitop100.afi_list), 99)

    def test_get_afi_list_by_year(self):
        afi_1998 = self.afitop100.get_afi_list_by_year(1998)
        afi_2007 = self.afitop100.get_afi_list_by_year(2007)
        self.assertEqual(len(afi_1998), 100)
        self.assertEqual(len(afi_2007), 100)

    def test_get_rank_movement(self):
        # We need to choose films that are in both the 1998 list and the 2007 list to test rank movement
        for film_obj in self.afitop100.afi_list:
            if film_obj.afi_rank_1998 is not None and film_obj.afi_rank_2007 is not None:
                self.assertIsNotNone(self.afitop100.calculate_rank_movement(film_obj))

    def test_get_film_by_title(self):
        film = self.afitop100.get_film_by_title(FILM_TITLE)
        self.assertEqual(film.title.lower(), FILM_TITLE.lower())

    def test_get_top_100_of_all_time_json(self):
        json_list = json.loads(self.afitop100.get_afi_list_json())
        self.assertGreaterEqual(len(json_list), 99)

    def test_get_afi_list_by_year_json(self):
        json_list = json.loads(self.afitop100.get_afi_list_json(year=2007))
        self.assertGreaterEqual(len(json_list), 99)

    def test_get_afi_list_by_year_csv(self):
        csv_list = self.afitop100.get_afi_list_csv(year=2007).splitlines()
        self.assertGreaterEqual(len(csv_list), 99)
