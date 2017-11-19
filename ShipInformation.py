""" module that holds the ship informations """


class ShipInformation(object):
    """ holds some necessary data from parsed ships """

    def __init__(self):
        self.ship_picture = None
        self.ship_name = None
        self.imo = None
        self.ship_type = None
        self.teu = None
        self.ship_length = None
        self.time_eta = None
        self.ship_anchorage = None
