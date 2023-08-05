import logging
from ncservice.ncDeviceOps.nc_device_ops import NcDeviceOps
from ncservice.ncDeviceOps.task_report import TaskReport
from ncservice.ncDeviceOps.threaded.base_thread_class import BaseThreadClass

logger = logging.getLogger('main.{}'.format(__name__))
extra = {'signature': '---SIGNATURE-NOT-SET---'}


class ConfirmCommit(BaseThreadClass):
    def __init__(self, service):
        super().__init__()
        self.service = service
        self.results = TaskReport(service)

    def confirm_commit(self, persist_id=None):
        if persist_id is None:
            persist_id = '123456'

        logger.debug('Requesting thread queue for _th_confirm_commit', extra=extra)
        logger.debug('persist_id={}'
                     .format(persist_id), extra=extra)
        enclosure_queue = self.create_thread_queue(
            self._th_confirm_commit,
            persist_id=persist_id
        )

        for device in self.service:
            enclosure_queue.put(device)

        enclosure_queue.join()

    def _th_confirm_commit(self, tid, queue,
                           persist_id=None):
        persist_id = persist_id
        while True:
            target_device = queue.get()
            device_name = target_device['device']
            host = target_device['host']
            port = target_device.get('ncport', 830)
            session = NcDeviceOps(host, port=port, tid=tid)
            result = session.nc_confirm_commit(persist_id=persist_id)
            if not result:
                logger.error(
                    'TID-{} Failed to confirm commit configs for device {}'.format(tid, device_name))
            else:
                current_config = session.nc_get_configs()
                self.results.set_device_config_data('current_running_configs', device_name, current_config)
                self.results.set_service_result(device_name, 'SUCCESS')
            session.close_session()
            queue.task_done()
