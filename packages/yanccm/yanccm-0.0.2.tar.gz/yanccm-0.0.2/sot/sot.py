import requests
import ipaddress
import os
from jinja2 import Template

TOKEN = os.environ['SOT_TOKEN']
BASE_URL = os.environ['SOT_URL']


class DevicesDb:
    def __init__(self, *args, **kwargs):
        self.devices = []
        self.kwargs = kwargs
        self.get_devices()
        # print(self.devices)

    def get_devices(self):
        headers = {
            'Authorization': 'Token {}'.format(TOKEN)
        }
        url = '{}/dcim/devices'.format(BASE_URL)
        result = requests.get(url, self.kwargs, headers=headers)
        self.devices = result.json()['results']

    def get_devices_management(self):
        devices_list = []
        for device in self.devices:
            _management = {
                'device': device['name'],
                'host': str(ipaddress.ip_interface(device['primary_ip']['address']).ip)
            }
            devices_list.append(_management)
        return devices_list

    def update_job_with_device_mgmt(self, job):
        for device in job['service']:
            for _device in self.get_devices_management():
                if device['device'].lower() == _device['device'].lower():
                    device.update(_device)
        return job


class Templates:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def generate_day0(data):
        result = []
        for device in data:
            template = device['custom_fields'].get('day0-template')
            if template is not None:
                with open('templates/{}'.format(template['label'])) as _file:
                    template = Template(_file.read())
                config = template.render(item=device)
                result.append({
                    'device': device['name'],
                    'host': str(ipaddress.ip_interface(device['primary_ip']['address']).ip),
                    'config': config
                })
            else:
                print('WARNING: Device {} has not Day0 template specified'.format(device['name']))

        return result
