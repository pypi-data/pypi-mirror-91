# Copyright (c) 2021 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_A9='"ietf-sztp-bootstrap-server:input" is missing.'
_A8='ssl_object'
_A7='access-denied'
_A6='/ietf-sztp-bootstrap-server:report-progress'
_A5='Resource does not exist.'
_A4='Requested resource does not exist.'
_A3=':log-entry'
_A2='/devices/device='
_A1=':devices/device='
_A0='2021-01-14'
_z='2019-04-30'
_y='urn:ietf:params:xml:ns:yang:ietf-yang-types'
_x='ietf-yang-types'
_w='TBD'
_v='module'
_u='module-set-id'
_t='ietf-yang-library:modules-state'
_s='application/yang-data+xml'
_r='webhooks'
_q='/ietf-sztp-bootstrap-server:get-bootstrapping-data'
_p='Parent node does not exist.'
_o='Resource can not be modified.'
_n='2013-07-15'
_m='webhook'
_l='Unable to parse "input" document: '
_k='import'
_j='application/yang-data+json'
_i='callback'
_h='passed-input'
_g='malformed-message'
_f=':device'
_e='Content-Type'
_d='1'
_c=False
_b=':tenants/tenant='
_a='x'
_Z='implement'
_Y='reference'
_X=True
_W='invalid-value'
_V='unknown-element'
_U='application'
_T='0'
_S='path'
_R='method'
_Q='source-ip'
_P='timestamp'
_O='conformance-type'
_N='namespace'
_M='revision'
_L=':dynamic-callout'
_K='ietf-sztp-bootstrap-server:input'
_J='protocol'
_I='text/plain'
_H='name'
_G='dynamic-callout'
_F='+'
_E='return-code'
_D='error-returned'
_C=None
_B='event-details'
_A='/'
import os,json,base64,pprint,asyncio,aiohttp,yangson,datetime,basicauth,urllib.parse,pkg_resources
from .  import yl
from .  import dal
from .  import utils
from aiohttp import web
from .native import Read
from pyasn1.type import univ
from .dal import DataAccessLayer
from .rcsvr import RestconfServer
from .handler import RouteHandler
from pyasn1_modules import rfc5652
from passlib.hash import sha256_crypt
from pyasn1.codec.der.encoder import encode as encode_der
from pyasn1.codec.der.decoder import decode as der_decoder
from certvalidator import CertificateValidator,ValidationContext,PathBuildingError
from cryptography.hazmat.backends import default_backend
from cryptography import x509
class RFC8572ViewHandler(RouteHandler):
	len_prefix_running=len(RestconfServer.root+'/ds/ietf-datastores:running');len_prefix_operational=len(RestconfServer.root+'/ds/ietf-datastores:operational');len_prefix_operations=len(RestconfServer.root+'/operations');id_ct_sztpConveyedInfoXML=rfc5652._buildOid(1,2,840,113549,1,9,16,1,42);id_ct_sztpConveyedInfoJSON=rfc5652._buildOid(1,2,840,113549,1,9,16,1,43);supported_media_types=_j,_s;yl4errors={_t:{_u:_w,_v:[{_H:_x,_M:_n,_N:_y,_O:_k},{_H:'ietf-restconf',_M:'2017-01-26',_N:'urn:ietf:params:xml:ns:yang:ietf-restconf',_O:_Z},{_H:'ietf-netconf-acm',_M:'2018-02-14',_N:'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',_O:_k},{_H:'ietf-sztp-bootstrap-server',_M:_z,_N:'urn:ietf:params:xml:ns:yang:ietf-sztp-bootstrap-server',_O:_Z},{_H:'ietf-yang-structure-ext',_M:'2020-06-22',_N:'urn:ietf:params:xml:ns:yang:ietf-yang-structure-ext',_O:_Z},{_H:'ietf-sztp-csr',_M:_A0,_N:'urn:ietf:params:xml:ns:yang:ietf-sztp-csr',_O:_Z},{_H:'ietf-crypto-types',_M:_A0,_N:'urn:ietf:params:xml:ns:yang:ietf-crypto-types',_O:_Z}]}};yl4conveyedinfo={_t:{_u:_w,_v:[{_H:_x,_M:_n,_N:_y,_O:_k},{_H:'ietf-inet-types',_M:_n,_N:'urn:ietf:params:xml:ns:yang:ietf-inet-types',_O:_k},{_H:'ietf-sztp-conveyed-info',_M:_z,_N:'urn:ietf:params:xml:ns:yang:ietf-sztp-conveyed-info',_O:_Z}]}}
	def __init__(A,dal,mode,yl,nvh):D='sztpd';A.dal=dal;A.mode=mode;A.nvh=nvh;B=pkg_resources.resource_filename(D,'yang');A.dm=yangson.DataModel(json.dumps(yl),[B]);A.dm4conveyedinfo=yangson.DataModel(json.dumps(A.yl4conveyedinfo),[B]);C=pkg_resources.resource_filename(D,'yang4errors');A.dm4errors=yangson.DataModel(json.dumps(A.yl4errors),[C,B])
	async def _insert_bootstrapping_log_entry(A,device_id,bootstrapping_log_entry):
		E='/bootstrapping-log';B=device_id
		if A.mode==_T:C=_A+A.dal.app_ns+':device/bootstrapping-log'
		elif A.mode==_d:C=_A+A.dal.app_ns+_A1+B[0]+E
		elif A.mode==_a:C=_A+A.dal.app_ns+_b+B[1]+_A2+B[0]+E
		D={};D[A.dal.app_ns+_A3]=bootstrapping_log_entry;await A.dal.handle_post_opstate_request(C,D)
	async def _insert_audit_log_entry(A,tenant_name,audit_log_entry):
		B=tenant_name
		if A.mode==_T or A.mode==_d or B==_C:C=_A+A.dal.app_ns+':audit-log'
		elif A.mode==_a:C=_A+A.dal.app_ns+_b+B+'/audit-log'
		D={};D[A.dal.app_ns+_A3]=audit_log_entry;await A.dal.handle_post_opstate_request(C,D)
	async def handle_get_restconf_root(D,request):
		C=request;J=_A;F=await D._check_auth(C,J)
		if type(F)is web.Response:A=F;return A
		else:H=F
		B={};B[_P]=datetime.datetime.utcnow();B[_Q]=C.remote;B[_R]=C.method;B[_S]=C.path;E,K=utils.check_http_headers(C,D.supported_media_types,accept_required=_X)
		if type(E)is web.Response:A=E;L=K;B[_E]=A.status;B[_D]=L;await D._insert_bootstrapping_log_entry(H,B);return A
		else:assert type(E)==str;G=E;assert G!=_I;I=utils.Encoding[G.rsplit(_F,1)[1]]
		A=web.Response(status=200);A.content_type=G
		if I==utils.Encoding.json:A.text='{\n    "ietf-restconf:restconf" : {\n        "data" : {},\n        "operations" : {},\n        "yang-library-version" : "2019-01-04"\n    }\n}\n'
		else:assert I==utils.Encoding.xml;A.text='<restconf xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">\n    <data/>\n    <operations/>\n    <yang-library-version>2016-06-21</yang-library-version>\n</restconf>\n'
		B[_E]=A.status;await D._insert_bootstrapping_log_entry(H,B);return A
	async def handle_get_yang_library_version(D,request):
		C=request;J=_A;F=await D._check_auth(C,J)
		if type(F)is web.Response:A=F;return A
		else:H=F
		B={};B[_P]=datetime.datetime.utcnow();B[_Q]=C.remote;B[_R]=C.method;B[_S]=C.path;E,K=utils.check_http_headers(C,D.supported_media_types,accept_required=_X)
		if type(E)is web.Response:A=E;L=K;B[_E]=A.status;B[_D]=L;await D._insert_bootstrapping_log_entry(H,B);return A
		else:assert type(E)==str;G=E;assert G!=_I;I=utils.Encoding[G.rsplit(_F,1)[1]]
		A=web.Response(status=200);A.content_type=G
		if I==utils.Encoding.json:A.text='{\n  "ietf-restconf:yang-library-version" : "2019-01-04"\n}'
		else:assert I==utils.Encoding.xml;A.text='<yang-library-version xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">2019-01-04</yang-library-version>'
		B[_E]=A.status;await D._insert_bootstrapping_log_entry(H,B);return A
	async def handle_get_opstate_request(C,request):
		D=request;E=D.path[C.len_prefix_operational:];E=_A;G=await C._check_auth(D,E)
		if type(G)is web.Response:A=G;return A
		else:I=G
		B={};B[_P]=datetime.datetime.utcnow();B[_Q]=D.remote;B[_R]=D.method;B[_S]=D.path;F,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_X)
		if type(F)is web.Response:A=F;M=L;B[_E]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(I,B);return A
		else:assert type(F)==str;H=F;assert H!=_I;J=utils.Encoding[H.rsplit(_F,1)[1]]
		if E=='/ietf-yang-library:yang-library'or E==_A or E=='':A=web.Response(status=200);A.content_type=_j;A.text=getattr(yl,'sbi_rfc8572')()
		else:A=web.Response(status=404);A.content_type=H;J=utils.Encoding[A.content_type.rsplit(_F,1)[1]];K=utils.gen_rc_errors(_J,_V,error_message=_A4);N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(K,J,C.dm4errors,N);B[_D]=K
		B[_E]=A.status;await C._insert_bootstrapping_log_entry(I,B);return A
	async def handle_get_config_request(C,request):
		D=request;F=D.path[C.len_prefix_running:];G=await C._check_auth(D,F)
		if type(G)is web.Response:A=G;return A
		else:I=G
		B={};B[_P]=datetime.datetime.utcnow();B[_Q]=D.remote;B[_R]=D.method;B[_S]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_X)
		if type(E)is web.Response:A=E;M=L;B[_E]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(I,B);return A
		else:assert type(E)==str;H=E;assert H!=_I;J=utils.Encoding[H.rsplit(_F,1)[1]]
		if F==_A or F=='':A=web.Response(status=204)
		else:A=web.Response(status=404);A.content_type=H;J=utils.Encoding[A.content_type.rsplit(_F,1)[1]];K=utils.gen_rc_errors(_J,_V,error_message=_A4);N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(K,J,C.dm4errors,N);B[_D]=K
		B[_E]=A.status;await C._insert_bootstrapping_log_entry(I,B);return A
	async def handle_post_config_request(C,request):
		D=request;F=D.path[C.len_prefix_running:];G=await C._check_auth(D,F)
		if type(G)is web.Response:A=G;return A
		else:J=G
		B={};B[_P]=datetime.datetime.utcnow();B[_Q]=D.remote;B[_R]=D.method;B[_S]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_c)
		if type(E)is web.Response:A=E;M=L;B[_E]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(J,B);return A
		else:assert type(E)==str;H=E;assert H!=_I;K=utils.Encoding[H.rsplit(_F,1)[1]]
		if F==_A or F=='':A=web.Response(status=400);I=utils.gen_rc_errors(_U,_W,error_message=_o)
		else:A=web.Response(status=404);I=utils.gen_rc_errors(_J,_V,error_message=_p)
		A.content_type=H;K=utils.Encoding[A.content_type.rsplit(_F,1)[1]];N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(I,K,C.dm4errors,N);B[_E]=A.status;B[_D]=I;await C._insert_bootstrapping_log_entry(J,B);return A
	async def handle_put_config_request(C,request):
		D=request;F=D.path[C.len_prefix_running:];G=await C._check_auth(D,F)
		if type(G)is web.Response:A=G;return A
		else:J=G
		B={};B[_P]=datetime.datetime.utcnow();B[_Q]=D.remote;B[_R]=D.method;B[_S]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_c)
		if type(E)is web.Response:A=E;M=L;B[_E]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(J,B);return A
		else:assert type(E)==str;H=E;assert H!=_I;K=utils.Encoding[H.rsplit(_F,1)[1]]
		if F==_A or F=='':A=web.Response(status=400);I=utils.gen_rc_errors(_U,_W,error_message=_o)
		else:A=web.Response(status=404);I=utils.gen_rc_errors(_J,_V,error_message=_p)
		A.content_type=H;K=utils.Encoding[A.content_type.rsplit(_F,1)[1]];N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(I,K,C.dm4errors,N);B[_E]=A.status;B[_D]=I;await C._insert_bootstrapping_log_entry(J,B);return A
	async def handle_delete_config_request(C,request):
		D=request;G=D.path[C.len_prefix_running:];H=await C._check_auth(D,G)
		if type(H)is web.Response:A=H;return A
		else:L=H
		B={};B[_P]=datetime.datetime.utcnow();B[_Q]=D.remote;B[_R]=D.method;B[_S]=D.path;E,M=utils.check_http_headers(D,C.supported_media_types,accept_required=_c)
		if type(E)is web.Response:A=E;N=M;B[_E]=A.status;B[_D]=N;await C._insert_bootstrapping_log_entry(L,B);return A
		else:
			assert type(E)==str;I=E
			if I==_I:J=_C
			else:J=utils.Encoding[I.rsplit(_F,1)[1]]
		if G==_A or G=='':A=web.Response(status=400);F=_o;K=utils.gen_rc_errors(_U,_W,error_message=F)
		else:A=web.Response(status=404);F=_p;K=utils.gen_rc_errors(_J,_V,error_message=F)
		A.content_type=I
		if J is _C:A.text=F
		else:O=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(K,J,C.dm4errors,O)
		B[_E]=A.status;B[_D]=K;await C._insert_bootstrapping_log_entry(L,B);return A
	async def handle_action_request(C,request):
		D=request;F=D.path[C.len_prefix_operational:];G=await C._check_auth(D,F)
		if type(G)is web.Response:A=G;return A
		else:J=G
		B={};B[_P]=datetime.datetime.utcnow();B[_Q]=D.remote;B[_R]=D.method;B[_S]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_c)
		if type(E)is web.Response:A=E;M=L;B[_E]=A.status;B[_D]=M;await C._insert_bootstrapping_log_entry(J,B);return A
		else:assert type(E)==str;H=E;assert H!=_I;K=utils.Encoding[H.rsplit(_F,1)[1]]
		if F==_A or F=='':A=web.Response(status=400);I=utils.gen_rc_errors(_U,_W,error_message='Resource does not support action.')
		else:A=web.Response(status=404);I=utils.gen_rc_errors(_J,_V,error_message=_A5)
		A.content_type=H;K=utils.Encoding[A.content_type.rsplit(_F,1)[1]];N=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(I,K,C.dm4errors,N);B[_E]=A.status;B[_D]=I;await C._insert_bootstrapping_log_entry(J,B);return A
	async def handle_rpc_request(C,request):
		P='sleep';D=request;F=D.path[C.len_prefix_operations:];J=await C._check_auth(D,F)
		if type(J)is web.Response:A=J;return A
		else:E=J
		B={};B[_P]=datetime.datetime.utcnow();B[_Q]=D.remote;B[_R]=D.method;B[_S]=D.path;H,M=utils.check_http_headers(D,C.supported_media_types,accept_required=_c)
		if type(H)is web.Response:A=H;N=M;B[_E]=A.status;B[_D]=N;await C._insert_bootstrapping_log_entry(E,B);return A
		else:
			assert type(H)==str;K=H
			if K==_I:L=_C
			else:L=utils.Encoding[K.rsplit(_F,1)[1]]
		if F==_q:
			async with C.nvh.fifolock(Read):
				if os.environ.get('SZTPD_MODE')and P in D.query:await asyncio.sleep(int(D.query[P]))
				A=await C._handle_get_bootstrapping_data_rpc(E,D,B);B[_E]=A.status;await C._insert_bootstrapping_log_entry(E,B);return A
		elif F==_A6:
			try:A=await C._handle_report_progress_rpc(E,D,B)
			except NotImplementedError as Q:raise NotImplementedError('is this ever called?')
			B[_E]=A.status;await C._insert_bootstrapping_log_entry(E,B);return A
		elif F==_A or F=='':A=web.Response(status=400);G=_A5;I=utils.gen_rc_errors(_U,_W,error_message=G)
		else:A=web.Response(status=404);G='Unrecognized RPC.';I=utils.gen_rc_errors(_J,_V,error_message=G)
		A.content_type=K
		if A.content_type==_I:A.text=G
		else:I=utils.gen_rc_errors(_J,_W,error_message=G);O=C.dm4errors.get_schema_node(_A);A.text=utils.obj_to_encoded_str(I,L,C.dm4errors,O)
		B[_E]=A.status;B[_D]=I;await C._insert_bootstrapping_log_entry(E,B);return A
	async def _check_auth(A,request,data_path):
		z='num-times-accessed';y='local-truststore-reference';x=':device-type';w='identity-certificates';v='activation-code';u='" not found for any tenant.';t='Device "';s='X-Client-Cert';e='verification';d='device-type';T='sbi-access-stats';P='lifecycle-statistics';J='comment';I='failure';H='outcome';C=request
		def F(request,supported_media_types):
			E='Accept';D=supported_media_types;C=request;B=web.Response(status=401)
			if E in C.headers and any((C.headers[E]==A for A in D)):B.content_type=C.headers[E]
			elif _e in C.headers and any((C.headers[_e]==A for A in D)):B.content_type=C.headers[_e]
			else:B.content_type=_I
			if B.content_type!=_I:F=utils.Encoding[B.content_type.rsplit(_F,1)[1]];G=utils.gen_rc_errors(_J,_A7);H=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(G,F,A.dm4errors,H)
			return B
		B={};B[_P]=datetime.datetime.utcnow();B[_Q]=C.remote;B['source-proxies']=list(C.forwarded);B['host']=C.host;B[_R]=C.method;B[_S]=C.path;K=set();M=_C;N=C.transport.get_extra_info('peercert')
		if N is not _C:O=N['subject'][-1][0][1];K.add(O)
		elif C.headers.get(s)!=_C:f=C.headers.get(s);U=bytes(urllib.parse.unquote(f),'utf-8');M=x509.load_pem_x509_certificate(U,default_backend());g=M.subject;O=g.get_attributes_for_oid(x509.ObjectIdentifier('2.5.4.5'))[0].value;K.add(O)
		Q=_C;V=_C;R=C.headers.get('AUTHORIZATION')
		if R!=_C:Q,V=basicauth.decode(R);K.add(Q)
		if len(K)==0:B[H]=I;B[J]='Device provided no identification credentials.';await A._insert_audit_log_entry(_C,B);return F(C,A.supported_media_types)
		if len(K)!=1:B[H]=I;B[J]='Device provided mismatched authentication credentials ('+O+' != '+Q+').';await A._insert_audit_log_entry(_C,B);return F(C,A.supported_media_types)
		E=K.pop();D=_C
		if A.mode==_T:L=_A+A.dal.app_ns+_f
		elif A.mode==_d:L=_A+A.dal.app_ns+_A1+E
		if A.mode!=_a:
			try:D=await A.dal.handle_get_opstate_request(L)
			except dal.NodeNotFound as W:B[H]=I;B[J]=t+E+u;await A._insert_audit_log_entry(_C,B);return F(C,A.supported_media_types)
			G=_C
		else:
			try:G=await A.dal.get_tenant_name_for_global_key(_A+A.dal.app_ns+':tenants/tenant/devices/device',E)
			except dal.NodeNotFound as W:B[H]=I;B[J]=t+E+u;await A._insert_audit_log_entry(_C,B);return F(C,A.supported_media_types)
			L=_A+A.dal.app_ns+_b+G+_A2+E;D=await A.dal.handle_get_opstate_request(L)
		assert D!=_C;assert A.dal.app_ns+_f in D;D=D[A.dal.app_ns+_f]
		if A.mode!=_T:D=D[0]
		if v in D:
			if R==_C:B[H]=I;B[J]='Activation code required but none passed for serial number '+E;await A._insert_audit_log_entry(G,B);return F(C,A.supported_media_types)
			X=D[v];assert X.startswith('$5$')
			if not sha256_crypt.verify(V,X):B[H]=I;B[J]='Activation code mismatch for serial number '+E;await A._insert_audit_log_entry(G,B);return F(C,A.supported_media_types)
		else:0
		assert d in D;h=_A+A.dal.app_ns+':device-types/device-type='+D[d];Y=await A.dal.handle_get_opstate_request(h)
		if w in Y[A.dal.app_ns+x][0]:
			if N is _C and M is _C:B[H]=I;B[J]='Client cert required but none passed for serial number '+E;await A._insert_audit_log_entry(G,B);return F(C,A.supported_media_types)
			if N:Z=C.transport.get_extra_info(_A8);assert Z is not _C;a=Z.getpeercert(_X)
			else:assert M is not _C;a=U
			S=Y[A.dal.app_ns+x][0][w];assert e in S;assert y in S[e];b=S[e][y];i=_A+A.dal.app_ns+':truststore/certificate-bags/certificate-bag='+b['certificate-bag']+'/certificate='+b['certificate'];j=await A.dal.handle_get_config_request(i);k=j[A.dal.app_ns+':certificate'][0]['cert-data'];l=base64.b64decode(k);m,n=der_decoder(l,asn1Spec=rfc5652.ContentInfo());assert not n;o=utils.degenerate_cms_obj_to_ders(m);p=ValidationContext(trust_roots=o);q=CertificateValidator(a,validation_context=p)
			try:q._validate_path()
			except PathBuildingError as W:B[H]=I;B[J]="Client cert for serial number '"+E+"' does not validate using trust anchors specified by device-type '"+D[d]+"'";await A._insert_audit_log_entry(G,B);return F(C,A.supported_media_types)
		B[H]='success';await A._insert_audit_log_entry(G,B);r=L+'/lifecycle-statistics';c=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
		if D[P][T][z]==0:D[P][T]['first-accessed']=c
		D[P][T]['last-accessed']=c;D[P][T][z]+=1;await A.dal.handle_put_opstate_request(r,D[P]);return E,G
	async def _handle_get_bootstrapping_data_rpc(A,device_id,request,bootstrapping_log_entry):
		Av='ietf-sztp-bootstrap-server:output';Au='ASCII';At='content';As='contentType';Ar=':configuration';Aq='configuration-handling';Ap='script';Ao='hash-value';An='hash-algorithm';Am='address';Al='referenced-definition';Ak='exited-normally';Aj='function';Ai='plugin';Ah='callout-type';Ag='serial-number';Af='rpc-supported';Ae='not';Ad='match-criteria';Ac='matched-response';Ab='input';AJ='post-configuration-script';AI='configuration';AH='pre-configuration-script';AG='os-version';AF='os-name';AE='trust-anchor';AD='port';AC='bootstrap-server';AB='ietf-sztp-conveyed-info:redirect-information';AA='data-missing';A9='response-manager';A8='operation-not-supported';z='image-verification';y='download-uri';x='boot-image';w='callback-results';v='selected-response';u='value';n=device_id;m='onboarding-information';i='error-tag';h='key';e='ietf-sztp-conveyed-info:onboarding-information';d='redirect-information';c='error';Y=request;X='ietf-restconf:errors';N='response';J='managed-response';I='response-details';E='get-bootstrapping-data-event';D='conveyed-information';C=bootstrapping_log_entry;j,AK=utils.check_http_headers(Y,A.supported_media_types,accept_required=_X)
		if type(j)is web.Response:B=j;AL=AK;C[_E]=B.status;C[_D]=AL;return B
		else:assert type(j)==str;O=j;assert O!=_I;S=utils.Encoding[O.rsplit(_F,1)[1]]
		K=_C
		if Y.body_exists:
			AM=await Y.text();AN=utils.Encoding[Y.headers[_e].rsplit(_F,1)[1]]
			try:G=A.dm.get_schema_node(_q);K=utils.encoded_str_to_obj(AM,AN,A.dm,G)
			except Exception as Z:B=web.Response(status=400);o=_l+str(Z);B.content_type=O;H=utils.gen_rc_errors(_J,_g,error_message=o);G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,S,A.dm4errors,G);C[_D]=H;return B
			if not _K in K:
				B=web.Response(status=400)
				if not _K in K:o=_l+_A9
				B.content_type=O;H=utils.gen_rc_errors(_J,_g,error_message=o);G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,S,A.dm4errors,G);C[_D]=H;return B
		C[_B]={};C[_B][E]={};C[_B][E][_h]={}
		if K is _C:C[_B][E][_h]['no-input-passed']=[_C]
		else:
			C[_B][E][_h][Ab]=[]
			for A0 in K[_K].keys():input={};input[h]=A0;input[u]=K[_K][A0];C[_B][E][_h][Ab].append(input)
		if A.mode!=_a:P=_A+A.dal.app_ns+':'
		else:P=_A+A.dal.app_ns+_b+n[1]+_A
		if A.mode==_T:A1=P+'device'
		else:A1=P+'devices/device='+n[0]
		try:R=await A.dal.handle_get_config_request(A1)
		except Exception as Z:B=web.Response(status=501);B.content_type=_j;H=utils.gen_rc_errors(_U,A8,error_message='Unhandled exception: '+str(Z));B.text=utils.enc_rc_errors('json',H);return B
		assert R!=_C;assert A.dal.app_ns+_f in R;R=R[A.dal.app_ns+_f]
		if A.mode!=_T:R=R[0]
		if A9 not in R or Ac not in R[A9]:B=web.Response(status=404);B.content_type=O;H=utils.gen_rc_errors(_U,AA,error_message='No responses configured.');G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,S,A.dm4errors,G);C[_D]=H;C[_B][E][v]='no-responses-configured';return B
		F=_C
		for k in R[A9][Ac]:
			if not Ad in k:F=k;break
			if K is _C:continue
			for Q in k[Ad]['match']:
				if Q[h]not in K[_K]:break
				if'present'in Q:
					if Ae in Q:
						if Q[h]in K[_K]:break
					elif Q[h]not in K[_K]:break
				elif u in Q:
					if Ae in Q:
						if Q[u]==K[_K][Q[h]]:break
					elif Q[u]!=K[_K][Q[h]]:break
				else:raise NotImplementedError("Unrecognized 'match' expression.")
			else:F=k;break
		if F is _C or'none'in F[N]:
			if F is _C:C[_B][E][v]='no-match-found'
			else:C[_B][E][v]=F[_H]+" (explicit 'none')"
			B=web.Response(status=404);B.content_type=O;H=utils.gen_rc_errors(_U,AA,error_message='No matching responses configured.');G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,S,A.dm4errors,G);C[_D]=H;return B
		C[_B][E][v]=F[_H];C[_B][E][I]={J:{}}
		if D in F[N]:
			C[_B][E][I][J]={D:{}};M={}
			if _G in F[N][D]:
				C[_B][E][I][J][D]={_G:{}};assert _Y in F[N][D][_G];p=F[N][D][_G][_Y];C[_B][E][I][J][D][_G][_H]=p;V=await A.dal.handle_get_config_request(P+'dynamic-callouts/dynamic-callout='+p);assert p==V[A.dal.app_ns+_L][0][_H];C[_B][E][I][J][D][_G][Af]=V[A.dal.app_ns+_L][0][Af];a={}
				if A.mode!=_T:a[Ag]=n[0]
				else:a[Ag]='mode-0 == no-sn'
				a['source-ip-address']=Y.remote
				if K:a['from-device']=K[_K]
				A2=Y.transport.get_extra_info(_A8)
				if A2:
					A3=A2.getpeercert(_X)
					if A3:a['identity-certificate']=A3
				if _i in V[A.dal.app_ns+_L][0]:
					C[_B][E][I][J][D][_G][Ah]=_i;A4=V[A.dal.app_ns+_L][0][_i][Ai];A5=V[A.dal.app_ns+_L][0][_i][Aj];C[_B][E][I][J][D][_G]['callback-details']={Ai:A4,Aj:A5};C[_B][E][I][J][D][_G][w]={};L=_C
					try:L=A.nvh.plugins[A4]['functions'][A5](a)
					except Exception as Z:C[_B][E][I][J][D][_G][w]['exception-thrown']=str(Z);B=web.Response(status=500);B.content_type=O;H=utils.gen_rc_errors(_U,A8,error_message='Server encountered an error while trying to generate a response: '+str(Z));G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,S,A.dm4errors,G);C[_D]=H;return B
					assert L and type(L)==dict
					if X in L:
						assert len(L[X][c])==1
						if any((A==L[X][c][0][i]for A in(_W,'too-big','missing-attribute','bad-attribute','unknown-attribute','bad-element',_V,'unknown-namespace',_g))):B=web.Response(status=400)
						elif any((A==L[X][c][0][i]for A in _A7)):B=web.Response(status=403)
						elif any((A==L[X][c][0][i]for A in('in-use','lock-denied','resource-denied','data-exists',AA))):B=web.Response(status=409)
						elif any((A==L[X][c][0][i]for A in('rollback-failed','operation-failed','partial-operation'))):B=web.Response(status=500)
						elif any((A==L[X][c][0][i]for A in A8)):B=web.Response(status=501)
						else:raise NotImplementedError('Unrecognized error-tag: '+L[X][c][0][i])
						B.content_type=O;H=L;G=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(H,S,A.dm4errors,G);C[_D]=L;C[_B][E][I][J][D][_G][w][Ak]='Returning an RPC-error provided by callback (NOTE: RPC-error != exception, hence a normal exit).';return B
					else:C[_B][E][I][J][D][_G][w][Ak]='Returning conveyed information provided by callback.'
				elif _r in V[A.dal.app_ns+_L][0]:C[_B][E][I][J][D][_G][Ah]=_m;raise NotImplementedError('webhooks callout support pending!')
				else:raise NotImplementedError('unhandled dynamic callout type: '+str(V[A.dal.app_ns+_L][0]))
				M=L
			elif d in F[N][D]:
				C[_B][E][I][J][D]={d:{}};M[AB]={};M[AB][AC]=[]
				if _Y in F[N][D][d]:
					f=F[N][D][d][_Y];C[_B][E][I][J][D][d]={Al:f};q=await A.dal.handle_get_config_request(P+'conveyed-information-responses/redirect-information-response='+f)
					for AO in q[A.dal.app_ns+':redirect-information-response'][0][d][AC]:
						W=await A.dal.handle_get_config_request(P+'bootstrap-servers/bootstrap-server='+AO);W=W[A.dal.app_ns+':bootstrap-server'][0];l={};l[Am]=W[Am]
						if AD in W:l[AD]=W[AD]
						if AE in W:l[AE]=W[AE]
						M[AB][AC].append(l)
				else:raise NotImplementedError('unhandled redirect-information config type: '+str(F[N][D][d]))
			elif m in F[N][D]:
				C[_B][E][I][J][D]={};M[e]={}
				if _Y in F[N][D][m]:
					f=F[N][D][m][_Y];C[_B][E][I][J][D][m]={Al:f};q=await A.dal.handle_get_config_request(P+'conveyed-information-responses/onboarding-information-response='+f);T=q[A.dal.app_ns+':onboarding-information-response'][0][m]
					if x in T:
						AP=T[x];AQ=await A.dal.handle_get_config_request(P+'boot-images/boot-image='+AP);U=AQ[A.dal.app_ns+':boot-image'][0];M[e][x]={};b=M[e][x]
						if AF in U:b[AF]=U[AF]
						if AG in U:b[AG]=U[AG]
						if y in U:
							b[y]=list()
							for AR in U[y]:b[y].append(AR)
						if z in U:
							b[z]=list()
							for A6 in U[z]:r={};r[An]=A6[An];r[Ao]=A6[Ao];b[z].append(r)
					if AH in T:AS=T[AH];AT=await A.dal.handle_get_config_request(P+'scripts/pre-configuration-script='+AS);M[e][AH]=AT[A.dal.app_ns+':pre-configuration-script'][0][Ap]
					if AI in T:AU=T[AI];A7=await A.dal.handle_get_config_request(P+'configurations/configuration='+AU);M[e][Aq]=A7[A.dal.app_ns+Ar][0][Aq];M[e][AI]=A7[A.dal.app_ns+Ar][0]['config']
					if AJ in T:AV=T[AJ];AW=await A.dal.handle_get_config_request(P+'scripts/post-configuration-script='+AV);M[e][AJ]=AW[A.dal.app_ns+':post-configuration-script'][0][Ap]
			else:raise NotImplementedError('unhandled conveyed-information type: '+str(F[N][D]))
		else:raise NotImplementedError('unhandled response type: '+str(F[N]))
		g=rfc5652.ContentInfo()
		if O==_j:g[As]=A.id_ct_sztpConveyedInfoJSON;g[At]=encode_der(json.dumps(M,indent=2),asn1Spec=univ.OctetString())
		else:assert O==_s;g[As]=A.id_ct_sztpConveyedInfoXML;G=A.dm4conveyedinfo.get_schema_node(_A);assert G;AX=utils.obj_to_encoded_str(M,S,A.dm4conveyedinfo,G);g[At]=encode_der(AX,asn1Spec=univ.OctetString())
		AY=encode_der(g,rfc5652.ContentInfo());s=base64.b64encode(AY).decode(Au);AZ=base64.b64decode(s);Aa=base64.b64encode(AZ).decode(Au);assert s==Aa;t={};t[Av]={};t[Av][D]=s;B=web.Response(status=200);B.content_type=O;G=A.dm.get_schema_node(_q);B.text=utils.obj_to_encoded_str(t,S,A.dm,G);return B
	async def _handle_report_progress_rpc(A,device_id,request,bootstrapping_log_entry):
		j='remote-port';i='wn-sztpd-rpcs:input';h='webhook-results';Y='tcp-client-parameters';X='encoding';V=device_id;U='http';L=request;H='report-progress-event';C=bootstrapping_log_entry;M,Z=utils.check_http_headers(L,A.supported_media_types,accept_required=_c)
		if type(M)is web.Response:B=M;a=Z;C[_E]=B.status;C[_D]=a;return B
		else:assert type(M)==str;I=M
		if I!=_I:R=utils.Encoding[I.rsplit(_F,1)[1]]
		if not L.body_exists:
			G='RPC "input" node missing (required for "report-progress").';B=web.Response(status=400);B.content_type=I
			if B.content_type==_I:B.text=G
			else:E=utils.gen_rc_errors(_J,_W,error_message=G);F=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(E,R,A.dm4errors,F)
			C[_D]=B.text;return B
		b=utils.Encoding[L.headers[_e].rsplit(_F,1)[1]];c=await L.text()
		try:F=A.dm.get_schema_node(_A6);N=utils.encoded_str_to_obj(c,b,A.dm,F)
		except Exception as O:B=web.Response(status=400);G=_l+str(O);B.content_type=I;E=utils.gen_rc_errors(_J,_g,error_message=G);F=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(E,R,A.dm4errors,F);C[_D]=E;return B
		if not _K in N:
			B=web.Response(status=400)
			if not _K in N:G=_l+_A9
			B.content_type=I;E=utils.gen_rc_errors(_J,_g,error_message=G);F=A.dm4errors.get_schema_node(_A);B.text=utils.obj_to_encoded_str(E,R,A.dm4errors,F);C[_D]=E;return B
		C[_B]={};C[_B][H]={};C[_B][H][_h]=N[_K];C[_B][H][_G]={}
		if A.mode==_T or A.mode==_d:J=_A+A.dal.app_ns+':preferences/notification-delivery'
		elif A.mode==_a:J=_A+A.dal.app_ns+_b+V[1]+'/preferences/notification-delivery'
		try:d=await A.dal.handle_get_config_request(J)
		except Exception as O:C[_B][H][_G]['no-callout-configured']=[_C]
		else:
			S=d[A.dal.app_ns+':notification-delivery'][_G][_Y];C[_B][H][_G][_H]=S
			if A.mode==_T or A.mode==_d:J=_A+A.dal.app_ns+':dynamic-callouts/dynamic-callout='+S
			elif A.mode==_a:J=_A+A.dal.app_ns+_b+V[1]+'/dynamic-callouts/dynamic-callout='+S
			P=await A.dal.handle_get_config_request(J);C[_B][H][_G][h]={_m:[]};T={};T[i]={};T[i]['notification']=N;e=json.dumps(T,indent=2);f='FIXME: xml output'
			if _i in P[A.dal.app_ns+_L][0]:raise NotImplementedError('callback support not implemented yet')
			elif _r in P[A.dal.app_ns+_L][0]:
				for D in P[A.dal.app_ns+_L][0][_r][_m]:
					K={};K[_H]=D[_H]
					if X not in D or D[X]=='json':W=e
					elif D[X]=='xml':W=f
					if U in D:
						Q='http://'+D[U][Y]['remote-address']
						if j in D[U][Y]:Q+=':'+str(D[U][Y][j])
						Q+='/relay-notification';K['uri']=Q
						try:
							async with aiohttp.ClientSession()as g:B=await g.post(Q,data=W)
						except aiohttp.client_exceptions.ClientConnectorError as O:K['connection-error']=str(O)
						else:
							K['http-status-code']=B.status
							if B.status==200:break
					else:assert'https'in D;raise NotImplementedError('https-based webhook is not supported yet.')
					C[_B][H][_G][h][_m].append(K)
			else:raise NotImplementedError('unrecognized callout type '+str(P[A.dal.app_ns+_L][0]))
		B=web.Response(status=204);return B