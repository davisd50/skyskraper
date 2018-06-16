import argparse
import csv
import logging
from os import path
import sys
import tempfile
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import exceptions as selenium_exc
from sparc.config.container import SparcConfigContainerFactory
from .conifg import get_runtime_config
from .sg import session

description = """\
SkyTrak shot data export tool.
"""
def getScriptArgumentParser(args=sys.argv):
    """Return ArgumentParser object
    
    Args:
        description: Text description of application ArgumentParser will be
                     applied to.
    
    Kwargs:
        args (list):        list of arguments that will be parsed.  The default
                            is the sys.argv list, and should be correct for most
                            use cases.
    
    Returns:
        ArgumentParser object that can be used to validate and execute the
        current script invocation.
    """
    # Description
    parser = argparse.ArgumentParser(
            description=description)

    # format
    parser.add_argument('format',
            default='csv',
            choices=['csv','tab'],
            help="Format of exported data.")

    # --username
    parser.add_argument('--username',
            help="Your login username to www.skygolf.com.")

    # --password
    parser.add_argument('--password',
            help="Your login username to www.skygolf.com.")

    # --file
    parser.add_argument('--file',
            help="File name to write data into.  defaults to standard out.")

    # --config_file
    parser.add_argument('--config',
            help="(optional) App configuration file.  This should be the path to "\
                 "a YAML configuration file.  See config_sample.yaml"\
                 "for detailed specifications.")

    # --driver
    parser.add_argument('--driver',
            help="Selenium web driver to use, default is PhantomJS.  See "\
                 "http://selenium-python.readthedocs.io for additional "\
                 "information on driver specific setup requirements.")

    # --timeout
    parser.add_argument('--timeout',
            help="Number of seconds to wait for web page loads.")
    
    # --verbose
    parser.add_argument('--verbose',
            action='store_true',
            help="Echo verbose messages to stdout.")
    
    # --debug
    parser.add_argument('--debug',
            action='store_true',
            help="Echo debug messages to stdout.")
    
    return parser

class SkySkraper(object):
    def __init__(self, config):
        self.config = SparcConfigContainerFactory(config)
        self.set_logging()
        self.client = getattr(webdriver, self.config.mapping()['Selenium']['webdriver'])()
        self.timeout = int(self.config.mapping()['Selenium']['timeout'])
    
    def set_logging(self):
        root_logger = logging.getLogger()
        root_logger.setLevel(self.config.mapping()['Logging']['root']['level'])
    
    def _debug_write_client_page_source_to_file(self):
        with tempfile.NamedTemporaryFile(mode='w+t') as file:
            file.write(self.client.page_source)
            print('Debug web page written to: {}'.format(file.name))
            import pdb;pdb.set_trace()
    
    def login(self):
        #TODO: update to use XPATH selection for username/password keywords vs exact names
        self.client.get('https://clubsg.skygolf.com/login/')
        element_username = self.client.find_element_by_id('f_username')
        element_username.send_keys(self.config.mapping()['SkyGolf']['identity']['username'])
        element_password = self.client.find_element_by_id('f_password')
        element_password.send_keys(self.config.mapping()['SkyGolf']['identity']['password'])
        element_login = self.client.find_element_by_id('btnLogin')
        element_login.click()
        for i in range(self.timeout):
            time.sleep(1)
            if 'invalid username' in self.client.page_source.lower():
                raise RuntimeError("Login attempt failed for user {}".format(self.config.mapping()['SkyGolf']['identity']['username']))
            if self.config.mapping()['SkyGolf']['identity']['username'].lower() in self.client.current_url.lower():
                break
        if not self.config.mapping()['SkyGolf']['identity']['username'].lower() in self.client.current_url.lower():
            raise RuntimeError("Timeout error while waiting for login.")
    
    def logoff(self):
        self.client.get('https://www.skygolf.com/signin.aspx?logout=1')
    
    def parse_skytrak_shots(self):
        self.client.get('https://clubsg.skygolf.com/skytrak/'+self.config.mapping()['SkyGolf']['identity']['username'])
        time.sleep(2)
        
        for i in range(self.timeout):
            time.sleep(1)
            try:
                element_loading = self.client.find_element_by_id('loading')
                if not element_loading.is_displayed():
                    break
            except selenium_exc.NoSuchElementException:
                pass
        #page is now loaded with session shot info
        handle = sys.stdout
        _path = self.config.mapping()['SkyGolf']['export']['file']
        try:
            if _path:
                if path.exists(_path):
                    raise EnvironmentError("{} already exists! exiting now!", format(_path))
                handle = open(_path, 'w')
            writer = None
            soup = BeautifulSoup(self.client.page_source, 'html.parser')
            for session_tag in soup.find(id='sessions-list').find_all('div', recursive=False):
                sg_session = session.SGSessionFromBSDivSpec(session_tag)
                if not writer:
                    dialect = 'excel' if self.config.mapping()['SkyGolf']['export']['format'] == 'csv' else 'excel-tab'
                    writer = csv.DictWriter(handle,
                                            dialect=dialect,
                                            extrasaction='ignore',
                                            fieldnames = ['id','date','club','duration', 'total_shots',
                                                          'sequence','ball_speed','club_speed',
                                                          'launch_angle','backspin','sidespin',
                                                          'carry_distance','total_distance',
                                                          'deviation'])
                    writer.writeheader()
                for sg_shot in sg_session.shots:
                    row = {}
                    row.update(sg_session.__dict__)
                    row.update(sg_shot.__dict__)
                    writer.writerow(row)
        finally:
            if handle != sys.stdout:
                handle.close()
    
    def go(self):
        self.login()
        self.parse_skytrak_shots()
        self.logoff()

def main():
    args = getScriptArgumentParser().parse_args()
    app = SkySkraper(get_runtime_config(args))
    app.go() 

if __name__ == '__main__':
    main()