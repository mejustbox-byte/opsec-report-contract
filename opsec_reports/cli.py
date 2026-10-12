import argparse
import json
import sys
from .core import VERSION, ReportError, load, validate, outcome, compare, render, write_new
from . import adapters


def main():
    parser=argparse.ArgumentParser(description='Offline OPSEC contract, validation, conservative comparison and HTML.')
    parser.add_argument('--version',action='version',version=VERSION)
    commands=parser.add_subparsers(dest='command',required=True)
    p=commands.add_parser('validate');p.add_argument('input')
    p=commands.add_parser('diff');p.add_argument('before');p.add_argument('after');p.add_argument('--output')
    p=commands.add_parser('html');p.add_argument('input');p.add_argument('--output',required=True)
    p=commands.add_parser('normalize');p.add_argument('source',choices=['guard','ad']);p.add_argument('input');p.add_argument('--output',required=True)
    p.add_argument('--scope');p.add_argument('--observed-at');p.add_argument('--synthetic',action='store_true')
    args=parser.parse_args()
    try:
        if args.command=='validate':
            report=validate(load(args.input));code=outcome(report)
            payload={'valid':True,'inspection_exit_code':code}
        elif args.command=='diff':
            payload=compare(load(args.before),load(args.after));code=0 if payload['comparable'] else 2
        elif args.command=='html':
            report=load(args.input);write_new(args.output,render(report));payload={'written':True};code=outcome(report)
        else:
            data=load(args.input)
            if args.source=='guard':
                if not args.scope or not args.observed_at:raise ReportError('guard_context_required')
                report=adapters.guard(data,args.scope,args.observed_at,args.synthetic)
            else:report=adapters.ad(data)
            write_new(args.output,json.dumps(report,ensure_ascii=False,indent=2)+'\n');payload={'written':True};code=outcome(report)
        if args.command=='diff' and args.output:write_new(args.output,json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
        else:print(json.dumps(payload,ensure_ascii=True,indent=2))
        return code
    except ReportError as error:
        # ReportError messages are static codes only; never source data or paths.
        print(json.dumps({'valid':False,'error':str(error)}));return 3
    except ImportError:
        print(json.dumps({'valid':False,'error':'dependency_missing'}));return 3

if __name__=='__main__':sys.exit(main())
