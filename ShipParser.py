""" module which parses the content from a html site """
from BeautifulSoup import BeautifulSoup
from ShipInformation import ShipInformation


class ParseURLGetInformation(object):
    """ parse all informations """

    def __init__(self, raw_data):
        self.ship_found = False
        self.ship_list = []
        self.image_ending = '.jpg'
        self.data = raw_data
        self._iterate_through_data()

    def _iterate_through_data(self):
        soup = BeautifulSoup(self.data)
        for temp in soup.findAll("ul", {"class": "list-tile-box"}):
            temp_ship_info = ShipInformation()
            temp_ship_info.ship_picture = temp.a.img['src']
            temp_ship_info.ship_name = temp.a.img['alt']
            temp_detail = temp.findAll("dd")
            temp_ship_info.imo = temp_detail[0].text
            temp_ship_info.ship_type = temp_detail[1].text
            temp_ship_info.teu = temp_detail[2].text
            if('-' in temp_ship_info.teu):
                temp_ship_info.teu = 0
            temp_ship_info.ship_length = temp_detail[3].text
            temp_ship_info.time_eta = temp_detail[4].text
            temp_ship_info.ship_anchorage = temp_detail[5].text
            self.ship_list.append(temp_ship_info)
