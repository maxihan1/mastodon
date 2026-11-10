# 하위 폴더까지 읽어 다시 만든 Mastodon OpenAPI 에서, 관리자 문서가 덮어쓴 공통 이름을 원래대로 되돌린다
import json,sys
orig=json.load(open('schema.orig.json')); new=json.load(open('mo/dist/schema.json'))
oc,nc=orig['components'],new['components']
nc['schemas']['AdminDomainBlockConflict422']=nc['schemas']['CustomError422']
nc['examples']['AdminDomainBlockConflict422Example']=nc['examples']['CustomError422422Example']
nc['examples']['AdminTrendsLink200Example']=nc['examples']['TrendsLink200Example']
nc['schemas']['CustomError422']=oc['schemas']['CustomError422']
nc['examples']['CustomError422422Example']=oc['examples']['CustomError422422Example']
nc['examples']['TrendsLink200Example']=oc['examples']['TrendsLink200Example']
def swap(op,a,b): return json.loads(json.dumps(op).replace(a,b))
p=new['paths']
p['/api/v1/admin/domain_blocks']['post']=swap(swap(p['/api/v1/admin/domain_blocks']['post'],'#/components/examples/CustomError422422Example','#/components/examples/AdminDomainBlockConflict422Example'),'#/components/schemas/CustomError422"','#/components/schemas/AdminDomainBlockConflict422"')
p['/api/v1/admin/trends/links']['get']=swap(p['/api/v1/admin/trends/links']['get'],'#/components/examples/TrendsLink200Example','#/components/examples/AdminTrendsLink200Example')
new['info']['description']=(new['info'].get('description','')+"\n\n이 판은 abraham/mastodon-openapi d2287ca 를 바탕으로 하위 폴더(methods/admin)까지 읽어 관리자 API 47개를 더했다. 기존 동작 210개는 원본과 같다.").strip()
json.dump(new,open('mastodon-openapi.json','w'),ensure_ascii=False,indent=2)
# 검증 — 관리자 것을 빼면 원본과 같아야 한다
M=('get','post','put','patch','delete')
def ops(d): return {(a,m):v for a,pv in d['paths'].items() for m,v in pv.items() if m in M}
oo,no=ops(orig),ops(new)
bad=[k for k in oo if json.dumps(oo[k],sort_keys=True)!=json.dumps(no.get(k),sort_keys=True)]
cbad=[(s,k) for s in oc for k in oc[s] if json.dumps(oc[s][k],sort_keys=True)!=json.dumps(nc.get(s,{}).get(k),sort_keys=True)]
refs=set(__import__('re').findall(r'#/components/(\w+)/(\w+)',json.dumps(new)))
missing=[r for r in refs if r[1] not in nc.get(r[0],{})]
print('기존 동작 바뀜',bad,'| 기존 components 바뀜',cbad,'| 없는 $ref',missing,'| 동작',len(no),'| 관리자',len([k for k in no if '/admin/' in k[0]]))
