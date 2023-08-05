import logging
from lxml import etree

logger = logging.getLogger('main.{}'.format(__name__))
extra = {'signature': '---SIGNATURE-NOT-SET---'}


class TaskReport:
    def __init__(self, service):
        self.service = service
        self.report = {
            'commit_failure': False,
            'service_results': self._initialize_device_results(self.service),
            'original_running_configs': self._initialize_device_results(self.service),
            'target_running_configs': self._initialize_device_results(self.service),
            'current_running_configs': self._initialize_device_results(self.service),
            'current_startup_configs': self._initialize_device_results(self.service)
        }

    @staticmethod
    def _initialize_device_results(service):
        results = {}
        for device in service:
            results.update({device['device']: 'NOT_COLLECTED'})
        logger.debug('Initialise task results: {}'.format(results), extra=extra)
        return results

    def set_commit_failure(self):
        self.report['commit_failure'] = True

    def set_service_result(self, device, result):
        self.report['service_results'][device] = result

    def set_device_config_data(self, config, device, data):
        self.report[config][device] = self.stringify_etree(data)

    def get_device_config_data(self, config=None):
        if config is None:
            return self.report
        else:
            return self.report.get(config, 'CONFIG DATA NOT FOUND: {}'.format(config))

    @staticmethod
    def stringify_etree(xml_etree):
        return etree.tostring(xml_etree, pretty_print=True).decode()
