import os
import re
from icecream import ic

def get_profile_name(memory_total):
    total = int(memory_total)
    if total < 5500:
        return 'MIG 1g.5gb'
    elif total < 11000:
        return 'MIG 2g.10gb'
    elif total < 22000:
        return 'MIG 4g.20gb'
    else:
        return 'MIG 7g.40gb'

def get_gpu_info():
    gpu_info = {}
    smi = os.popen('nvidia-smi').read().split('\n')

    mode='gpu'

    mig_id = 0
    device_names = os.popen('nvidia-smi -L').read().split('\n')
    mig_names = [name for name in device_names if 'MIG' in name]
    gpu_names = [name for name in device_names if 'A100-SXM4-40GB' in name]

    for line in smi:
        if 'MIG devices' in line:
            mode = 'mig'

        # gpu 정보를 파싱
        if 'A100-SXM4-40GB' in line:
            line = line.replace('|', '').split()
            gpu_id = line[0]

        if '400W' in line:
            memory = re.findall('([0-9]+)MiB', line)
            uuid = re.findall('UUID: (GPU-[0-9a-z\-\/]+)', gpu_names[int(gpu_id)])[0]
            name = 'GPU %d: A100-SXM4-40GB' % int(gpu_id)
            if len(memory) > 0:
                used, total = memory[0], memory[1]
                gpu_info[name] = {'used': used, 'total': total, 'mig': {}, 'uuid': gpu_id}

            else:
                gpu_info[name] = {'used': 'N/A', 'total': 'N/A', 'mig': {}, 'uuid': gpu_id}

        # mig instance 정보를 파싱
        if mode == 'mig':
            memory = re.findall('([0-9]+)MiB', line)
            if len(memory) == 0:
                continue

            line = line.replace('|', '').split()
            if len(line) < 12:
                continue

            gpu_name = 'GPU %d: A100-SXM4-40GB' % int(line[0])
            used, total = memory[0], memory[1]
            name = mig_names[mig_id].split(':')[0].strip()
            uuid = re.findall('UUID: (MIG-GPU-[0-9a-z\-\/]+)', mig_names[mig_id])[0]
            mig_id += 1

            gpu_info[gpu_name]['mig'][name] = {
                'used': used,
                'total': total,
                'uuid': uuid
            }

    # mig 활성화된 device 가 있는 경우,
    # 활성화되지 않은 device 에서는 job 을 돌릴 수 없음
    if mode == 'mig':
        for gpu_name, gpu_status in gpu_info.items():
            gpu_info[gpu_name]['used'] = 'N/A'
            gpu_info[gpu_name]['total'] = 'N/A'

    return gpu_info

def get_idle_v2(n_devices=1, device_name='A100-SXM4-40GB', memory_used_less_than=300):
    assert device_name in [
        'A100-SXM4-40GB',
        '1g.5gb',
        '2g.10gb',
        '3g.20gb',
        '4g.20gb',
        '7g.40gb'
    ], 'The value of `device_name` should be one of "A100-SXM4-40GB", "1g.5gb", "2g.10gb", "3g.20gb", "4g.20gb", "7g.40gb".'

    gpu_info = get_gpu_info()

    idle_devices = []
    idle_devices_group = []
    for gpu_name, gpu_status in gpu_info.items():
        if device_name in gpu_name and \
            gpu_status['total'] != 'N/A' and \
            int(gpu_status['used']) < memory_used_less_than:

            idle_devices_group.append(gpu_status['uuid'])

        if len(idle_devices_group) == n_devices:
            idle_devices.append(','.join(idle_devices_group))
            idle_devices_group = []

        for mig_name, mig_status in gpu_status['mig'].items():
            if device_name in mig_name and \
                int(mig_status['used']) < memory_used_less_than:
                idle_devices_group.append(mig_status['uuid'])

            if len(idle_devices_group) == n_devices:
                idle_devices.append(','.join(idle_devices_group))
                idle_devices_group = []

    return idle_devices

def to_pretty(gpu_info):
    from socket import gethostname
    ret = '{}\n'.format(gethostname())
    for gpu_name, gpu_status in gpu_info.items():
        used = '{}MiB'.format(gpu_status['used']) if gpu_status['used'] != 'N/A' else gpu_status['used']
        total = '{}MiB'.format(gpu_status['total']) if gpu_status['total'] != 'N/A' else gpu_status['used']

        if used == 'N/A':
            ret += '{name: <25}\n'.format(name=gpu_name)
        else:
            ret += '{name: <25} | {used:9} / {total:9}\n'.format(name=gpu_name, used=used, total=total)

        for mig_name, mig_status in gpu_status['mig'].items():
            used = '{}MiB'.format(mig_status['used'])
            total = '{}MiB'.format(mig_status['total'])

            ret += '  {name: <23} | {used:9} / {total:9}\n'.format(name=mig_name, used=used, total=total)

    return ret

if __name__ == '__main__':
    get_gpu_info()

    idle = get_idle_v2(
        n_devices=2,
        # device_name='2g.10gb'
    )
