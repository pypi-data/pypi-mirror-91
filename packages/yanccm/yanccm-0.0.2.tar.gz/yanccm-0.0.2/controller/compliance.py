import logging
from ncservice.ncService import Job
from view.view import CliOutput
from sot.sot import DevicesDb
from sot.sot import Templates

logger = logging.getLogger('main.{}'.format(__name__))
extra = {'signature': '---SIGNATURE-NOT-SET---'}


def get_device_set(args):
    if args.site:
        return DevicesDb(site=args.site)
    elif args.device:
        return DevicesDb(name=args.device)


class Compliance:
    def __init__(self, args):
        self.compliance(args)

    @staticmethod
    def add_args(_key, _subparsers):
        compliance = _subparsers.add_parser(_key, help='use yanccm compliance -h for help')
        compliance.add_argument('--site', help='sub-command1 help')
        compliance.add_argument('--device', help='sub-command2 help')
        compliance.add_argument('--baseline', help='sub-command2 help')
        compliance.add_argument('--revert', help='sub-command2 help')
        day0 = compliance.add_subparsers(help='sub-command help')
        day0 = ComplianceDay0.add_args('day0', day0)
        day0.set_defaults(func=ComplianceDay0)
        return compliance

    @staticmethod
    def compliance(args):
        logger.info('Running configuration compliance against configDB with filter site={}, device={}'
                    .format(args.site, args.device), extra=extra)
        devices_db = get_device_set(args)
        _manifest = {}
        _manifest.update({'name': 'Change compliance test for site={}'.format(args.site)})
        _manifest.update({'service': devices_db.get_devices_management()})
        _manifest.update({'action': 'diff'})
        _job = Job(_manifest)
        _job.get_configs()
        if args.baseline:
            _job.results.update_config_db()
        elif args.revert:
            _job.revert_ref_configs()
        else:
            CliOutput.print_diffs(_job.results.get_config_diffs(original='ref_configs', target='original_running_configs'))


class ComplianceDay0:
    def __init__(self, args):
        self.compliance_day0(args)

    @staticmethod
    def add_args(_key, _subparsers):
        day0 = _subparsers.add_parser(_key, help='use yanccm compliance day0 -h for help')
        day0.add_argument('--site', required=True, help='sub-command1 help')
        day0.add_argument('--device', help='sub-command2 help')
        day0.add_argument('--commit', help='sub-command2 help')
        return day0

    @staticmethod
    def compliance_day0(args):
        logger.info('Running configuration compliance against Day0 template with filter site={}, device={}'
              .format(args.site, args.device), extra=extra)
        devices_db = get_device_set(args)
        _manifest = {}
        _manifest.update({'name': 'Day0 Compliance test for site={}'.format(args.site)})
        day0 = Templates.generate_day0(devices_db.devices)
        _manifest.update({'service': day0})
        _manifest.update({'action': 'diff'})
        _job = Job(_manifest)
        if args.commit:
            _job.deploy_configs(commit_confirm=True)
        else:
            _job.get_candidate_configs()
            CliOutput.print_diffs(_job.results.get_config_diffs())