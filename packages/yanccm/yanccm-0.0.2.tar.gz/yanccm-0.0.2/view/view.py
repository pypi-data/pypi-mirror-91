import tabulate

class CliOutput:

    @staticmethod
    def compliance_report(task_results):
        rows = []
        for device, result in task_results.items():
            rows.append([device, result])

    @staticmethod
    def print_diffs(job_config_diff, no_diff_msg='COMPLIANT'):
        for device, diff in job_config_diff.items():
            if len(diff) > 0:
                print(' {} '.format(device).center(60, '@'))
                print(diff)
            else:
                print('Device: {} - {} (no diffs found)'.format(device, no_diff_msg))

        return
