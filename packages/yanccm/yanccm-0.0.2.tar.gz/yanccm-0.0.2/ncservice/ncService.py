import uuid
from difflib import context_diff
import logging
import threading
from lxml import etree
from ncservice.ncDeviceOps.threaded.get_configs import GetConfigs
from ncservice.ncDeviceOps.threaded.deploy_configs import DeployConfigs
from ncservice.ncDeviceOps.threaded.get_candidate_configs import GetCandidateConfigs
from ncservice.ncDeviceOps.threaded.confirm_commit import ConfirmCommit
from ncservice.ncDeviceOps.threaded.discard_configs import DiscardConfigs
from ncservice.configDb.configdb import ConfigDb
from ncservice.ncDeviceOps import helpers

nc_xmlns = "urn:ietf:params:xml:ns:netconf:base:1.0"
logger = logging.getLogger('main.{}'.format(__name__))
extra = {'signature': '---SIGNATURE-NOT-SET---'}


class JobResults:
    def __init__(self, job_id, manifest):
        self.service = manifest['service']
        self.report = {}
        self.task = {}
        self._initialize_job_report()

    def _initialize_job_report(self):
        self.report.update({'last_run': 'never', 'result': 'NOT_RUN', 'ref_configs': {}, 'task': self.task})
        for device in self.service:
            hostname = device['device']
            ref_config = ConfigDb.get_device_ref_configs(hostname)
            self.report['ref_configs'].update({hostname: ref_config})
        logger.debug('Initialise job results: {}'.format(self.report), extra=extra)

    def update_device_config_records(self, device, config, record):
        self.report[device][record] = self.stringify_etree(config)

    def update_config_db(self, target='current_running_configs'):
        _config = self.report['task'][target]
        ConfigDb.update_device_configs(_config)

    def get_device_config_records(self, target=None):
        if target is None:
            return self.report
        else:
            return self.report['task'][target]

    def get_config_diffs(self, original='original_running_configs', target='target_running_configs'):
        diffs = {}
        for device in self.service:
            if original == 'ref_configs':
                _original = self.report['ref_configs'][device['device']]
            else:
                _original = self.report['task'][original][device['device']]
            _target = self.report['task'][target][device['device']]
            _device_diffs = self._diff_config_str(_original, _target)
            diffs.update({device['device']: _device_diffs})

        return diffs

    @staticmethod
    def _diff_config_str(original, target):
        _config_diff = '\n'.join(context_diff(original.splitlines(),
                                              target.splitlines()))
        return _config_diff

    @staticmethod
    def stringify_etree(xml_etree):
        return etree.tostring(xml_etree, pretty_print=True).decode()

    # def _initialize_last_configs(self):
    #     last_configs = {}
    #     for device in self.service:
    #         last_configs.update({device['device']: 'NOT_RUN'})
    #     logger.debug('Initialise last configs: {}'.format(last_configs), extra=extra)
    #     return last_configs
    #
    # def _update_config_history(self, device, config):
    #     _raw_config = self.stringify_etree(config)
    #     self.config_last_running[device] = _raw_config
    #
    #
    # @staticmethod
    # def _copy_nc_data_to_config(xml_etree):
    #     native = xml_etree.getchildren()
    #     config_element = etree.Element("{" + nc_xmlns + "}config", nsmap={'nc': nc_xmlns})
    #     for elem in native:
    #         config_element.append(elem)
    #     return etree.tostring(config_element).decode()
    #


