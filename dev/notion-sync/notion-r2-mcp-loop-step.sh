#!/bin/bash
# One step: next -> write /tmp/r2-next-mcp-op.json, print summary
cd "$(dirname "$0")"
python3 notion-r2-mcp-executor.py next >/dev/null 2>&1
python3 -c "
import json
d=json.load(open('/tmp/r2-next-mcp-op.json'))
if d.get('done'):
    print('DONE', json.dumps(d.get('counts',{}), ensure_ascii=False))
elif d.get('error'):
    print('ERROR', d['error'], json.dumps(d.get('meta',{}), ensure_ascii=False))
else:
    op=d['op']
    meta=d.get('meta',{})
    args=op['args']
    if op['tool']=='notion-update-page':
        json.dump(args, open('/tmp/r2-mcp-args.json','w'), ensure_ascii=False)
        sz=len(args.get('new_str', args.get('content','')))
        print('UPDATE', meta.get('batch'), meta.get('op_idx'), meta.get('total_ops'), args['page_id'], args['command'], sz)
    else:
        json.dump(args, open('/tmp/r2-create-args.json','w'), ensure_ascii=False)
        print('CREATE', meta.get('batch'), len(args.get('pages',[])))
"
