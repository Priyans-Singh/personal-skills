"""Read-only local coverage verification and representative behavior fixtures.

No network: every transport fixture uses httpx.MockTransport. No SQL/gRPC imports.
"""
from pathlib import Path
import ast
import asyncio
import collections
import hashlib
import importlib.metadata
import importlib.util
import json
import re

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent/'.venv/lib/python3.11/site-packages/a2a/compat'
checks=[]
def check(name, condition, detail=None):
    checks.append({'check':name,'passed':bool(condition),'detail':detail})
    if not condition:raise AssertionError(f'{name}: {detail}')

def enumerate_ast(tree):
    result=[]
    def walk(node,parents=()):
        for n in ast.iter_child_nodes(node):
            if isinstance(n,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)):
                path=parents+(n.name,)
                result.append(('.'.join(path),type(n).__name__,n.lineno,n))
                walk(n,path)
            else:walk(n,parents)
    walk(tree)
    return result

def coverage():
    manifest=json.loads((OUT/'source_manifest.json').read_text())
    index=json.loads((OUT/'callable_index.json').read_text())
    check('distribution version',importlib.metadata.version('a2a-sdk')=='1.1.4')
    files={str(p.relative_to(ROOT)):p for p in ROOT.rglob('*') if p.is_file()}
    recorded={x['path']:x for x in manifest['files']}
    check('complete file inventory including caches',files.keys()==recorded.keys())
    for rel,p in files.items():
        check('source hash '+rel,hashlib.sha256(p.read_bytes()).hexdigest()==recorded[rel]['sha256'])
        if recorded[rel]['guide']:check('guide exists '+rel,(OUT/recorded[rel]['guide']).is_file())
    actual=[]
    model_fields=0
    for rel,p in files.items():
        if p.suffix not in ('.py','.pyi'):continue
        guide=(OUT/recorded[rel]['guide']).read_text()
        tree=ast.parse(p.read_text())
        for name,kind,line,node in enumerate_ast(tree):
            actual.append((rel,name,kind,line))
            heading=f'### {"PYI " if p.suffix==".pyi" else ""}`{name}`'
            check('exact declaration heading '+rel+':'+name,heading in guide)
            section=guide.split(heading+'\n',1)[1].split('\n### ',1)[0]
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) and p.suffix=='.py':
                check('behavior/signature/body '+rel+':'+name,all(s in section for s in ['Inputs:','Output annotation:','Ordered implementation behavior','Explicit errors:','Exact executable implementation']))
            elif isinstance(node,ast.ClassDef) and p.suffix=='.py':
                check('class behavior '+rel+':'+name,'Bases:' in section and ('Execution:' in section or 'Declared operations:' in section))
                for n in node.body:
                    if isinstance(n,ast.AnnAssign):
                        field=ast.unparse(n.target)
                        check('field '+name+'.'+field,field in section)
                        if rel.endswith('/types.py'):model_fields+=1
    expected=[(r['source'],r['name'],r['kind'],r['line']) for r in index]
    check('AST declaration index exact equality',sorted(actual)==sorted(expected))
    check('human callable index complete',all(f'`{r["name"]}`' in (OUT/'callable_index.md').read_text() for r in index))
    from a2a.compat.v0_3 import a2a_v0_3_pb2 as pb
    proto_guide=(OUT/'v0_3_a2a_v0_3_pb2_knowledge.md').read_text()
    descriptor_count=0;descriptor_fields=0
    def walk(d):
        nonlocal descriptor_count,descriptor_fields
        descriptor_count+=1
        check('descriptor heading '+d.full_name,f'### Descriptor `{d.full_name}`' in proto_guide)
        block=proto_guide.split(f'### Descriptor `{d.full_name}`',1)[1].split('\n### ',1)[0]
        for f in d.fields:
            descriptor_fields+=1
            check('descriptor field '+d.full_name+'.'+f.name,f'| {f.name} | {f.number} |' in block)
        for nested in d.nested_types:walk(nested)
    for d in pb.DESCRIPTOR.message_types_by_name.values():walk(d)
    for d in pb.DESCRIPTOR.enum_types_by_name.values():
        check('enum heading '+d.full_name,f'### Enum `{d.full_name}`' in proto_guide)
        for v in d.values:check('enum value '+v.name,f'`{v.name}={v.number}`' in proto_guide)
    rpcs=[]
    for service in pb.DESCRIPTOR.services_by_name.values():
        for method in service.methods:
            rpcs.append(method.name)
            check('generated dynamic stub method '+method.name,f'| {method.name} |' in proto_guide)
    # Prove shipped schema declarations are accounted separately from synthetic map entries.
    proto=(ROOT/'v0_3/a2a_v0_3.proto').read_text()
    schema_messages=re.findall(r'^message\s+(\w+)\s*\{',proto,re.M)
    check('source schema message names match runtime top-level',set(schema_messages)==set(pb.DESCRIPTOR.message_types_by_name))
    check('source schema RPCs match runtime',set(re.findall(r'\brpc\s+(\w+)\(',proto))==set(rpcs))
    text_assets=(OUT/'v0_3_protocol_assets_knowledge.md').read_text()
    for rel,p in files.items():
        if p.suffix not in ('.py','.pyi','.pyc'):
            normalized='\n'.join(line.rstrip() for line in p.read_text().splitlines()).rstrip()
            check('complete textual support file '+rel,normalized in text_assets)
    # Markdown link and whitespace validation, excluding fenced source examples.
    md_files=list(OUT.glob('*.md'))
    for p in md_files:
        lines=p.read_text().splitlines(); fence=None;prose=[]
        for i,line in enumerate(lines,1):
            check('no trailing whitespace '+p.name+':'+str(i),line==line.rstrip())
            m=re.match(r'^(`{3,})(.*)$',line)
            if m:
                marker=m.group(1)
                if fence is None:fence=len(marker)
                elif len(marker)>=fence and not m.group(2).strip():fence=None
                continue
            if fence is None:prose.append(line)
        check('balanced code fences '+p.name,fence is None)
        for target in re.findall(r'\]\(([^)]+)\)','\n'.join(prose)):
            if '://' in target or target.startswith('#'):continue
            target=target.split('#',1)[0]
            check('local link '+p.name+' → '+target,(p.parent/target).exists())
    counts=collections.Counter(r['kind'] for r in index)
    return {'source_support_files':sum(x['kind']=='source/support' for x in recorded.values()),'cache_files':sum(x['kind']=='runtime cache' for x in recorded.values()),'ast_declarations':len(index),'ast_by_kind':dict(counts),'pydantic_declared_fields':model_fields,'protobuf_messages_including_map_entries':descriptor_count,'protobuf_fields':descriptor_fields,'protobuf_enums':len(pb.DESCRIPTOR.enum_types_by_name),'service_rpcs':len(rpcs),'knowledge_files':len(list(OUT.glob('*_knowledge.md'))),'markdown_files':len(md_files)}