class Job:
    def __init__(self, manifest, threaded=True, thread_count=10):
        logger.debug('Initialising job results', extra=extra)
        self.job_uuid = str(uuid.uuid4())
        self.results = JobResults(self.job_uuid, manifest)
        self.manifest = manifest
        self.job_name = self.manifest['name']
        self.job_action = self.manifest['action']
        self.service = self.manifest['service']
        self._join_device_configs()
        self.threaded = threaded
        self.thread_count = thread_count
        self.thread_lock = threading.Lock()
        logger.debug('Service config: {}'.format(self.service), extra=extra)

    def _join_device_configs(self):
        # Optimise multiple configuration elements into a single configuration for each device
        logger.debug('Merging device configuration elements into a single', extra=extra)
        for device in self.service:
            if 'config' in device.keys():
                if type(device['config']) == list:
                    device['config'] = self._join_configs(device['config'])

    @staticmethod
    def _join_configs(configs_list):
        _config_trees = []
        for _config in configs_list:
            root = etree.fromstring(_config)
            if '{}config'.format(nc_xmlns) == root.tag:
                body = root.getchildren()
                _config_trees.append(body)
            else:
                logger.error(
                    'all configs must be contained in config element with nc namespace tag {}'.format(nc_xmlns),
                    extra=extra)
        config_element = etree.Element("{" + nc_xmlns + "}config", nsmap={'nc': nc_xmlns})
        for _tree in _config_trees:
            # Usually we only expect a single element tree but it is still of type list
            for elem in _tree:
                config_element.append(elem)
        return etree.tostring(config_element).decode()

    def get_configs(self):
        if self.threaded:
            _task = GetConfigs(self.service)
            _task_results = _task.get_configs()
        else:
            _task_results = {}

        self.results.task.update(_task_results.report)

    def get_candidate_configs(self):
        if self.threaded:
            _task = GetCandidateConfigs(self.service)
            _task_results = _task.get_candidate_configs()
        else:
            _task_results = {}

        self.results.task.update(_task_results.report)

    def deploy_configs(self,
                       commit_confirm=False,
                       confirm_timeout=30,
                       commit_replace=False,
                       merge_configs=True
                       ):
        persist_id = self.job_uuid

        if self.threaded:
            _task = DeployConfigs(self.service)
            _task_results = _task.deploy_configs(
                commit_confirm=commit_confirm,
                confirm_timeout=confirm_timeout,
                persist_id=persist_id,
                commit_replace=commit_replace,
                merge_configs=merge_configs
            )
        else:
            _task_results = {}

        if _task_results.report['commit_failure']:
            logger.error('Commit failed on one or more devices', extra=extra)
            if self.threaded and commit_confirm:
                logger.info('Waiting for confirm_commit={} timeout before discarding candidate configs'
                            .format(commit_confirm), extra=extra)
                _discard = DiscardConfigs(self.service)
                _discard_result = _discard.discard_configs()
                logger.debug('discard config task report: {}'.format(_discard_result), extra=extra)
        elif commit_confirm:
            if self.threaded:
                _confirm = ConfirmCommit(self.service)
                _confirm.confirm_commit(persist_id=persist_id)

        self.results.task.update(_task_results.report)

    def revert_ref_configs(self):
        for device in self.service:
            # ToDo This needs tidying up
            _config = helpers._copy_nc_data_to_config(etree.fromstring(self.results.report['ref_configs'][device['device']]))
            device.update({'config': {}})
            device['config'] = _config

        self.deploy_configs(commit_confirm=True, commit_replace=True)

    # def confirm_commit(self, persist_id=None):
    #     if persist_id is None:
    #         persist_id = self.job_uuid
    #
    #     logger.debug('Requesting thread queue for _th_confirm_commit', extra=extra)
    #     logger.debug('persist_id={}'
    #                  .format(persist_id), extra=extra)
    #     enclosure_queue = self.create_thread_queue(
    #         self._th_confirm_commit,
    #         persist_id=persist_id
    #     )
    #
    #     for device in self.service:
    #         enclosure_queue.put(device)
    #
    #     enclosure_queue.join()
    #
    # def _th_confirm_commit(self, tid, queue,
    #                        persist_id=None):
    #     persist_id = persist_id
    #     while True:
    #         target_device = queue.get()
    #         device_name = target_device['device']
    #         host = target_device['host']
    #         port = target_device.get('ncport', 830)
    #         session = NcDeviceOps(host, port=port, tid=tid)
    #         result = session.nc_confirm_commit(persist_id=persist_id)
    #         if not result:
    #             logger.error(
    #                 'TID-{} Failed to confirm commit configs for device {}'.format(tid, device_name))
    #         else:
    #             current_config = session.nc_get_configs()
    #             self._update_device_config_records(device_name, current_config, 'current_running_configs')
    #         session.close_session()
    #         queue.task_done()

    # def discard_configs(self):
    #     logger.debug('Requesting thread queue for _th_discard_configs', extra=extra)
    #     enclosure_queue = self.create_thread_queue(
    #         self._th_discard_configs
    #     )
    #
    #     for device in self.service:
    #         enclosure_queue.put(device)
    #
    #     enclosure_queue.join()
    #
    # def _th_discard_configs(self, tid, queue):
    #     while True:
    #         target_device = queue.get()
    #         device_name = target_device['device']
    #         host = target_device['host']
    #         port = target_device.get('ncport', 830)
    #
    #         session = NcDeviceOps(host, port=port, tid=tid)
    #         result = session.nc_discard_configs()
    #         if not result:
    #             logger.error('TID-{} Failed to discard configs for device: {}'.format(tid, device_name), extra=extra)
    #         else:
    #             logger.info('TID-{} Configs successfully discarded for device: {}'.format(tid, device_name), extra=extra)
    #
    #         session.close_session()
    #         queue.task_done()

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
            persist_id = self.job_uuid
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
    # def commit(self, commit_confirm=True, confirm_timeout=10):
    #     logger.info('Deploying service with commit MERGE, commit_confirm={} and confirm_timeout={} seconds'.format(
    #         commit_confirm, confirm_timeout), extra=extra)
    #     # Should we return commit fail and test on this rather than inheriting attributes?
    #     self.service.deploy_configs(commit_confirm=commit_confirm, confirm_timeout=confirm_timeout, persist_id=self.job_uuid)
    #
    #     if self.service.commit_failure:
    #         logger.error('Config deploy failed on one or more devices', extra=extra)
    #         logger.error('Not sending commit-confirm to any devices', extra=extra)
    #         logger.info('Waiting for commit timeout before clearing candidate DS', extra=extra)
    #         time.sleep(confirm_timeout)
    #         self.service.discard_configs()
    #         return
    #     else:
    #         logger.info('Sending commit-confirm to all devices', extra=extra)
    #         self.service.confirm_commit(persist_id=self.job_uuid)
    #
    # def commit_replace(self, commit_confirm=True, confirm_timeout=10):
    #     logger.info('Deploying service with commit REPLACE, commit_confirm={} and confirm_timeout={} seconds'.format(
    #         commit_confirm, confirm_timeout), extra=extra)
    #     self.service.deploy_configs(commit_confirm=commit_confirm, confirm_timeout=confirm_timeout, persist_id=self.job_uuid, commit_replace=True)
    #
    #     if self.service.commit_failure:
    #         logger.error('Config deploy failed on one or more devices', extra=extra)
    #         logger.error('Not sending commit-confirm to any devices', extra=extra)
    #         logger.info('Waiting for commit timeout before clearing candidate DS', extra=extra)
    #         time.sleep(confirm_timeout)
    #         self.service.discard_configs()
    #         return
    #     else:
    #         logger.info('Sending commit-confirm to all devices', extra=extra)
    #         self.service.confirm_commit(persist_id=self.job_uuid)
    #
    # # This is only useful whilst the job has run and is still loaded.  Perhaps Rollback should be implemented at the
    # # controller layer using configs from the DB?
    # def rollback(self, commit_confirm=True, confirm_timeout=10):
    #     logger.info('Issuing ROLLBACK to last known configs, commit_confirm={} and confirm_timeout={} seconds'.format(
    #         commit_confirm, confirm_timeout), extra=extra)
    #     logger.warning('Applying device configurations stored before changes made by this job.  Other changes will be '
    #                    'overwritten', extra=extra)
    #     self.service.rollback(commit_confirm=commit_confirm, confirm_timeout=confirm_timeout, persist_id=self.job_uuid)
    #
    #     if self.service.commit_failure:
    #         logger.error('Config deploy failed on one or more devices', extra=extra)
    #         logger.error('Not sending commit-confirm to any devices', extra=extra)
    #         logger.info('Waiting for commit timeout before clearing candidate DS', extra=extra)
    #         time.sleep(confirm_timeout)
    #         self.service.discard_configs()
    #         return
    #     else:
    #         logger.info('Sending commit-confirm to all devices', extra=extra)
    #         self.service.confirm_commit(persist_id=self.job_uuid)
    #
    # def diff(self):
    #     logger.info('Calculating service config diffs. No commit requested', extra=extra)
    #     self.service.deploy_configs(diff_only=True)

    # def get_configs(self):
    #     logger.info('Fetching current configs for device set', extra=extra)
    #     self.service.get_configs()

