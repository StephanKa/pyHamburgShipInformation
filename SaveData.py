""" module for saving the data to a mysql database or a sqlite database """
try:
    import urllib2
except:
    import urllib.request
import base64
import sys
import sqlite3
import setup
import mysql.connector


class SaveData(object):
    """ class which can save all ship data to database """

    def __init__(self, ship_info):
        self.ship_info = ship_info
        try:
            if(setup.DATABASE_TYPE == 'mysql'):
                self.conn = mysql.connector.connect(user=setup.USER,
                                                    password=setup.PASSWORD,
                                                    host=setup.HOST,
                                                    database=setup.DATABASE)
                self.insert_command = 'INSERT IGNORE INTO'
            elif(setup.DATABASE_TYPE == 'sqlite'):
                self.conn = sqlite3.connect(setup.FILENAME_SQLITE)
                self.insert_command = 'INSERT OR IGNORE INTO'
            else:
                raise BaseException('Database type not know: {0}'.format(setup.DATABASE_TYPE))
            self.cursor = self.conn.cursor()
            self._create_table()
            self._insert_name()
            ship_id = self._get_ship_id()
            self._insert_arrival(ship_id)
            self.cursor.close()
        except BaseException as ex:
            print(str(ex))

    def __del__(self):
        try:
            self.conn.close()
        except BaseException as ex:
            print(str(ex))

    def _create_table(self):
        if(setup.DATABASE_TYPE == 'mysql'):
            self.cursor.execute(setup.MYSQL_DATABASE_SHIP_NAME_SETUP)
            self.cursor.execute(setup.MYSQL_DATABASE_SHIP_HAMBURG_ETA_SETUP)
        elif(setup.DATABASE_TYPE == 'sqlite'):
            self.cursor.execute(setup.SQLITE_DATABASE_SHIP_NAME_SETUP)
            self.cursor.execute(setup.SQLITE_DATABASE_SHIP_HAMBURG_ETA_SETUP)
        self.conn.commit()

    def _get_image(self):
        base_image_url = 'https://www.hafen-hamburg.de{0}'
        if(sys.version_info >= (3, 0)):
            request = urllib.request.Request(base_image_url.format(self.ship_info.ship_picture))
            content = urllib.request.urlopen(request)
        else:
            request = urllib2.Request(base_image_url.format(self.ship_info.ship_picture))
            content = urllib2.urlopen(request)
        return base64.b64encode(content.read())

    def _get_ship_id(self):
        command = '''SELECT id FROM ship_name WHERE name="{0}"'''.format(self.ship_info.ship_name)
        self.cursor.execute(command)
        return self.cursor.fetchall()[0][0]

    def _insert_arrival(self, ship_id):
        command = self.insert_command + ''' ship_hamburg_eta (eta, anchorage, F_SHIP_ID)
                                            VALUES ("{0}", "{1}", {2})'''.format(self.ship_info.time_eta,
                                                                                 self.ship_info.ship_anchorage,
                                                                                 ship_id)
        self.cursor.execute(command)
        self.conn.commit()

    def _insert_name(self):
        command = self.insert_command + ''' ship_name (name, length, teu, type, image, imo)
                                            VALUES ("{0}", {1}, {2}, "{3}", "{4}", {5})'''.format(self.ship_info.ship_name,
                                                                                                  self.ship_info.ship_length,
                                                                                                  self.ship_info.teu,
                                                                                                  self.ship_info.ship_type,
                                                                                                  self._get_image(),
                                                                                                  self.ship_info.imo)
        self.cursor.execute(command)
