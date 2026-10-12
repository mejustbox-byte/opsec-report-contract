import copy,json,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from opsec_reports.core import ReportError,make_report,validate,compare,render,load,write_new,outcome
from opsec_reports.adapters import result,guard,ad
ROOT=Path(__file__).resolve().parents[1]

def report(status='fail',asset='synthetic-asset',version='1',scope='synthetic-scope'):
 return make_report('synthetic-producer',version,'synthetic-rules',scope,'2026-10-12T00:00:00Z',True,[result('CHECK-001',asset,status,'high' if status=='fail' else 'info')])

class ReportTests(unittest.TestCase):
 def test_all_four_states(self):
  for status,code in [('pass',0),('fail',1),('not_tested',2),('not_applicable',0)]:self.assertEqual(outcome(report(status)),code)
 def test_empty_is_not_clean(self):
  r=make_report('producer','1','rules','scope','2026-10-12T00:00:00Z',True,[]);self.assertEqual(outcome(r),2);self.assertEqual(r['coverage_gaps'][0]['code'],'empty_scope')
 def test_bad_schema_types_fields_redaction(self):
  for key,value in [('schema_version','other'),('coverage_complete',1),('results',{}),('summary',{}),('extra','SECRET')]:
   r=report();r[key]=value
   with self.assertRaises(ReportError):validate(r)
  r=report();r['results'][0]['evidence']['redacted']=False
  with self.assertRaises(ReportError):validate(r)
 def test_summary_coverage_duplicates(self):
  for mutation in ('summary','coverage','duplicate'):
   r=report()
   if mutation=='summary':r['summary']['fail']=0
   elif mutation=='coverage':r['coverage_complete']=False
   else:r['results'].append(copy.deepcopy(r['results'][0]));r['summary']['fail']=2
   with self.assertRaises(ReportError):validate(r)
 def test_invalid_dates(self):
  for date in ['2026-02-30T00:00:00Z','yesterday','2026-10-12T00:00:00+05:00']:
   r=report();r['run']['observed_at']=date
   with self.assertRaises(ReportError):validate(r)
 def test_diff_missing_is_not_fix(self):
  self.assertEqual({c['change'] for c in compare(report(),report(asset='different'))['changes']},{'added','not_observed'})
 def test_diff_explicit_pass_and_coverage_loss(self):
  self.assertEqual(compare(report(),report('pass'))['changes'][0]['change'],'explicitly_passed');self.assertEqual(compare(report(),report('not_tested'))['changes'][0]['change'],'coverage_lost')
 def test_diff_incomparable_producer_scope(self):
  for b in [report(version='2'),report(scope='other')]:self.assertFalse(compare(report(),b)['comparable'])
 def test_html_escaped_no_network_elements(self):
  r=report(asset='<script>alert(1)</script>');r['results'][0]['message']='<img src="https://secret.invalid" onerror="alert(1)">';h=render(r)
  self.assertNotIn('<script>',h);self.assertNotIn('<img ',h);self.assertIn('&lt;script&gt;',h);self.assertIn('default-src',h)
  with patch('socket.socket',side_effect=AssertionError('network')):validate(r);render(r)
 def test_loader_strict_json_and_budget(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'input.json'
   for data in [b'{"x":1,"x":2}',b'{"x":NaN}',b'\xff',b'{} {}',b'[['*65+b']]'*65]:
    p.write_bytes(data)
    with self.assertRaises(ReportError):load(p)
   p.write_text('{}')
   with patch('opsec_reports.core.MAX_BYTES',1):
    with self.assertRaises(ReportError):load(p)
 def test_symlink_and_new_output(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'existing';p.write_text('original');link=Path(tmp)/'link';link.symlink_to(p)
   with self.assertRaises(ReportError):load(link)
   with self.assertRaises(ReportError):write_new(p,'changed')
   self.assertEqual(p.read_text(),'original')
 def test_guard_adapter_preserves_gaps_without_pass_inference(self):
  data=json.loads((ROOT/'examples/guard-source.synthetic.json').read_text());r=guard(data,'scope','2026-10-12T00:00:00Z',True)
  self.assertEqual(outcome(r),1);self.assertFalse(r['coverage_complete']);self.assertEqual(r['summary']['pass'],0)
  data['findings']=[];self.assertEqual(outcome(guard(data,'scope','2026-10-12T00:00:00Z',True)),2)
 def test_ad_actual_producer_fixture_and_unknown_mapping(self):
  data=json.loads((ROOT/'examples/ad-source.synthetic.json').read_text());r=ad(data);self.assertEqual(r['summary']['pass'],9);self.assertEqual(outcome(r),0)
  data['results'][0].update(status='not_run',coverage='none',evidence_refs=[]);data['summary']['pass']=8;data['summary']['not_run']=1
  r=ad(data);self.assertEqual(r['summary']['not_tested'],1);self.assertEqual(outcome(r),2)
 def test_source_invalid_not_silently_accepted(self):
  data=json.loads((ROOT/'examples/ad-source.synthetic.json').read_text());data['summary']['pass']=0
  with self.assertRaises(ReportError):ad(data)
  data=json.loads((ROOT/'examples/guard-source.synthetic.json').read_text());data['coverage_complete']=False
  with self.assertRaises(ReportError):guard(data,'scope','2026-10-12T00:00:00Z',True)
 def test_cli_codes_and_output(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'report.json'
   for status,code in [('pass',0),('fail',1),('not_tested',2)]:
    p.write_text(json.dumps(report(status)));r=subprocess.run([sys.executable,'-m','opsec_reports','validate',str(p)],cwd=ROOT,capture_output=True,text=True,timeout=20);self.assertEqual(r.returncode,code,r.stdout+r.stderr)
   p.write_text('{"SECRET_KEY":NaN}');r=subprocess.run([sys.executable,'-m','opsec_reports','validate',str(p)],cwd=ROOT,capture_output=True,text=True,timeout=20);self.assertEqual(r.returncode,3);self.assertNotIn('SECRET',r.stdout+r.stderr)
 def test_result_cap(self):
  r=report();r['results']*=10001
  with self.assertRaises(ReportError):validate(r)

if __name__=='__main__':unittest.main()
