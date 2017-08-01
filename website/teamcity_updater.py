from controller import Controller
from urllib.parse import urljoin
import requests

class TeamCityUpdater:
    def __init__(self, lights, logger):
        self.lights = lights
        self.logger = logger

    def update(self):

        self.logger.debug('TeamCity updater running')

        build_types = [ 'buildType1' ]
        hostname = 'http://teamcity/'
        username = 'user'
        password = 'password'        

        baseurl = urljoin('http://', hostname)
        headers = {'Accept': 'application/json'}

        for i, build_type in enumerate(build_types):
            try:
                if not build_type: continue
                
                url = urljoin(baseurl, 'app/rest/builds/buildType:' + build_type)
                self.logger.debug('Getting url: ' + url)
                r = requests.get(url, auth=(username, password), headers=headers)
                self.logger.debug('HTTP status code: ' + str(r.status_code))
            
                build_info = r.json()
                build_status = build_info['status']
    
                if build_status == 'SUCCESS':
                    self.lights.set_indicator(i, Controller.GREEN)
                elif build_status == 'FAILURE':
                    self.lights.set_indicator(i, Controller.RED)
                else:
                    self.logger.debug('Unexpected build status "' + build_status + '" for ' + build_type)
            
            except requests.exceptions.ConnectionError as ex:
                self.logger.info('Connection error when trying to retrieve build staus for ' + build_type)
                self.logger.info(ex)
            except Exception as ex:
                self.logger.debug('Error occurred when trying to retrieve build status for ' + build_type)
                self.logger.exception(ex)