#
# class BaseThreadClass:
#
#     @staticmethod
#     def create_thread_queue(func, thread_count=10, **kwargs):
#         enclosure_queue = Queue()
#         logger.debug('Initialising thread queue with thread count {}'.format(thread_count), extra=extra)
#         for i in range(thread_count):
#             thread = threading.Thread(target=func, args=(i, enclosure_queue), kwargs=kwargs)
#             thread.setDaemon(True)
#             thread.start()
#
#         return enclosure_queue
#
#
# class TestMe(BaseThreadClass):
#     def __init__(self, job_id, manifest):
#         super().__init__()
#         self.service = manifest['service']
#         self.results = JobResults(job_id, manifest)
#
#     def get_configs(self):
#         logger.debug('Requesting thread queue for _th_read_configs', extra=extra)
#         enclosure_queue = self.create_thread_queue(
#             self._th_read_configs
#         )
#
#         for device in self.service:
#             enclosure_queue.put(device)
#
#         enclosure_queue.join()
#         return self.results
#
#     def _th_read_configs(self, tid, queue):
#         while True:
#             target_device = queue.get()
#             device_name = target_device['device']
#             host = target_device['host']
#             port = target_device.get('ncport', 830)
#
#             session = NcDeviceOps(host, port=port, tid=tid)
#             current_config = session.nc_get_configs()
#             if current_config is not None:
#                 self.results.update_device_config_records(device_name, current_config, 'original_running_configs')
#             else:
#                 logger.error('TID-{}: Unable to retrieve config for device: {}'
#                              .format(tid, device_name), extra=extra)
#                 queue.task_done()
#                 continue
#
#             session.close_session()
#             queue.task_done()
