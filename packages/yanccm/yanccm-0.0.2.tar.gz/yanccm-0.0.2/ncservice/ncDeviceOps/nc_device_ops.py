# Notes for refactor
# operations should as far as possible be atomic operations
# The methods and classes should not store data other than for the current run/results
# Configuration rollback, configuration and execution history should be maintained elsewhere

from ncclient import manager
import os
import logging

USERNAME = os.environ['NCUSER']
PASSWORD = os.environ['NCPASS']
PORT = os.environ.get('NCPORT', 830)

logger = logging.getLogger('main.{}'.format(__name__))
extra = {'signature': '---SIGNATURE-NOT-SET---'}


class NcDeviceOps:
    def __init__(self, host, **kwargs):
        self.default_persist_id = '123456'
        self.host = host
        self.username = kwargs.get('username', USERNAME)
        self.password = kwargs.get('password', PASSWORD)
        self.port = kwargs.get('port', PORT)
        self.tid = kwargs.get('tid', 'N/A')
        try:
            logger.debug('TID-{}: host={}, port={}'
                         .format(self.tid, self.host, self.port), extra=extra)
            self.session = self.nc_connect(self.host)
        except Exception as e:
            logger.error("TID-{}: Unable to establish netconf connection for device {}. MSG: {}"
                         .format(self.tid, self.host, e), extra=extra)

    @staticmethod
    def _my_unknown_host_cb(host, fingerprint):
        # Just return true for unknown host fingerprint
        return True

    def nc_connect(self, host, allow_agent=False, look_for_keys=False, hostkey_verify=False):

        try:
            logger.debug('TID-{}: host={}, port={}'
                         .format(self.tid, self.host, self.port), extra=extra)
            m = manager.connect(
                host=host,
                username=self.username,
                password=self.password,
                port=self.port,
                allow_agent=allow_agent,
                look_for_keys=look_for_keys,
                hostkey_verify=hostkey_verify,
                unknown_host_cb=self._my_unknown_host_cb
            )
        except Exception as e:
            logger.error("TID-{}: Unable to establish netconf connection for device {}. MSG: {}"
                         .format(self.tid, self.host, e), extra=extra)
            return None

        return m

    def close_session(self):
        # We should consider supporting with statement
        self.session.close_session()

    def nc_get_configs(self, source='running'):
        try:
            _config = self.session.get_config(source=source, filter=('xpath', '/native')).data
        except Exception as e:
            logger.error("TID-{}: Unable to load config for device: {}. MSG: {}"
                         .format(self.tid, self.host, e), extra=extra)
            _config = None

        return _config

    def nc_get_candidate_config(self, config, default_operation=None):
        try:
            # Hitting bugs so disabling the running-config locks if we get disconnected
            # m.lock(target="running")
            self.session.lock(target="candidate")
            self.session.discard_changes()
            self.session.edit_config(config, format='xml', target='candidate', default_operation=default_operation)
            _candidate = self.session.get_config(source='candidate', filter=('xpath', '/native')).data
            self.session.discard_changes()
            self.session.unlock(target="candidate")
        except Exception as e:
            logger.error("TID-{}: Unable to create candidate configs for device {}. MSG: {}"
                         .format(self.tid, self.host, e), extra=extra)
            _candidate = None

        return _candidate

    def nc_deploy_configs(self, config, persist_id=None, commit_confirm=False, confirm_timeout=None,
                          default_operation='merge'):

        success = True
        if persist_id is None:
            persist_id = self.default_persist_id

        try:
            # Hitting bugs so disabling the running-config locks if we get disconnected
            # m.lock(target="running")
            self.session.lock(target="candidate")
            self.session.discard_changes()
            self.session.edit_config(config, format='xml', target='candidate', default_operation=default_operation)
        except Exception as e:
            logger.error("TID-{}: Unable to create candidate configs for device {}. MSG: {}"
                         .format(self.tid, self.host, e), extra=extra)

        if commit_confirm:
            logger.info('TID-{} Issuing confirmed-commit for: {}'.format(self.tid, self.host), extra=extra)
            try:
                self.session.commit(confirmed=True, persist=persist_id, timeout=str(confirm_timeout))
            except Exception as e:
                logger.error('TID-{} ERROR: {} for device {}'.format(self.tid, e, self.host), extra=extra)
                success = False
        else:
            logger.info('TID-{} Issuing commit for: {}'.format(self.tid, self.host), extra=extra)
            try:
                self.session.commit()
            except Exception as e:
                logger.error("TID-{}: Commit failed for device: {}. MSG: {}"
                             .format(self.tid, self.host, e), extra=extra)
                success = False
        try:
            # m.unlock(target="running")
            self.session.unlock(target="candidate")
        except Exception as e:
            logger.error('TID-{} Unable to unlock candidate/running config: {}. MSG: {}'.format(self.tid, self.host, e), extra=extra)
            success = False

        return success

    def nc_confirm_commit(self, persist_id=None):

        success = True
        if persist_id is None:
            persist_id = self.default_persist_id

        _commit_confirm_session = self.nc_connect(self.host)
        if _commit_confirm_session is None:
            return False

        try:
            logger.info('TID-{} Confirming commit for device: {}'.format(self.tid, self.host), extra=extra)
            _commit_confirm_session.commit(persist_id=persist_id)
        except Exception as e:
            logger.error("TID-{}: Commit confirm failed for device: {}. MSG: {}"
                         .format(self.tid, self.host, e), extra=extra)
            success = False

        return success

    def nc_discard_configs(self):
        logger.info('TID-{}: Discarding candidate configs on device: {}'.format(self.tid, self.host), extra=extra)
        _discard_config_session = self.nc_connect(self.host)
        if _discard_config_session is None:
            logger.error('TID-{}: Unable to connect to device: {}'.format(self.tid, self.host), extra=extra)
            return None

        try:
            logger.info('TID-{}: Discard candidate configs for device: {}'.format(self.tid, self.host), extra=extra)
            _discard_config_session.lock(target="candidate")
            _candidate = _discard_config_session.get_config(source='candidate', filter=('xpath', '/native')).data
            _discard_config_session.discard_changes()
        except Exception as e:
            logger.error('TID-{}: Discard candidate configs for device: {}'.format(self.tid, self.host), extra=extra)
            logger.error('TID-{}: Error MSG: {}'.format(self.tid, e), extra=extra)
            return None

        return _candidate
