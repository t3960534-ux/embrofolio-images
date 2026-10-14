#!/usr/bin/env python3
"""Generate Pinterest image-Pin CSVs matching the working Cabin Recipes format.
Standard library only. Creates final imports only if --verify succeeds (unless --skip-verify).
"""
import argparse,csv,pathlib,urllib.request,urllib.error,concurrent.futures,sys,collections,time

BASE=pathlib.Path(__file__).resolve().parent.parent
META=BASE/'metadata'/'PINTEREST_METADATA_64.csv'
OUTPUT=BASE/'PINTEREST_READY'
FIELDS=['Title','Media URL','Pinterest board','Thumbnail','Description','Link','Publish date','Keywords']

def validate_url(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; Embrofolio media-check/1.0)','Accept':'image/jpeg'},method='HEAD')
    try:
        with urllib.request.urlopen(req,timeout=25) as response:
            ctype=response.headers.get('Content-Type','').lower()
            if response.status==200 and ('image/jpeg' in ctype or 'image/jpg' in ctype):return (url,True,'')
            return (url,False,f'HTTP {response.status}, Content-Type={ctype}')
    except Exception as ex:
        return (url,False,str(ex))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--owner',default='t3960534-ux')
    parser.add_argument('--repo',default='embrofolio-images')
    parser.add_argument('--ref',default='main',help='Git commit SHA recommended; main also works')
    parser.add_argument('--verify',action='store_true')
    parser.add_argument('--skip-verify',action='store_true')
    args=parser.parse_args()
    rows=list(csv.DictReader(META.open(encoding='utf-8-sig',newline='')))
    if not args.verify and not args.skip_verify:
        parser.error('Use --verify to check media URLs before generating import files.')
    for row in rows:
        if len(row['title'])>100 or len(row['description'])>500:
            raise SystemExit(f"Pinterest text exceeds allowed length: {row['pin_id']}")
    assert len(rows)==64, f'Expected 64, found {len(rows)}'
    urls=[f'https://raw.githubusercontent.com/{args.owner}/{args.repo}/{args.ref}/pins/{r["filename"]}' for r in rows]
    if args.verify and not args.skip_verify:
        print('Checking 64 public JPG URLs on GitHub. This can take a minute...',flush=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            checks=list(pool.map(validate_url,urls))
        errors=[(u,e) for u,ok,e in checks if not ok]
        if errors:
            print(f'FAILED: {len(errors)} images not publicly reachable as JPEG. No import CSV was generated.')
            for u,e in errors[:7]:print(' -',u, '\n   ',e)
            print('Make sure the repo is PUBLIC, the commit pushed, and wait for GitHub propagation before retrying.')
            sys.exit(2)
        print('PASS: all 64 URLs are reachable JPG images.')
    elif not args.skip_verify:
        print('Note: URLs were constructed but not checked. Add --verify before importing to Pinterest.')
    result=[]
    for r,url in zip(rows,urls):
        result.append({'Title':r['title'],'Media URL':url,'Pinterest board':r['board'],'Thumbnail':'',
            'Description':r['description'],'Link':r['link'],'Publish date':r['publish_date'],'Keywords':r['keywords']})
    if len({r['Link'] for r in result})!=64:raise SystemExit('Duplicate outbound tracking URLs detected.')
    if len({r['Media URL'] for r in result})!=64:raise SystemExit('Duplicate media URLs detected.')
    OUTPUT.mkdir(exist_ok=True)
    blocks=[('PART_1_26.csv',result[:26]),('PART_2_26.csv',result[26:52]),('PART_3_12.csv',result[52:])]
    blocks.append(('ALL_64.csv',result))
    blocks.append(('TEST_ONE_PIN.csv',result[:1]))
    blocks.append(('REMAINING_63_AFTER_TEST.csv',result[1:]))
    for name,block in blocks:
        path=OUTPUT/name
        with path.open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(block)
        print(f'Created {path.relative_to(BASE)}: {len(block)} rows')
    print('These are image Pins, not videos. The files contain no video paths.')
    print('Do not import TEST_ONE_PIN plus ALL_64: that would duplicate the first Pin.')
    print('Confirm your Pinterest boards exist and scheduled dates are still in the future.')

if __name__=='__main__':main()
