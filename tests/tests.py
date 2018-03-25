# -*- coding: utf-8 -*-
""" GENERAL TEST DESCRIPTION HERE

TODO: -

command line call:    python tests.py <Test_Case_Name>[.<Test_Method>] [<Test_Case_Name>.<Test_Method>]...
Test_Case_Name:       class name
Test_method:          optional argument
"""
import time
import unittest
import sys
import os
import xmlrunner
sys.path.extend(["../"])
import main
from ShipInformation import ShipInformation
from ShipParser import ParseURLGetInformation


class TestShipInformation(unittest.TestCase):
    """ Testcase for checking ShipInformation class """

    def test_ship(self):
        ''' check for availabilty of variables '''
        temp = ShipInformation()
        self.assertIsNone(temp.imo)
        self.assertIsNone(temp.ship_anchorage)
        self.assertIsNone(temp.ship_length)
        self.assertIsNone(temp.ship_name)
        self.assertIsNone(temp.ship_picture)
        self.assertIsNone(temp.ship_type)
        self.assertIsNone(temp.teu)
        self.assertIsNone(temp.time_eta)


class TestShipParser(unittest.TestCase):
    """ Testcase for testing ship parser class """

    def setUp(self):
        self.html = """<li class="col-25 tile-box-entry"><ul class="list-tile-box"><li><a href="/de/schiff/hammonia-husum-imo-9326835---44945"><div class="image-container"><img src="/images/450x300/fotos/schiffe/9326835.jpg" alt="HammoniaHusum" class="image")"></div></a></li><li class="list-tile-box-hl"><a href="/de/schiff/hammonia-husum-imo-9326835---44945">HammoniaHusum<ul class="list-inline"></ul></a></li><li class="list-tile-box-content"><a href="/de/schiff/hammonia-husum-imo-9326835---44945"><dl class="list-datas"><dt>IMO</dt><dd>9326835</dd><dt>Schiffstyp</dt><dd>Containerschiff</dd><dt>TEU</dt><dd>2556</dd><dt>Länge</dt><dd>210.00</dd><dt>ETA</dt><dd>20.11.1700:00</dd><dt>Liegeplatz</dt><dd>O'swaldkai</dd></dl></a></li><li class="list-tile-box-content"><a href="/de/schiff/hammonia-husum-imo-9326835---44945"></a><a class="list-tile-link" href="/de/schiff/hammonia-husum-imo-9326835---44945"></a></li></ul></li>"""

    def test_ship_parser(self):
        """ test correct parsing of HTML """
        temp = ParseURLGetInformation(self.html)
        self.assertNotEqual(temp.ship_list, list())
        self.assertEqual(temp.ship_list[0].ship_name, 'HammoniaHusum')
        self.assertEqual(temp.ship_list[0].teu, '2556')
        self.assertEqual(temp.ship_list[0].time_eta, '20.11.1700:00')
        self.assertEqual(temp.ship_list[0].imo, '9326835')
        self.assertEqual(temp.ship_list[0].ship_anchorage, "O'swaldkai")
        self.assertEqual(temp.ship_list[0].ship_length, '210.00')
        self.assertEqual(temp.ship_list[0].ship_type, 'Containerschiff')


class TestMain(unittest.TestCase):
    """ Testcase for testing whole program """

    def test_main(self):
        """ test main with instantiation and saving data """
        main.main()


class TestMysqlMain(unittest.TestCase):
        """ Testcase for testing whole program """

    def test_main(self):
        """ test main with instantiation and saving data """
        main.setup.DATABASE_TYPE = 'mysql'
        main.setup.PASSWORD = ''
        main.setup.HOST = '127.0.0.1'
        main.setup.USER = 'root'
        main.main()


if(__name__ == '__main__'):
    BEGIN_TIME = time.time()
    SUITE = unittest.TestSuite()
    if(len(sys.argv)) < 2:
        if(not os.path.exists('coverage')):
            os.mkdir('coverage')
        with open('coverage/test-results.xml', 'w') as output:
            unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output),
                          # these make sure that some options that are not applicable
                          # remain hidden from the help menu.
                          failfast=False, buffer=False, catchbreak=False)
    else:
        while(len(sys.argv) > 1):
            TMP_ARGUMENT = sys.argv.pop(1)
            if(TMP_ARGUMENT[0:2] == '--'):
                # add optional parameter here
                pass
            else:
                # split the test method from test class
                TEST_ARGUMENT = TMP_ARGUMENT.split('.')
                if(len(TEST_ARGUMENT) == 2):
                    TEST_CASE = TEST_ARGUMENT[0]
                    TEST_METHOD = TEST_ARGUMENT[1]
                    SUITE.addTest((eval(TEST_CASE))(TEST_METHOD))
                elif(len(TEST_ARGUMENT) == 1):
                    TEST_CASE = TEST_ARGUMENT[0]
                    if(SUITE != unittest.TestSuite()):
                        raise Exception('ERROR: Cannot have multiple test suites!')
                    SUITE = unittest.TestLoader().loadTestsFromTestCase(eval(TEST_CASE))
                else:
                    raise Exception('ERROR: invalid test case specification!')
        # set the test runner with parameters (description, verbosity, stream)
        # description means the test method description
        # verbosity is the output for the test suite
        # stream is a stream that can be output to other instances for example see code below:
        #
        # from StringIO import StringIO
        #
        # stream = StringIO()
        # runner = unittest.TextTestRunner(stream = stream)
        # print('Test Output\n{}'.format(stream.read()))
        RUNNER = unittest.TextTestRunner(descriptions=False, verbosity=2)
        TEST_RESULTAT = RUNNER.run(SUITE)
        print('Time elapsed: {0}sec'.format(time.time() - BEGIN_TIME))
        # check for errors or failures and return 0 or 1
        if((TEST_RESULTAT.errors != []) or (TEST_RESULTAT.failures != [])):
            sys.exit(1)
        else:
            sys.exit(0)
