"""Versioned, offline OPSEC result contract and conservative comparison."""
import datetime
import html
import json
import os
from pathlib import Path
import re
import stat
from collections import Counter

VERSION='0.1.0a1'
SCHEMA_VERSION='opsec-1.0'
STATUSES=('pass','fail','not_tested','not_applicable')
MAX_BYTES=8_000_000
MAX_RESULTS=10000

class ReportError(ValueError): pass

def strict_object(pairs):
    out={}
    for k,v in pairs:
        if k in out:raise ReportError('duplicate_key')
        out[k]=v
    return out

def reject_constant(_):raise ReportError('invalid_number')

def load(path):
    path=Path(path)
    try:
        if path.is_symlink():raise ReportError('symlink_input')
        fd=os.open(path,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0)|getattr(os,'O_NONBLOCK',0))
        with os.fdopen(fd,'rb') as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):raise ReportError('not_regular')
            raw=stream.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES:raise ReportError('input_size_limit')
        text=raw.decode('utf-8');depth=0;quoted=escaped=False
        for c in text:
            if quoted:
                if escaped:escaped=False
                elif c=='\\':escaped=True
                elif c=='"':quoted=False
            elif c=='"':quoted=True
            elif c in '[{':
                depth+=1
                if depth>64:raise ReportError('input_depth_limit')
            elif c in ']}':depth-=1
        return json.loads(text,object_pairs_hook=strict_object,parse_constant=reject_constant)
    except (OSError,UnicodeError,json.JSONDecodeError,RecursionError,OverflowError) as e:
        raise ReportError('invalid_input') from e

def validator():
    from jsonschema import Draft202012Validator
    from referencing import Registry
    from referencing.exceptions import NoSuchResource
    def deny(uri):raise NoSuchResource(ref=uri)
    schema=json.loads(Path(__file__).with_name('report-1.0.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema,registry=Registry(retrieve=deny))

def validate(report):
    try:
        if next(validator().iter_errors(report),None) is not None:raise ReportError('schema_invalid')
        seen=set();counts=Counter(r['status'] for r in report['results'])
        for result in report['results']:
            key=(result['check_id'],result['asset_id'])
            if key in seen:raise ReportError('duplicate_result_identity')
            seen.add(key)
        if report['summary']!={s:counts[s] for s in STATUSES}:raise ReportError('summary_mismatch')
        complete=bool(report['results']) and not report['coverage_gaps'] and not counts['not_tested']
        if report['coverage_complete']!=complete:raise ReportError('coverage_mismatch')
        if not report['results'] and not any(g['code']=='empty_scope' for g in report['coverage_gaps']):raise ReportError('empty_scope_mismatch')
        datetime.datetime.fromisoformat(report['run']['observed_at'].replace('Z','+00:00'))
    except (ImportError,OSError,KeyError,TypeError,RecursionError) as e:raise ReportError('validation_unavailable') from e
    except ValueError as e:
        if isinstance(e,ReportError):raise
        raise ReportError('invalid_timestamp') from e
    return report

def outcome(report):
    validate(report)
    return 1 if report['summary']['fail'] else 2 if not report['coverage_complete'] else 0

def make_report(producer,version,ruleset,scope,observed_at,synthetic,results,gaps=(),run_id='local'):
    counts=Counter(r['status'] for r in results)
    report={'schema_version':SCHEMA_VERSION,'producer':{'name':producer,'version':version,'ruleset':ruleset},
            'run':{'id':run_id,'scope':scope,'observed_at':observed_at,'synthetic':synthetic},
            'coverage_complete':bool(results) and not gaps and not counts['not_tested'],
            'summary':{s:counts[s] for s in STATUSES},'results':results,'coverage_gaps':list(gaps)}
    if not results and not any(g['code']=='empty_scope' for g in gaps):
        report['coverage_gaps'].append({'code':'empty_scope','message':'No normalized result records.'})
    return validate(report)

def compare(before,after):
    validate(before);validate(after)
    reasons=[]
    for field in ('name','version','ruleset'):
        if before['producer'][field]!=after['producer'][field]:reasons.append('producer_'+field+'_changed')
    if before['run']['scope']!=after['run']['scope']:reasons.append('scope_changed')
    if before['run']['synthetic']!=after['run']['synthetic']:reasons.append('provenance_class_changed')
    if reasons:return {'schema_version':'opsec-diff-1.0','comparable':False,'reasons':reasons,'changes':[]}
    a={(r['check_id'],r['asset_id']):r for r in before['results']}
    b={(r['check_id'],r['asset_id']):r for r in after['results']};changes=[]
    for key in sorted(a.keys()|b.keys()):
        old,new=a.get(key),b.get(key)
        if old==new:continue
        if old is None:kind='added'
        elif new is None:kind='not_observed'
        elif old['status']=='fail' and new['status']=='pass':kind='explicitly_passed'
        elif old['status'] in ('pass','fail') and new['status']=='not_tested':kind='coverage_lost'
        else:kind='changed'
        changes.append({'check_id':key[0],'asset_id':key[1],'change':kind,
                        'before':old['status'] if old else None,'after':new['status'] if new else None})
    return {'schema_version':'opsec-diff-1.0','comparable':True,'reasons':[],
            'before_coverage_complete':before['coverage_complete'],'after_coverage_complete':after['coverage_complete'],'changes':changes}

def render(report):
    validate(report);escape=lambda s:html.escape(str(s),quote=True)
    rows=[]
    for r in report['results']:
        cells=[r['check_id'],r['asset_id'],r['status'],r['severity'],r['message'],r['remediation'],', '.join(r['evidence']['refs'])]
        rows.append('<tr>'+''.join('<td>'+escape(c)+'</td>' for c in cells)+'</tr>')
    gaps=''.join('<li>'+escape(g['code'])+': '+escape(g['message'])+'</li>' for g in report['coverage_gaps'])
    cards=''.join('<div><strong>'+str(report['summary'][s])+'</strong> '+s+'</div>' for s in STATUSES)
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; base-uri \'none\'; form-action \'none\'"><title>OPSEC report</title><style>body{font:16px system-ui;margin:2rem;color:#172338;background:#f6f8fb}h1{margin-bottom:.4rem}.cards{display:flex;gap:1rem;flex-wrap:wrap}.cards div{padding:1rem;background:white;border:1px solid #ccd5e0;border-radius:8px}table{border-collapse:collapse;width:100%;background:white;margin-top:1.5rem}td,th{padding:.7rem;border:1px solid #ccd5e0;text-align:left;overflow-wrap:anywhere}strong{font-size:1.3rem}section{overflow:auto}</style><h1>OPSEC report</h1><p>'+escape(report['producer']['name'])+' '+escape(report['producer']['version'])+' · '+escape(report['run']['scope'])+'</p><p>Coverage complete: '+str(report['coverage_complete']).lower()+' · Synthetic: '+str(report['run']['synthetic']).lower()+'</p><div class="cards">'+cards+'</div><h2>Coverage gaps</h2><ul>'+gaps+'</ul><section><table><thead><tr><th>Check</th><th>Asset</th><th>Status</th><th>Severity</th><th>Message</th><th>Remediation</th><th>Evidence refs</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></section><p>Declarations only. Report validity does not authorize publication or authenticate evidence.</p></html>'

def write_new(path,text):
    path=Path(path)
    if path.is_symlink():raise ReportError('output_exists_or_symlink')
    try:
        with path.open('x',encoding='utf-8') as stream:stream.write(text)
    except OSError as e:raise ReportError('output_unavailable') from e
