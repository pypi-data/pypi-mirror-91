import pymongo
import os
import logging
from lxml import etree
from difflib import context_diff
from ncservice.ncDeviceOps import helpers

MONGO_DB = os.environ['MONGO_DB']
logger = logging.getLogger('main.{}'.format(__name__))
extra = {'signature': '---SIGNATURE-NOT-SET---'}


class ConfigDb:
    def __init__(self, target_configs):
        self.target_configs = target_configs

    @staticmethod
    def get_device_ref_configs(device):
        client = pymongo.MongoClient(MONGO_DB)
        result = client.configs.configs.find_one({"device": device})
        if result is None:
            logger.warning('No reference config found for {}'.format(device))
            logger.warning('Try running "compliance" with --baseline {}'.format(device))
            return 'EMPTY'
        else:
            return result['config']

    @staticmethod
    def update_device_configs(device_configs):
        client = pymongo.MongoClient(MONGO_DB)
        for device, config in device_configs.items():
            result = client.configs.configs.find_one({"device": device})
            if result is None:
                print('Adding initial device configs for {}'.format(device))
                client.configs.configs.insert_one({'device': device, 'config': config})
            else:
                client.configs.configs.update_one(
                    {'_id': result['_id']},
                    {"$set": {'config': config}}
                )
                print('updating device configs for {}'.format(device))

        return

    @staticmethod
    def diff_device_configs(device_configs):
        client = pymongo.MongoClient(MONGO_DB)
        _diffs = {}
        for device, config in device_configs.items():
            result = client.configs.configs.find_one({"device": device})
            if result is None:
                print('No device config history found for {}.  Try running with --device {} --baseline'
                      .format(device, device))
            else:
                _config_ref = result['config']
                _config_running = config
                _config_diff = '\n'.join(context_diff(_config_ref.splitlines(),
                                                      _config_running.splitlines()))
                _diffs.update({device: _config_diff})

        return _diffs

    @staticmethod
    def replace_device_configs(manifest):
        client = pymongo.MongoClient(MONGO_DB)
        for device in manifest['service']:
            result = client.configs.configs.find_one({"device": device['device']})
            etree.fromstring(result['config'])
            device['config'] = helpers._copy_nc_data_to_config(etree.fromstring(result['config']))
        # print(manifest)
        return manifest
