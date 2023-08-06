import os, sys
import unittest

from contextlib import redirect_stdout
from io import StringIO

from logging_service import LoggingService
from logging import StreamHandler
from logging import DEBUG

TEST_ALL = True
#TEST_ALL = False

class TestBirdsTrainingParallel(unittest.TestCase):


    #------------------------------------
    # setUp 
    #-------------------

    def setUp(self):
        self.curr_dir = os.path.dirname(__file__)
        self.console_redirect_file = os.path.join(self.curr_dir, 'fake_console.txt')
        self.test_log_file = os.path.join(self.curr_dir, 'tst_log.txt')

    #------------------------------------
    # tearDown 
    #-------------------
    
    def tearDown(self):
        try:
            os.remove(self.console_redirect_file)
        except:
            pass
        try:
            os.remove(self.test_log_file)
        except:
            pass

    #------------------------------------
    # test_log_to_file
    #-------------------
    
    @unittest.skipIf(TEST_ALL != True, 'skipping temporarily')
    def test_log_to_file(self):

        curr_dir = os.path.dirname(__file__)
        log = LoggingService(logfile=self.test_log_file)
        log.info("Info line 1")
        log.info("Info line 2")
        log.logging_level = DEBUG
        log.debug("Debug line 1")
        
        with open(self.test_log_file, 'r') as log_fd:
            line = log_fd.readline()
            self.assertTrue(line.find('Info line 1') > -1)
            line = log_fd.readline()
            self.assertTrue(line.find('Info line 2') > -1)
            line = log_fd.readline()
            self.assertTrue(line.find('Debug line 1') > -1)


    #------------------------------------
    # test_tee_to_console 
    #-------------------
    
    @unittest.skipIf(TEST_ALL != True, 'skipping temporarily')
    def test_tee_to_console(self):
        log = LoggingService(logfile=self.test_log_file,
                             tee_to_console=True)
        captured_stdout = StringIO()
        for one_handler in log.handlers:
            if type(one_handler) == StreamHandler:
                one_handler.setStream(captured_stdout)
                
        log.info("ConsoleTee line 1")

        line = captured_stdout.getvalue()
        self.assertTrue(line.find('ConsoleTee line 1') > -1)

    #------------------------------------
    # test_to_console 
    #-------------------
    
    @unittest.skipIf(TEST_ALL != True, 'skipping temporarily')
    def test_to_console(self):

        log = LoggingService()
        captured_stdout = StringIO()
        for one_handler in log.handlers:
            if type(one_handler) == StreamHandler:
                one_handler.setStream(captured_stdout)
                
        log.info("ConsoleTee line 1")

        line = captured_stdout.getvalue()
        self.assertTrue(line.find('ConsoleTee line 1') > -1)

# ----------------------- Main -----------------

if __name__ == "__main__":
    
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