def pure_fixtures():
    from a2a.compat.v0_3 import conversions as c, types as t, proto_utils as u, a2a_v0_3_pb2 as old
    from a2a.types import a2a_pb2 as core
    from a2a.compat.v0_3.versions import is_legacy_version
    from a2a.compat.v0_3.extension_headers import add_legacy_extension_header
    from a2a.utils.errors import VersionNotSupportedError
    text=t.Message(message_id='m1',role=t.Role.user,parts=[t.Part(root=t.TextPart(text='hello'))])
    converted=c.to_core_message(text)
    check('message identity/text direct round trip',c.to_compat_message(converted).message_id=='m1' and converted.parts[0].text=='hello')
    p=t.Part(root=t.FilePart(file=t.FileWithBytes(bytes='aGk=')))
    check('core file content decoded',c.to_core_part(p).raw==b'hi')
    wire=u.ToProto.part(p)
    check('legacy protobuf contains base64 text',wire.file.file_with_bytes==b'aGk=')
    check('legacy protobuf file reverse',u.FromProto.part(wire).root.file.bytes=='aGk=')
    scalar=core.Part();scalar.data.number_value=42
    pivot=c.to_compat_part(scalar)
    check('scalar data wrapper marker',pivot.root.data=={'value':42.0} and pivot.root.metadata['data_part_compat'] is True)
    check('scalar data wrapper round trip',c.to_core_part(pivot).data.number_value==42)
    status=t.TaskStatus(state=t.TaskState.working,timestamp='2026-10-07T00:00:00Z')
    check('direct status timestamp retained',c.to_core_task_status(status).HasField('timestamp'))
    check('legacy protobuf status timestamp dropped',not u.ToProto.task_status(status).HasField('timestamp'))
    absent=u.FromProto.task_status(old.TaskStatus())
    check('absent status update becomes placeholder',absent.message is not None and absent.message.message_id=='' and absent.message.role==t.Role.agent)
    params=u.FromProto.message_send_params(old.SendMessageRequest(request=u.ToProto.message(text)))
    check('absent protobuf config becomes false blocking',params.configuration.blocking is False)
    req=t.SendMessageRequest(id=0,params=params)
    check('legacy absent-config core immediate',c.to_core_send_message_request(req).configuration.return_immediately is True)
    direct=t.SendMessageRequest(id=0,params=t.MessageSendParams(message=text))
    check('direct pivot absent-config stays absent',not c.to_core_send_message_request(direct).HasField('configuration'))
    check('get protobuf zero history loses presence',u.FromProto.task_query_params(old.GetTaskRequest(name='tasks/t',history_length=0)).history_length is None)
    check('regex accepts suffix',u.FromProto.task_query_params(old.GetTaskRequest(name='tasks/t/extra')).id=='t')
    auth=t.PushNotificationAuthenticationInfo(schemes=['first','second'],credentials='test-placeholder')
    check('authentication schemes narrowed',c.to_core_authentication_info(auth).scheme=='first')
    flows=t.OAuthFlows(authorization_code=t.AuthorizationCodeOAuthFlow(authorization_url='https://example.invalid/auth',token_url='https://example.invalid/token',scopes={}),password=t.PasswordOAuthFlow(token_url='https://example.invalid/token',scopes={}))
    check('core OAuth last present wins',c.to_core_oauth_flows(flows).WhichOneof('flow')=='password')
    check('legacy proto OAuth first present wins',u.ToProto.oauth2_flows(flows).WhichOneof('flow')=='authorization_code')
    card=t.AgentCard(name='n',description='d',url='https://example.invalid',version='app',capabilities=t.AgentCapabilities(),default_input_modes=[],default_output_modes=[],skills=[],icon_url='https://example.invalid/icon')
    check('direct card icon retained',c.to_core_agent_card(card).icon_url==card.icon_url)
    check('legacy proto icon omitted',u.ToProto.agent_card(card).icon_url=='')
    current=core.AgentCard(supported_interfaces=[core.AgentInterface(url='https://example.invalid',protocol_version='1.0',protocol_binding='JSONRPC')])
    try:c.to_compat_agent_card(current)
    except VersionNotSupportedError:check('current-only card rejected',True)
    else:check('current-only card rejected',False)
    check('version interval accepts 0.4',is_legacy_version('0.4'))
    check('version invalid rejected',not is_legacy_version('not a version'))
    headers={'A2A-Extensions':'urn:one'};add_legacy_extension_header(headers)
    check('canonical extensions mirrored',headers['X-A2A-Extensions']=='urn:one')
    headers={'a2a-extensions':'urn:one'};add_legacy_extension_header(headers)
    check('lowercase extension keys not mirrored','X-A2A-Extensions' not in headers)
    wire_resp=old.SendMessageResponse(msg=old.Message(message_id='m'))
    check('pure protobuf serialization',old.SendMessageResponse.FromString(wire_resp.SerializeToString()).WhichOneof('payload')=='msg')
    err=t.SendMessageResponse(root=t.JSONRPCErrorResponse(id=0,error=t.InternalError()))
    check('send error root produces empty core response',c.to_core_send_message_response(err).WhichOneof('payload') is None)

