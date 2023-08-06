from . import resources
from .common import *


def create(istack):

    def _get_rec_info(record, rtype):
        r = {}
        param = record.split('.')
        r['stack'] = param[0]
        r['role'] = param[1]
        r['type'] = rtype
        if rtype == 'external':
            r['region'] = param[2]
            r['domain'] = '.'.join(param[3:6])
        if rtype == 'internal':
            r['domain'] = '.'.join(param[2:5])
        if rtype == 'cf':
            del r['stack']
            r['role'] = param[0]
            r['domain'] = '.'.join(param[2:5])

        if istack.cfg.suffix and rtype != 'cf':
            r['role'] = r['role'] + '-' + istack.cfg.suffix

        return r

    def _get_record_type(zoneid, name):
        resp = istack.route53.list_resource_record_sets(
            HostedZoneId=zoneid,
            StartRecordName=name,
            MaxItems='1',
        )

        if resp['ResourceRecordSets']:
            return resp['ResourceRecordSets'][0]['Type']
        else:
            return 'A'

    def _get_record_change(name, zoneid, target, rtype):
        changes = {
            'Action': 'UPSERT',
            'ResourceRecordSet': {
                'Name': name,
                'Type': rtype,
                'AliasTarget': {
                    'HostedZoneId': zoneid,
                    'DNSName': target,
                    'EvaluateTargetHealth': False
                }
            }
        }

        return changes

    def _get_zoneid(record):
        zones = istack.route53.list_hosted_zones_by_name(
            DNSName=record['domain'])['HostedZones']
        for z in zones:
            zoneid = z['Id'].split('/')[2]
            zone = istack.route53.get_hosted_zone(Id=zoneid)
            if zone['HostedZone']['Name'] != record['domain'] + '.':
                continue
            try:
                zone_region = zone['VPCs'][0]['VPCRegion']
            except Exception:
                return zoneid
            else:
                if zone_region == istack.boto3.region_name:
                    return zoneid

    istack.cfg.RESOURCES_MAP = istack.cfg.RESOURCES_MAP_R53
    res = resources.get(istack)
    pprint(res)
    out = {}
    for r, v in res.items():
        r_out = {}
        if r.startswith('RecordSetExternal'):
            record = _get_rec_info(v, 'external')
            record_region = '%s.%s.%s' % (
                record['role'], record['region'], record['domain'])
            record_origin = '%s.origin.%s' % (
                record['role'], record['domain'])
            record_cf = '%s.%s' % (
                record['role'], record['domain'])
            map_record = {
                record_region: v,
            }

            if 'RecordSetCloudFront' not in res:
                map_record[record_cf] = record_region

            if not istack.cfg.noorigin:
                map_record[record_origin] = record_region

        if r.startswith('RecordSetInternal'):
            record = _get_rec_info(v, 'internal')
            record_internal = record['role'] + '.' + record['domain']
            map_record = {
                record_internal: v,
            }

        if r == 'RecordSetCloudFront':
            record = _get_rec_info(v, 'cf')
            record_cf = record['role'] + '.' + record['domain']
            map_record = {
                record_cf: v,
            }

        zoneid = _get_zoneid(record)

        for name, target in map_record.items():
            rtype = _get_record_type(zoneid, target)
            changes = _get_record_change(name, zoneid, target, rtype)
            print(name)
            pprint(changes)
            print('')

            if istack.cfg.dryrun:
                continue

            resp = istack.route53.change_resource_record_sets(
                HostedZoneId=zoneid,
                ChangeBatch={'Changes': [changes]}
            )
            pprint(resp['ChangeInfo']['Status'])

            r_out[name] = target

        out[r] = r_out

    return out
