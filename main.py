""" module for parsing ship data from hamburg harbour website """
import time
import requests
import setup
from ShipParser import ParseURLGetInformation
from SaveData import SaveData


def main():
    BEGIN = time.time()
    RESPONSE = requests.get(setup.URL, headers=setup.HEADERS)
    PARSED = ParseURLGetInformation(RESPONSE.text)
    for temp_ship in PARSED.ship_list:
        SaveData(temp_ship)
    print('Elapsed Time: {0:.2f}sec'.format(time.time() - BEGIN))

if __name__ == '__main__':
    main()
