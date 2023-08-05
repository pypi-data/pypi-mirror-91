# Notes for refactor
# operations should as far as possible be atomic operations
# The methods and classes should not store data other than for the current run/results
# Configuration rollback, configuration and execution history should be maintained elsewhere

import threading
from queue import Queue
from lxml import etree
from ncservice.ncDeviceOps.nc_device_ops import NcDeviceOps
import logging

nc_xmlns = "urn:ietf:params:xml:ns:netconf:base:1.0"
logger = logging.getLogger('main.{}'.format(__name__))
extra = {'signature': '---SIGNATURE-NOT-SET---'}


def _copy_nc_data_to_config(xml_etree):
    native = xml_etree.getchildren()
    config_element = etree.Element("{" + nc_xmlns + "}config", nsmap={'nc': nc_xmlns})
    for elem in native:
        config_element.append(elem)
    return etree.tostring(config_element).decode()


def stringify_etree(xml_etree):
    return etree.tostring(xml_etree, pretty_print=True).decode()


class ThreadedOperations:
    def __init__(self, service, thread_count=10):
        self.thread_count = thread_count
        self.thread_lock = threading.Lock()
        self.default_persist_id = '123456'
        logger.debug('Service config: {}'.format(service), extra=extra)
        self.service = service
        self.results = None

    def create_thread_queue(self, func, **kwargs):
        thread_count = self.thread_count
        enclosure_queue = Queue()
        logger.debug('Initialising thread queue with thread count {}'.format(thread_count), extra=extra)
        for i in range(thread_count):
            thread = threading.Thread(target=func, args=(i, enclosure_queue), kwargs=kwargs)
            thread.setDaemon(True)
            thread.start()

        return enclosure_queue

    def get_configs(self):
        logger.debug('Requesting thread queue for _th_read_configs', extra=extra)
        enclosure_queue = self.create_thread_queue(
            self._th_read_configs
        )

        for device in self.service:
            enclosure_queue.put(device)

        enclosure_queue.join()

    def _th_read_configs(self, tid, queue):
        while True:
            target_device = queue.get()
            device_name = target_device['device']
            host = target_device['host']
            port = target_device.get('ncport', 830)

            session = NcDeviceOps(host, port=port, tid=tid)
            current_config = session.nc_get_configs()
            if current_config is not None:
                # self._update_config_history(device_name, current_config)
                self.results.update_device_config_records(device_name, current_config, 'original_running_configs')
            else:
                logger.error('TID-{}: Unable to retrieve config for device: {}'
                             .format(tid, device_name), extra=extra)
                queue.task_done()
                continue

            session.close_session()
            queue.task_done()

    def deploy_configs(self,
                       commit_confirm=False,
                       confirm_timeout=30,
                       persist_id=None,
                       commit_replace=False,
                       diff_only=False,
                       merge_configs=True
                       ):
        if persist_id is None:
            persist_id = self.default_persist_id
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

    def _th_deploy_configs(self, tid, queue,
                           persist_id=None,
                           diff_only=False,
                           commit_confirm=False,
                           confirm_timeout=None,
                           default_operation=None):
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
            logger.warning('TID-{}: debug device configs may contain sensitive information'.format(tid, device_name, config), extra=extra)
            logger.debug('TID-{}: Target device: {} config: {}'.format(tid, device_name, config), extra=extra)

            session = NcDeviceOps(host, port=port, tid=tid)
            current_config = session.nc_get_configs()
            self._update_device_config_records(device_name, current_config, 'original_running_configs')
            candidate_config = session.nc_get_candidate_config(config)
            if candidate_config is not None:
                self._update_config_diffs(device_name, current_config, candidate_config)
                self._update_device_config_records(device_name, candidate_config, 'target_running_configs')
            else:
                logger.error("TID-{}: Unable to create candidate configs for device {}"
                             .format(tid, device_name), extra=extra)
                queue.task_done()
                continue

            if diff_only:
                session.close_session()
                queue.task_done()
                continue

            if commit_confirm:
                logger.info('TID-{} Issuing confirmed-commit for: {}'.format(tid, target_device['device']), extra=extra)
                result = session.nc_deploy_configs(config, commit_confirm=True, persist_id=persist_id, confirm_timeout=str(confirm_timeout))
                if not result:
                    logger.error('TID-{} Failed to commit configs for device {}'.format(tid, target_device['device']), extra=extra)
                    # Todo (1) How are tracking commit failure for rollback?
                    target_device['last_commit_result'] = 'FAILURE'
                    self.commit_failure = True
                    session.close_session()
                    queue.task_done()
                    continue
            else:
                result = session.nc_deploy_configs(config)
                if not result:
                    logger.error("TID-{}: Commit failed for device: {}"
                                 .format(tid, device_name), extra=extra)
                    # Todo (1) How are tracking commit failure for rollback?
                    self.commit_failure = 'COMMIT_FAILED'
                    session.close_session()
                    queue.task_done()
                    continue
                else:
                    current_config = session.nc_get_configs()
                    self._update_device_config_records(device_name, current_config, 'current_running_configs')

            session.close_session()
            queue.task_done()

    def confirm_commit(self, persist_id=None):
        if persist_id is None:
            persist_id = self.default_persist_id

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
                self._update_device_config_records(device_name, current_config, 'current_running_configs')
            session.close_session()
            queue.task_done()

    def discard_configs(self):
        logger.debug('Requesting thread queue for _th_discard_configs', extra=extra)
        enclosure_queue = self.create_thread_queue(
            self._th_discard_configs
        )

        for device in self.service:
            enclosure_queue.put(device)

        enclosure_queue.join()

    def _th_discard_configs(self, tid, queue):
        while True:
            target_device = queue.get()
            device_name = target_device['device']
            host = target_device['host']
            port = target_device.get('ncport', 830)

            session = NcDeviceOps(host, port=port, tid=tid)
            result = session.nc_discard_configs()
            if not result:
                logger.error('TID-{} Failed to discard configs for device: {}'.format(tid, device_name), extra=extra)
            else:
                logger.info('TID-{} Configs successfully discarded for device: {}'.format(tid, device_name), extra=extra)

            session.close_session()
            queue.task_done()

    # This may be needed for when we do commit without confirm
    def rollback(self,
                 # ncDeviceOps=True,
                 commit_confirm=False,
                 confirm_timeout=30,
                 persist_id=None,
                 commit_replace=True,
                 diff_only=False,
                 ):
        logger.debug('Initiating config rollback to last known device configuration', extra=extra)
        logger.debug('Requesting thread queue for _th_deploy_configs', extra=extra)
        logger.debug('commit_confirm={}, confirm_timeout={}, persist_id={}, commit_replace={}, diff_only={}'
                     .format(commit_confirm, confirm_timeout, persist_id, commit_replace, diff_only), extra=extra)
        self.commit_failure = False
        if persist_id is None:
            persist_id = self.default_persist_id
        if commit_replace:
            default_operation = 'replace'
        else:
            default_operation = 'merge'

        enclosure_queue = self.create_thread_queue(
            self._th_deploy_configs,
            commit_confirm=commit_confirm,
            persist_id=persist_id,
            confirm_timeout=confirm_timeout,
            diff_only=diff_only,
            default_operation=default_operation
        )

        for device in self.service:
            if device['last_commit_result'] == 'SUCCESS':
                target_config = etree.fromstring(self.config_last_running[device['device']])
                config_element = _copy_nc_data_to_config(target_config)
                device.update({'target_config': config_element})
                enclosure_queue.put(device)

        enclosure_queue.join()
