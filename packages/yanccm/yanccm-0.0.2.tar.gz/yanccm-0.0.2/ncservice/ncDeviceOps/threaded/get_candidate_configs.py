import logging
from ncservice.ncDeviceOps.nc_device_ops import NcDeviceOps
from ncservice.ncDeviceOps.task_report import TaskReport
from ncservice.ncDeviceOps.threaded.base_thread_class import BaseThreadClass

logger = logging.getLogger('main.{}'.format(__name__))
extra = {'signature': '---SIGNATURE-NOT-SET---'}


class GetCandidateConfigs(BaseThreadClass):
    def __init__(self, service):
        super().__init__()
        self.service = service
        self.results = TaskReport(service)

    def get_candidate_configs(self):
        logger.debug('Requesting thread queue for _th_read_configs', extra=extra)
        enclosure_queue = self.create_thread_queue(
            self._th_create_candidate_configs
        )

        for device in self.service:
            config = device['config']
            device.update({'target_config': config})
            enclosure_queue.put(device)

        enclosure_queue.join()
        return self.results

    def _th_create_candidate_configs(self, tid, queue):
        while True:
            target_device = queue.get()
            device_name = target_device['device']
            host = target_device['host']
            port = target_device.get('ncport', 830)
            logger.info('TID-{}: Accepting device config from queue: {}'.format(tid, device_name),
                        extra=extra)

            config = target_device['target_config']
            logger.warning(
                'TID-{}: debug device configs may contain sensitive information'.format(tid, device_name, config),
                extra=extra)
            logger.debug('TID-{}: Target device: {} config: {}'.format(tid, device_name, config), extra=extra)

            session = NcDeviceOps(host, port=port, tid=tid)
            current_config = session.nc_get_configs()
            self.results.set_device_config_data('original_running_configs', device_name, current_config)
            candidate_config = session.nc_get_candidate_config(config)
            if candidate_config is not None:
                self.results.set_device_config_data('target_running_configs', device_name, candidate_config)
                self.results.set_service_result(device_name, 'SUCCESS')
            else:
                logger.error("TID-{}: Unable to create candidate configs for device {}"
                             .format(tid, device_name), extra=extra)
                queue.task_done()
                continue

            session.close_session()
            queue.task_done()
            continue
