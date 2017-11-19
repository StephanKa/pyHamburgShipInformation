""" module which holds same needed data """

URL = 'https://www.hafen-hamburg.de/de/schiffe/eta?view=gitter'
HEADERS = {'X-Requested-With': 'XMLHttpRequest',
           'Host': 'www.hafen-hamburg.de',
           'Referer': 'https://www.hafen-hamburg.de/de/schiffe/eta'}
HOST = 'localhost'
USER = 'root'
PASSWORD = 'root'
PORT = 3306
DATABASE = 'Ships'
# possible options 'mysql' or 'sqlite'
DATABASE_TYPE = 'sqlite'
FILENAME_SQLITE = 'ship.db'

# mysql scripts for creating the sqlite database or mysql tables
MYSQL_DATABASE_SHIP_NAME_SETUP = """CREATE TABLE IF NOT EXISTS `ship_name` (
`id` INT(11) NOT NULL AUTO_INCREMENT,
`name` CHAR(50) NULL DEFAULT NULL,
`length` FLOAT NOT NULL,
`teu` INT(11) NOT NULL,
`type` CHAR(50) NOT NULL,
`imo` INT(11) NULL DEFAULT NULL,
`image` MEDIUMBLOB NULL,
`added` DATETIME NULL DEFAULT NULL,
`mt_links` VARCHAR(100) NULL DEFAULT NULL,
PRIMARY KEY (`id`),
UNIQUE INDEX `name` (`name`)
)
AUTO_INCREMENT=0;
"""

MYSQL_DATABASE_SHIP_HAMBURG_ETA_SETUP = """CREATE TABLE IF NOT EXISTS `ship_hamburg_eta` (
`id` INT(11) NOT NULL AUTO_INCREMENT,
`eta_formated` DATETIME NULL DEFAULT NULL,
`eta` CHAR(50) NULL DEFAULT NULL,
`anchorage` CHAR(50) NULL DEFAULT NULL,
`added` DATETIME NULL DEFAULT NULL,
`F_SHIP_ID` INT(11) NULL DEFAULT NULL,
PRIMARY KEY (`id`),
UNIQUE INDEX `eta` (`eta_formated`),
INDEX `F_SHIP` (`F_SHIP_ID`),
CONSTRAINT `F_SHIP` FOREIGN KEY (`F_SHIP_ID`) REFERENCES `ship_name` (`id`)
)
"""

# sqlite script for creating tables
SQLITE_DATABASE_SHIP_NAME_SETUP = """CREATE TABLE IF NOT EXISTS `ship_name` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT,
`name` CHAR(50) NULL DEFAULT NULL UNIQUE,
`length` FLOAT NOT NULL,
`teu` INT(11) NOT NULL,
`type` CHAR(50) NOT NULL,
`imo` INT(11) NULL DEFAULT NULL,
`image` MEDIUMBLOB NULL,
`added` DATETIME NULL DEFAULT NULL,
`mt_links` VARCHAR(100) NULL DEFAULT NULL
)
"""

SQLITE_DATABASE_SHIP_HAMBURG_ETA_SETUP = """CREATE TABLE IF NOT EXISTS `ship_hamburg_eta` (
`id` INTEGER PRIMARY KEY AUTOINCREMENT,
`eta_formated` DATETIME NULL DEFAULT NULL,
`eta` CHAR(50) NULL DEFAULT NULL UNIQUE,
`anchorage` CHAR(50) NULL DEFAULT NULL,
`added` DATETIME NULL DEFAULT NULL,
`F_SHIP_ID` INT(11) NULL DEFAULT NULL,
CONSTRAINT `F_SHIP` FOREIGN KEY (`F_SHIP_ID`) REFERENCES `ship_name` (`id`)
)
"""
