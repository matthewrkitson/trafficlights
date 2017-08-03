from controller import Controller
from urllib.parse import urljoin
import requests
import json
import os
import base64
import _thread as thread

class TeamCityUpdater:
    def __init__(self, lights, logger):
        self.lights = lights
        self.logger = logger

    def update(self):
        print('TeamCity updater running on thread ' + str(thread.get_ident()))

        config = TeamCityUpdater._read_config('teamcity-config.json')
        baseurl = config['baseurl']
        username = config['username']
        password = TeamCityUpdater._unobscure(config['obscured_password'])
        build_types = config['build_types']
        
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

    def _read_config(config_path):
        if not os.path.isfile(config_path):
            TeamCityUpdater._write_default_config(config_path)
            
        with open(config_path) as config_stream:
            config = json.load(config_stream)

        return config
        
    def _write_config(config, config_path):
        with open(config_path, 'w') as config_stream:
            json.dump(config, config_stream, indent=4)

    def _write_default_config(config_path):
        config = { 
            'baseurl': 'http://teamcity/',
            'username': 'username',
            'obscured_password': TeamCityUpdater._obscure('password'),
            'build_types': [
                'buildType1'
            ]
        }
        
        TeamCityUpdater._write_config(config, config_path)

    def _obscure(plaintext):
        # This does nothing more than prevent casual observtion
        # of the password. However, even if proper encryption
        # was used, we'd still have to store the password somewhere
        # so it wouldn't actually offer any extra security. 
        return base64.b64encode(plaintext.encode('utf-8')).decode('ascii')
        
    def _unobscure(cyphertext):
        return base64.b64decode(cyphertext).decode('utf-8')
