"""Explicit, lossy adapters; no inferred pass from an absent source finding."""
from collections import Counter
import hashlib
import json
from pathlib import Path
from .core import ReportError, make_report, STATUSES, validator


def result(check,asset,status,severity,refs=()):
    return {'check_id':check,'asset_id':asset,'status':status,'severity':severity,
            'message':'Status normalized from the declared source report; evidence is not authenticated.',
            'remediation':'Review the source product remediation guidance and evidence locally.',
            'evidence':{'redacted':True,'refs':list(refs)}}


def guard(data,scope,observed_at,synthetic):
    from jsonschema import Draft202012Validator
    from referencing import Registry
    from referencing.exceptions import NoSuchResource
    def deny(uri):raise NoSuchResource(ref=uri)
    schema=json.loads(Path(__file__).with_name('guard-response-0.2.schema.json').read_text(encoding='utf-8'))
    if not Draft202012Validator(schema,registry=Registry(retrieve=deny)).is_valid(data) or 'findings' not in data:raise ReportError('source_guard_invalid')
    if (data['coverage_complete']!=(not data['coverage_gaps'] and not data['exclusions'])
       or (data['files_inspected']==0)!=any(g['reason']=='empty_scope' for g in data['coverage_gaps'])
       or data['files_inspected']>data['files_encountered']
       or data['files_encountered']>data['limits']['max_files']
       or data['bytes_read']>data['limits']['max_total_bytes']
       or len(data['findings'])>data['limits']['max_findings']):raise ReportError('source_guard_inconsistent')
    stop_reasons={'file_count_limit','total_bytes_limit','finding_count_limit','directory_count_limit'}
    if data['scan_stopped']!=any(g['reason'] in stop_reasons for g in data['coverage_gaps']):raise ReportError('source_guard_stop_mismatch')
    groups={}
    for f in data['findings']:
        key=(f['check_id'],f['asset_id']);record=groups.setdefault(key,result(*key,'fail',f['severity']))
        ref='line:'+str(f['evidence']['line'])
        if ref not in record['evidence']['refs']:
            if len(record['evidence']['refs'])>=128:raise ReportError('source_evidence_ref_limit')
            record['evidence']['refs'].append(ref)
    gaps=[{'code':'guard_'+g['reason'],'message':'Source declared incomplete coverage.'} for g in data['coverage_gaps']]
    gaps += [{'code':'guard_exclusion','message':'Source excluded a directory.'} for _ in data['exclusions']]
    # Finding-only source format cannot enumerate every performed check/asset combination.
    gaps.append({'code':'finding_only_source','message':'Source exposes findings, not explicit per-check passes; missing findings are not normalized as pass.'})
    return make_report('publication-opsec-guard',data['tool_version'],'response-0.2-five-rules',scope,observed_at,synthetic,list(groups.values()),gaps)


def ad(data):
    try:
        if type(data['report_schema_version']) is not int or data['report_schema_version']!=1 or not isinstance(data['results'],list) or len(data['results'])>10000:raise ReportError('source_ad_invalid')
        if any(type(data['summary'].get(s)) is not int for s in ('pass','fail','unknown','not_run')):raise ReportError('source_ad_summary_invalid')
        evidence_ids=[e['id'] for e in data['evidence']]
        if any(not isinstance(x,str) for x in evidence_ids) or len(set(evidence_ids))!=len(evidence_ids):raise ReportError('source_ad_evidence_invalid')
        counts=Counter(r['status'] for r in data['results'])
        if set(counts)-{'pass','fail','unknown','not_run'} or data['summary']!={s:counts[s] for s in ('pass','fail','unknown','not_run')}:raise ReportError('source_ad_summary_invalid')
        if not isinstance(data['input_sha256'],str) or len(data['input_sha256'])!=64 or any(c not in '0123456789abcdef' for c in data['input_sha256']):raise ReportError('source_ad_hash_invalid')
        records=[]
        for r in data['results']:
            status=r['status'] if r['status'] in ('pass','fail') else 'not_tested'
            if status in ('pass','fail') and (r['coverage']!='complete' or not r['evidence_refs']):raise ReportError('source_ad_coverage_invalid')
            if not isinstance(r['evidence_refs'],list) or len(r['evidence_refs'])>128 or any(not isinstance(x,str) for x in r['evidence_refs']) or not set(r['evidence_refs'])<=set(evidence_ids):raise ReportError('source_ad_refs_invalid')
            refs=['source-ref:'+hashlib.sha256(x.encode()).hexdigest() for x in sorted(set(r['evidence_refs']))]
            records.append(result(r['check_id'],data['scope'],status,r['severity'],refs))
        return make_report('ad-opsec-auditor',data['engine_version'],data['rules_version'],data['scope'],data['collected_at'],data['synthetic'],records,run_id='sha256:'+data['input_sha256'])
    except (KeyError,TypeError,AttributeError) as e:raise ReportError('source_ad_invalid') from e
