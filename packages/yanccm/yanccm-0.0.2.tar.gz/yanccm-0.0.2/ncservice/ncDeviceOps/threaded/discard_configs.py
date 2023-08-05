import logging
from ncservice.ncDeviceOps.nc_device_ops import NcDeviceOps
from ncservice.ncDeviceOps.task_report import TaskReport
from ncservice.ncDeviceOps.threaded.base_thread_class import BaseThreadClass

logger = logging.getLogger('main.{}'.format(__name__))
extra = {'signature': '---SIGNATURE-NOT-SET---'}


class DiscardConfigs(BaseThreadClass):
    def __init__(self, service):
        super().__init__()
        self.service = service
        self.results = TaskReport(service)

    def discard_configs(self):
        logger.debug('Requesting thread queue for _th_discard_configs', extra=extra)
        enclosure_queue = self.create_thread_queue(
            self._th_discard_configs
        )

        for device in self.service:
            enclosure_queue.put(device)

        enclosure_queue.join()
        return self.results

    def _th_discard_configs(self, tid, queue):
        while True:
            target_device = queue.get()
            device_name = target_device['device']
            host = target_device['host']
            port = target_device.get('ncport', 830)

            session = NcDeviceOps(host, port=port, tid=tid)
            result = session.nc_discard_configs()
            if result is not None:
                logger.error('TID-{} Failed to discard configs for device: {}'.format(tid, device_name), extra=extra)
            else:
                self.results.set_device_config_data('target_running_configs', device_name, result)
                self.results.set_service_result(device_name, 'SUCCESS')
                logger.info('TID-{} Configs successfully discarded for device: {}'.format(tid, device_name), extra=extra)

            session.close_session()
            queue.task_done()
