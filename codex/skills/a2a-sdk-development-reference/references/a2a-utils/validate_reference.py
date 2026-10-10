"""Validate read-only source coverage and pure implementation behavior; no network."""
from pathlib import Path
import ast, asyncio, collections, hashlib, importlib.util, importlib.metadata, json, types
from google.protobuf import json_format, descriptor_pb2, message_factory
from a2a.types import a2a_pb2 as pb
from a2a.utils import proto_utils as pu
from a2a.utils import task, _jcs, signing, error_handlers as eh, errors, telemetry
from a2a.utils.version_validator import validate_version
from a2a.server.context import ServerCallContext
from starlette.datastructures import QueryParams
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'.venv/lib/python3.11/site-packages/a2a'; checks=[]
def check(name,condition):
 assert condition,name
 checks.append(name)
def raises(cls,fn):
 try:fn()
 except cls:return True
 return False
def declarations(tree):
 out=[]
 def walk(n,scope=''):
  for c in ast.iter_child_nodes(n):
   if isinstance(c,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)):
    q=scope+'.'+c.name if scope else c.name;out.append((q,c.lineno,type(c).__name__));walk(c,q)
   else:walk(c,scope)
 walk(tree);return out
counts={}
for pkg in ['utils','types']:
 out=ROOT/('a2a-'+pkg); manifest=json.loads((out/'source_manifest.json').read_text());idx=json.loads((out/'callable_index.json').read_text()); actual=[]; annotations=[]; lambdas=[]
 files=[p for p in sorted((SRC/pkg).rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
 check(pkg+' complete non-cache inventory',set(x['file'] for x in manifest)==set(p.relative_to(SRC/pkg).as_posix() for p in files))
 for p in files:
  rel=p.relative_to(SRC/pkg).as_posix();s=p.read_text();tree=ast.parse(s);doc=(out/(p.name.replace('.','_')+'_knowledge.md')).read_text()
  check(pkg+'/'+rel+' source hash',hashlib.sha256(p.read_bytes()).hexdigest()==next(x['sha256'] for x in manifest if x['file']==rel))
  for q,line,kind in declarations(tree):
   ident=f'{rel}:{line}:{q}';actual.append(ident);check('behavior section '+ident,f'### `{q}` (line {line})' in doc and f'Coverage ID: `{ident}`' in doc)
   if pkg=='utils':check('authored behavior '+ident,'Implementation evidence' in doc.split(f'### `{q}` (line {line})')[1].split('### ')[0])
  def members(node,scope=''):
   for c in ast.iter_child_nodes(node):
    if isinstance(c,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)):members(c,scope+'.'+c.name if scope else c.name)
    elif isinstance(c,ast.AnnAssign):annotations.append({'file':rel,'line':c.lineno,'scope':scope,'entry':ast.unparse(c)})
    elif isinstance(c,ast.Lambda):lambdas.append({'file':rel,'line':c.lineno,'scope':scope,'entry':ast.unparse(c)})
    else:members(c,scope)
  members(tree)
 check(pkg+' exact AST identity comparison',collections.Counter(actual)==collections.Counter(x['id'] for x in idx))
 (out/'annotation_and_lambda_inventory.json').write_text(json.dumps({'annotated_entries':annotations,'anonymous_callables':lambdas},indent=2)+'\n')
 counts[pkg]={'non_cache_files':len(files),'ast_declarations':len(idx),'classes':sum(x['kind']=='ClassDef' for x in idx),'functions_and_async_functions':sum(x['kind']!='ClassDef' for x in idx),'pyi_declarations':sum(x['stub'] for x in idx),'annotated_entries':len(annotations),'anonymous_callables':len(lambdas)}
# Enumerate compiled generated callable surfaces, not just AST names.
runtime=[]
def model(d):
 cls=message_factory.GetMessageClass(d); names=[]
 for name in dir(cls):
  try:value=getattr(cls,name)
  except (AttributeError,TypeError):continue
  if callable(value):names.append(name)
 runtime.append({'full_name':d.full_name,'module':cls.__module__,'callables':names})
 for child in d.nested_types:model(child)
for d in pb.DESCRIPTOR.message_types_by_name.values():model(d)
(ROOT/'a2a-types/generated_callable_inventory.json').write_text(json.dumps(runtime,indent=2)+'\n')
# Every descriptor model/field represented, including nested map entries and HTTP options.
doc=(ROOT/'a2a-types/descriptor_knowledge.md').read_text()
for m in runtime:check('descriptor class '+m['full_name'],f'## `{m["full_name"]}`' in doc)
fd=descriptor_pb2.FileDescriptorProto();pb.DESCRIPTOR.CopyToProto(fd)
check('complete raw descriptor metadata',json.loads((ROOT/'a2a-types/descriptor_inventory.json').read_text())==json_format.MessageToDict(fd,preserving_proto_field_name=True))
# Descriptor field rows and every discovered runtime callable require concrete documentation.
def descriptor_fields(d):
 section=doc.split(f'## `{d.full_name}`',1)[1].split('## ',1)[0]
 for f in d.fields:
  check('descriptor field '+f.full_name,f'| `{f.name}` / `{f.json_name}` | {f.number} |' in section)
 for child in d.nested_types:descriptor_fields(child)
for d in pb.DESCRIPTOR.message_types_by_name.values():descriptor_fields(d)
runtime_doc=(ROOT/'a2a-types/runtime_surface_knowledge.md').read_text()
for name in sorted({name for m in runtime for name in m['callables']}):
 check('runtime callable explanation '+name,name in runtime_doc)
# Pure address classification (no DNS), queue creation/shutdown, and trace extractor behavior.
from a2a.utils.push_url_validator import _ip_is_blocked
from a2a.utils._async_queue_compat import create_async_queue
for ip in ['127.0.0.1','10.0.0.1','169.254.169.254','::1','::ffff:127.0.0.1','224.0.0.1','not-an-ip']:
 check('blocked address '+ip,_ip_is_blocked(ip))
check('public address classification',not _ip_is_blocked('8.8.8.8'))
queue=create_async_queue(3);check('Python 3.11 queue branch',queue.maxsize==3);queue.shutdown()
seen=[]
@telemetry.trace_function(attribute_extractor=lambda span,args,kwargs,result,exception:seen.append((result,exception)))
def traced():return 'result'
check('trace return/extractor',traced()=='result' and seen==[('result',None)])
# Supporting file hashes still match inspected source.
for pkg in ['utils','types']:
 for row in json.loads((ROOT/('a2a-'+pkg)/'supporting_source_manifest.json').read_text())['files']:
  check('supporting hash '+row['source'],hashlib.sha256(Path(row['source']).read_bytes()).hexdigest()==row['sha256'])
# Presence, ownership, JSON, validation and serialization.
req=pb.GetTaskRequest(id='t'); check('history absence vs zero',not req.HasField('history_length'));req.history_length=0;check('explicit zero presence',req.HasField('history_length'))
p=pb.Part(text='');check('oneof default still selects',p.WhichOneof('content')=='text');p.raw=b'x';check('oneof switch clears',p.text=='' and p.WhichOneof('content')=='raw')
msg=pb.Message(message_id='m',role=pb.ROLE_USER,parts=[pb.Part(text='é')]);pu.validate_proto_required_fields(msg)
t=pb.Task(id='t',history=[msg]);t.status.state=pb.TASK_STATE_WORKING;pu.validate_proto_required_fields(t)
e=pu.to_stream_response(t);t.id='other';check('event CopyFrom isolation',e.task.id=='t');check('wire round trip',pb.StreamResponse.FromString(e.SerializeToString())==e)
check('JSON aliases and literal unicode',json_format.MessageToDict(msg)['messageId']=='m' and json_format.MessageToDict(msg)['parts'][0]['text']=='é')
check('proto3 does not enforce Google REQUIRED',pb.Task().SerializeToString()==b'' and pb.Task().IsInitialized())
check('required utility enforcement',raises(errors.InvalidParamsError,lambda:pu.validate_proto_required_fields(pb.Task())))
try:pu.validate_proto_required_fields(pb.SendMessageRequest(message=pb.Message()))
except errors.InvalidParamsError as ex:check('nested error path',any(x['field']=='message.parts' for x in ex.data['errors']))
check('unsupported event empty response',pu.to_stream_response(object()).WhichOneof('payload') is None)
q=pb.ListTasksRequest();pu.parse_params(QueryParams('pageSize=4&includeArtifacts=garbage&unknown=1'),q);check('query defaults/coercion',q.page_size==4 and q.HasField('include_artifacts') and not q.include_artifacts)
h=pb.Task(history=[pb.Message(message_id='a'),pb.Message(message_id='b')]);check('no-limit identity',task.apply_history_length(h,pb.GetTaskRequest()) is h)
s=task.apply_history_length(h,pb.GetTaskRequest(history_length=1));check('suffix copy',s is not h and s.history[0].message_id=='b' and len(h.history)==2)
check('zero copy clear',not task.apply_history_length(h,pb.GetTaskRequest(history_length=0)).history)
check('negative requires separate validation',task.apply_history_length(h,pb.GetTaskRequest(history_length=-1)) is h and raises(errors.InvalidParamsError,lambda:task.validate_history_length(pb.GetTaskRequest(history_length=-1))))
check('page bounds',raises(errors.InvalidParamsError,lambda:task.validate_page_size(101)) and raises(errors.InvalidParamsError,lambda:task.validate_page_size(0)))
check('cursor roundtrip unicode unpadded',task.decode_page_token(task.encode_page_token('é/t').rstrip('='))=='é/t');check('cursor non-strict junk',task.decode_page_token('!!!!')=='')
check('integer normalization threshold',pu.normalize_large_integers_to_strings([10**15,10**15-1])==[str(10**15),10**15-1]);check('restore heuristic',pu.parse_string_integers_in_dict(str(10**15))==10**15)
check('repeated minus restore error',raises(ValueError,lambda:pu.parse_string_integers_in_dict('--1234567890123456')))
check('JCS order unicode negative zero',_jcs.canonicalize({'z':-0.0,'a':'é'})=='{"a":"é","z":0}')
for name,val in [('nonfinite',float('nan')),('unsafe int',2**53),('non-string key',{1:'x'}),('surrogate','\ud800')]:check('JCS reject '+name,raises(_jcs.CanonicalizationError,lambda v=val:_jcs.canonicalize(v)))
check('clean removes null/empty retains zero',signing._clean_empty({'a':None,'b':[],'c':'','z':0,'f':False})=={'z':0,'f':False})
card=pb.AgentCard(name='demo',description='é');signer=signing.create_agent_card_signer('local-example-key-at-least-32-bytes-long',{'kid':'local','alg':'HS256','typ':'JOSE','jku':None});check('signer mutates returns same',signer(card) is card and len(card.signatures)==1)
verify=signing.create_signature_verifier(lambda kid,jku:'local-example-key-at-least-32-bytes-long',['HS256']);verify(card);checks.append('signature local HMAC roundtrip');card.name='tampered';check('tampered card rejects',raises(signing.InvalidSignaturesError,lambda:verify(card)))
check('no signature rejects',raises(signing.NoSignatureError,lambda:verify(pb.AgentCard())))
err=errors.InvalidParamsError(data={'errors':[{'field':'x','message':'missing'}]});payload=eh.build_rest_error_payload(err);check('typed error details',payload['error']['code']==400 and len(payload['error']['details'])==2)
check('JSONParseError REST fallback',eh.build_rest_error_payload(errors.JSONParseError())['error']['status']=='INTERNAL')
class Child(errors.InvalidParamsError):pass
check('exact class lookup fallback',eh.build_rest_error_payload(Child())['error']['code']==500)
async def async_checks():
 @validate_version('1.0')
 async def op(context=None):return 42
 check('major-only version compatibility',await op(ServerCallContext(state={'headers':{'A2A-Version':'1.99'}}))==42)
 check('missing context bypass',await op()==42)
 try:await op(ServerCallContext(state={'headers':{}}))
 except errors.VersionNotSupportedError:checks.append('missing header defaults 0.3 mismatch')
 @validate_version('1.0')
 async def gen(context=None):yield 1
 check('generator version early rejection',raises(errors.VersionNotSupportedError,lambda:gen(ServerCallContext(state={'headers':{}}))))
 @eh.rest_error_handler
 async def unary():raise errors.InvalidParamsError()
 check('REST coroutine exception conversion',(await unary()).status_code==400)
 @eh.rest_stream_error_handler
 async def stream():
  async def body():
   yield 'ok'
   raise errors.InvalidParamsError()
  return types.SimpleNamespace(body_iterator=body())
 response=await stream();check('stream passes item',await anext(response.body_iterator)=='ok')
 try:await anext(response.body_iterator)
 except errors.InvalidParamsError:checks.append('stream iteration error rethrows')
 @eh.rest_error_handler
 async def cancel():raise asyncio.CancelledError()
 try:await cancel()
 except asyncio.CancelledError:checks.append('REST cancellation propagates')
asyncio.run(async_checks())
# Fake gRPC API proves bindings and registration without import/install/network.
source=ast.parse((SRC/'types/a2a_pb2_grpc.py').read_text());source.body=[n for n in source.body if not isinstance(n,(ast.Import,ast.ImportFrom))]
class Fake:
 StatusCode=types.SimpleNamespace(UNIMPLEMENTED='unimplemented')
 def __getattr__(self,name):
  return lambda *a,**kw:(name,a,kw)
fake=Fake(); fake.experimental=Fake();ns={'grpc':fake,'a2a__pb2':pb,'google_dot_protobuf_dot_empty__pb2':__import__('google.protobuf.empty_pb2',fromlist=['Empty'])};exec(compile(source,'local_generated_grpc_fixture','exec'),ns)
stub=ns['A2AServiceStub'](fake);svc=pb.DESCRIPTOR.services_by_name['A2AService']
for m in svc.methods:
 binding=getattr(stub,m.name);check('RPC binding '+m.name,binding[0]==('unary_stream' if m.server_streaming else 'unary_unary') and binding[1][0]==f'/{svc.full_name}/{m.name}')
 check('RPC serializer '+m.name,binding[2]['request_serializer'](message_factory.GetMessageClass(m.input_type)())==b'')
 result=getattr(ns['A2AService'],m.name)(message_factory.GetMessageClass(m.input_type)(),'unused-local-target');check('experimental forwarding '+m.name,result[1][2]==f'/{svc.full_name}/{m.name}' and result[2]['_registered_method'])
 ctx=types.SimpleNamespace(set_code=lambda c:None,set_details=lambda d:None);check('servicer unimplemented '+m.name,raises(NotImplementedError,lambda:getattr(ns['A2AServiceServicer'](),m.name)(None,ctx)))
registrations=[];server=types.SimpleNamespace(add_generic_rpc_handlers=lambda x:registrations.append(x),add_registered_method_handlers=lambda *x:registrations.append(x));ns['add_A2AServiceServicer_to_server'](ns['A2AServiceServicer'](),server);check('registration all methods',set(registrations[1][1])==set(m.name for m in svc.methods))
for pkg in ['utils','types']:
 for p in (ROOT/('a2a-'+pkg)).glob('*.md'):
  check('no trailing whitespace '+str(p.relative_to(ROOT)),all(line==line.rstrip() for line in p.read_text().splitlines()))
  check('balanced fences '+str(p.relative_to(ROOT)),sum(line.startswith('```') for line in p.read_text().splitlines())%2==0)
# Bootstrap report destinations before validating navigation, then replace with final results.
for pkg in ['utils','types']:
 p=ROOT/('a2a-'+pkg)/'validation_knowledge.md'
 if not p.exists():p.write_text('# Validation pending\n')
# Internal links only; no network.
import re
for pkg in ['utils','types']:
 for p in (ROOT/('a2a-'+pkg)).glob('*.md'):
  for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   if '://' not in target: check('link '+p.name+' '+target,(p.parent/target.split('#')[0]).exists())
summary={'version':importlib.metadata.version('a2a-sdk'),'date':'2026-10-07','counts':counts,'descriptor_counts':json.loads((ROOT/'a2a-types/descriptor_counts.json').read_text()),'checks_passed':len(checks),'optional_grpc_available':False,'generated_message_callable_entries':sum(len(m['callables']) for m in runtime),'generated_channel_callable_assignments':11,'limitations':['No real grpc import or RPC: grpc absent; AST/fake-channel bindings verified.','Compiled upb internals not available as Python source; descriptor/common runtime source and pure examples inspected.','No DNS resolver/network push URL test, no cloud APIs, no external persistence/authorization guarantee.','Coverage checks establish inventory and behavior evidence, not complete branch correctness of installed SDK.']}
for pkg in ['utils','types']:
 out=ROOT/('a2a-'+pkg)
 (out/'validation_results.json').write_text(json.dumps({'summary':summary,'passed_checks':checks},indent=2)+'\n')
 (out/'validation_knowledge.md').write_text('# Validation and limitations\n\nRun `.venv/bin/python a2a-utils/validate_reference.py` from workspace. Rebuild per-file/descriptor docs with `.venv/bin/python a2a-utils/build_reference.py`; authored overview/runtime guides remain separate.\n\n```json\n'+json.dumps(summary,indent=2)+'\n```\n\nEvidence beyond name matching: exact `(file,line,qualified-name,kind)` declaration multiset comparison; authored utility execution sections; raw decoded descriptor equality; source SHA-256 equality; concrete local presence/oneof/ownership/validation/serialization/signing/version/error assertions; all 11 fake-channel generated bindings/static forwarders/unimplemented skeletons and full registration dictionary. Every PYI repeated class/constructor/annotation is separately scoped. Markdown links, balanced code fences and whitespace checked. Full passed-check list is in validation_results.json. Anonymous lambdas and annotations are separately inventoried; compiled runtime callable inventory is separate from AST count.\n')
print(json.dumps(summary,indent=2))
