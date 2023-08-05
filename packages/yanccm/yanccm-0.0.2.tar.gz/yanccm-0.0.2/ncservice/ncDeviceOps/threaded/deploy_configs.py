import logging
from ncservice.ncDeviceOps.nc_device_ops import NcDeviceOps
from ncservice.ncDeviceOps.task_report import TaskReport
from ncservice.ncDeviceOps.threaded.base_thread_class import BaseThreadClass

logger = logging.getLogger('main.{}'.format(__name__))
extra = {'signature': '---SIGNATURE-NOT-SET---'}


class DeployConfigs(BaseThreadClass):
    def __init__(self, service):
        super().__init__()
        self.service = service
        self.results = TaskReport(service)

    def deploy_configs(self,
                       commit_confirm=False,
                       confirm_timeout=30,
                       persist_id=None,
                       commit_replace=False,
                       diff_only=False,
                       merge_configs=True
                       ):
        if persist_id is None:
            persist_id = '123456'
        if commit_replace:
            default_operation = 'replace'
        else:
            default_operation = 'merge'

        logger.debug('Requesting thread queue for _th_deploy_configs', extra=extra)
        logger.debug('persist_id={}, diff_only={}, commit_confirm={}, confirm_timeout={}, default_operation={}'
                     .format(persist_id, diff_only, commit_confirm, confirm_timeout, default_operation), extra=extra)
        enclosure_queue = self.create_thread_queue(
            self._th_deploy_configs,
            persist_id=persist_id,
            diff_only=diff_only,
            commit_confirm=commit_confirm,
            confirm_timeout=confirm_timeout,
            default_operation=default_operation,
        )

        for device in self.service:
            config = device['config']
            device.update({'target_config': config})
            enclosure_queue.put(device)

        enclosure_queue.join()
        return self.results

    def _th_deploy_configs(self, tid, queue,
                           persist_id=None,
                           diff_only=False,
                           commit_confirm=False,
                           confirm_timeout=None,
                           default_operation='merge'):
        while True:
            target_device = queue.get()
            device_name = target_device['device']
            host = target_device['host']
            port = target_device.get('ncport', 830)
            logger.info('TID-{}: Accepting device config from queue: {}'.format(tid, device_name),
                        extra=extra)

            if not target_device.get('last_commit_result'):
                target_device.update({'last_commit_result': ''})
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
            else:
                logger.error("TID-{}: Unable to create candidate configs for device {}"
                             .format(tid, device_name), extra=extra)
                queue.task_done()
                continue

            if commit_confirm:
                logger.info('TID-{} Issuing confirmed-commit for: {}'.format(tid, target_device['device']), extra=extra)
                result = session.nc_deploy_configs(config, commit_confirm=True, persist_id=persist_id,
                                                   confirm_timeout=str(confirm_timeout), default_operation=default_operation)
                if not result:
                    logger.error('TID-{} Failed to commit configs for device {}'.format(tid, target_device['device']),
                                 extra=extra)
                    self.results.set_commit_failure()
                    session.close_session()
                    queue.task_done()
                    continue
            else:
                result = session.nc_deploy_configs(config)
                if not result:
                    logger.error("TID-{}: Commit failed for device: {}"
                                 .format(tid, device_name), extra=extra)
                    self.results.set_commit_failure()
                    session.close_session()
                    queue.task_done()
                    continue
                else:
                    current_config = session.nc_get_configs()
                    self.results.set_device_config_data('current_running_configs', device_name, current_config)
                    self.results.set_service_result(device_name, 'SUCCESS')

            session.close_session()
            queue.task_done()