async def mock_fixtures():
    import httpx
    # Installed route initializer cycles back into compat; routes-first avoids it.
    import a2a.server.routes
    from a2a.client.client import ClientCallContext
    from a2a.client.transports.http_helpers import parse_sse_stream
    from a2a.compat.v0_3.jsonrpc_transport import CompatJsonRpcTransport
    from a2a.compat.v0_3.rest_transport import CompatRestTransport
    from a2a.compat.v0_3.jsonrpc_adapter import JSONRPC03Adapter
    from a2a.compat.v0_3.rest_adapter import REST03Adapter
    from a2a.compat.v0_3 import types as t, conversions as c
    from a2a.types import a2a_pb2 as core
    from a2a.server.context import ServerCallContext
    from a2a.utils.version_validator import validate_version
    from a2a.utils.errors import TaskNotFoundError
    from starlette.requests import Request
    @validate_version('0.3')
    async def probe(context):return 'accepted'
    check('validator actual major-only accepts 0.2',await probe(ServerCallContext(state={'headers':{'a2a-version':'0.2'}}))=='accepted')
    captured=[]
    async def jsonrpc_peer(request):
        captured.append(request)
        body=json.loads(request.content)
        return httpx.Response(200,json={'jsonrpc':'2.0','id':body['id'],'result':{'messageId':'r','role':'agent','parts':[]}})
    client=httpx.AsyncClient(transport=httpx.MockTransport(jsonrpc_peer))
    transport=CompatJsonRpcTransport(client,None,'https://example.invalid/a2a')
    req=core.SendMessageRequest(message=core.Message(message_id='m',role=core.Role.ROLE_USER))
    ctx=ClientCallContext(service_parameters={'A2A-Extensions':'urn:local'},timeout=1)
    response=await transport.send_message(req,context=ctx)
    check('JSON-RPC missing kind fallback',response.message.message_id=='r')
    check('JSON-RPC version and extension wire headers',captured[0].headers['a2a-version']=='0.3' and captured[0].headers['x-a2a-extensions']=='urn:local')
    check('original service parameter mapping unchanged','X-A2A-Extensions' not in ctx.service_parameters)
    check('JSON-RPC UUID distinct from conversion id',json.loads(captured[0].content)['id']!=0)
    await transport.close()
    check('transport closes injected client',client.is_closed)
    methods=[]
    async def rest_peer(request):
        methods.append(request.method)
        if request.method=='POST':return httpx.Response(405,json={})
        return httpx.Response(200,headers={'content-type':'text/event-stream'},content='data: {"message":{"messageId":"s","role":"ROLE_AGENT"}}\n\n')
    rest_client=httpx.AsyncClient(transport=httpx.MockTransport(rest_peer))
    rest=CompatRestTransport(rest_client,None,'https://example.invalid/')
    events=[e async for e in rest.subscribe(core.SubscribeToTaskRequest(id='t'))]
    check('REST subscription local POST-to-GET fallback',methods==['POST','GET'] and events[0].message.message_id=='s')
    methods.clear();_= [e async for e in rest.subscribe(core.SubscribeToTaskRequest(id='t'))]
    check('REST GET preference remembered',methods==['GET'])
    await rest.close()
    # Shared parser intentionally requires blank event terminator.
    response=httpx.Response(200,content='data: first\n\ndata: unflushed\n')
    parsed=[x async for x in parse_sse_stream(response)]
    check('SSE unflushed EOF event dropped',parsed==[('message','first')])
    # Handler need not be a concrete subclass for this local error fixture.
    class FakeCore:
        async def on_get_task(self,request,context):raise TaskNotFoundError()
    adapter=JSONRPC03Adapter(FakeCore())
    request=Request({'type':'http','method':'POST','path':'/','headers':[]})
    result=await adapter.handle_request('rpc','tasks/get',{'id':'rpc','method':'tasks/get','params':{'id':'t'}},request)
    check('JSON-RPC server downstream domain error becomes internal',json.loads(result.body)['error']['code']==-32603)
    route_map=REST03Adapter(FakeCore()).routes()
    check('REST route list exists but delete absent',('/v1/tasks/{id}/pushNotificationConfigs','GET') in route_map and not any(method=='DELETE' for path,method in route_map))

def optional_status():
    result={}
    for name in ['grpc','sqlalchemy','httpx','starlette','sse_starlette','cryptography','jsonrpc','packaging','pydantic','google.api.annotations_pb2']:
        try:result[name]=importlib.util.find_spec(name) is not None
        except ModuleNotFoundError:result[name]=False
    return result

if __name__=='__main__':
    (OUT/'validation_report.json').write_text(json.dumps({'passed':False,'status':'validation running'},indent=2)+'\n')
    counts=coverage()
    before=len(checks)
    pure_fixtures();asyncio.run(mock_fixtures())
    report={'version':'1.1.4','date':'2026-10-07','counts':counts,'passed':True,'checks_passed':len(checks),'behavior_fixtures_passed':len(checks)-before,'optional_dependencies':optional_status(),'network':'none; httpx.MockTransport only','limitations':['grpcio and SQLAlchemy absent: gRPC/ORM modules statically reviewed only','No external peer/service/DB execution; runtime transport/server policy remains external','Mechanical narrative presence and name/field checks do not prove semantic correctness; source-body review and representative fixtures supplement them'],'command':'.venv/bin/python -B a2a-compat/validate_reference.py'}
    (OUT/'validation_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
