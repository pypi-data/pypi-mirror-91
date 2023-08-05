import logging
import yaml
from ncservice.ncService import Job
from view.view import CliOutput
from sot.sot import DevicesDb

logger = logging.getLogger('main.{}'.format(__name__))
extra = {'signature': '---SIGNATURE-NOT-SET---'}


class JobFile:
    def __init__(self, args):
        self.job(args)

    @staticmethod
    def add_args(_key, _subparsers):
        job = _subparsers.add_parser(_key, help='use yanccm job -h for help')
        job.add_argument('file', help='File containing yanccm Job definition')
        return job

    @staticmethod
    def job(args):
        logger.info('Running Job from file {}'.format(args.file), extra=extra)
        with open(args.file) as file:
            _manifest = yaml.load(file, Loader=yaml.FullLoader)

        device_query = []
        for device in _manifest['service']:
            device_query.append(('name', device['device']))

        devices_db = DevicesDb(device_query)
        _manifest = devices_db.update_job_with_device_mgmt(_manifest)
        _job = Job(_manifest)

        if _manifest.get('action') == 'diff':
            _job.get_candidate_configs()
            CliOutput.print_diffs(_job.results.get_config_diffs())
        elif _manifest.get('action') == 'commit':
            _job.deploy_configs(commit_confirm=True, confirm_timeout=10)
