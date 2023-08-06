# Copyright (c) 2021 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_A3=' found): '
_A2='The asymmetric-key has a mismatched public/private key pair: '
_A1=b"this is some data I'd like to sign"
_A0='Unsupported "private-key-format" ('
_z='ietf-crypto-types:ec-private-key-format'
_y='cleartext-private-key'
_x='Parsing public key structure failed for '
_w='Unsupported "public-key-format" ('
_v='ietf-crypto-types:subject-public-key-info-format'
_u='should check to see if an alarm can be cleared...'
_t='admin-account'
_s='$0$'
_r='%Y-%m-%dT%H:%M:%SZ'
_q='password-last-modified'
_p='module'
_o='sztpd.plugins.'
_n="why wasn't this assertion caught by val? "
_m='operation-failed'
_l='data-exists'
_k='missing-attribute'
_j='Unable to parse "input" JSON document: '
_i='malformed-message'
_h='method'
_g='": '
_f='cert-data'
_e='public-key'
_d='\\g<1>'
_c='.*plugins/plugin=([^/]*).*'
_b='function'
_a='application/yang-data+json'
_Z='private-key-format'
_Y=') for '
_X='public-key-format'
_W='need to implement this code'
_V='SZTPD_MODE'
_U='plugin'
_T=')'
_S=' ('
_R=False
_Q='operation-not-supported'
_P=True
_O='functions'
_N='name'
_M='certificate'
_L='certificates'
_K='+'
_J='text/plain'
_I='password'
_H='unknown-element'
_G='sleep'
_F='invalid-value'
_E='application'
_D='protocol'
_C='asymmetric-key'
_B=None
_A='/'
import os,re,sys,json,base64,signal,asyncio,yangson,datetime,basicauth,importlib,pkg_resources
from enum import Enum
from aiohttp import web
from enum import IntFlag
from fifolock import FifoLock
from passlib.hash import sha256_crypt
from .dal import DataAccessLayer
from .val import ValidationLayer
from .rcsvr import RestconfServer
from .handler import RouteHandler
from .  import dal
from .  import val
from .  import utils
from pyasn1.codec.der.encoder import encode as encode_der
from pyasn1.codec.der.decoder import decode as decode_der
from pyasn1.error import PyAsn1Error
from pyasn1_modules import rfc4055
from pyasn1_modules import rfc5280
from pyasn1_modules import rfc5480
from pyasn1_modules import rfc5915
from pyasn1_modules import rfc5652
from pyasn1.type import univ
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from cryptography.x509.oid import ExtensionOID
class RefAction(IntFlag):ADDED=1;REMOVED=2
class TimeUnit(Enum):Days=2;Hours=1;Minutes=0
class Period:
	def __init__(A,amount,units):A.amount=amount;A.units=units
class PluginNotFound(Exception):0
class PluginSyntaxError(Exception):0
class FunctionNotFound(Exception):0
class FunctionNotCallable(Exception):0
class Read(asyncio.Future):
	@staticmethod
	def is_compatible(holds):return not holds[Write]
class Write(asyncio.Future):
	@staticmethod
	def is_compatible(holds):A=holds;return not A[Read]and not A[Write]
class NativeViewHandler(RouteHandler):
	len_prefix_running=RestconfServer.len_prefix_running;len_prefix_operational=RestconfServer.len_prefix_operational;len_prefix_operations=RestconfServer.len_prefix_operations;supported_media_types=_a,
	def __init__(A,_dal,_mode,_loop):
		W=':tenants/tenant/truststore/certificate-bags/certificate-bag/certificate/cert-data';V=':tenants/tenant/keystore/asymmetric-keys/asymmetric-key/certificates/certificate/cert-data';U=':tenants/tenant/keystore/asymmetric-keys/asymmetric-key/cleartext-private-key';T=':tenants/tenant/keystore/asymmetric-keys/asymmetric-key/public-key';S=':truststore/certificate-bags/certificate-bag/certificate/cert-data';R=':keystore/asymmetric-keys/asymmetric-key/certificates/certificate/cert-data';Q=':keystore/asymmetric-keys/asymmetric-key/cleartext-private-key';P=':keystore/asymmetric-keys/asymmetric-key/public-key';O=':preferences/system/plugins/plugin/functions/function';N=':preferences/system/plugins/plugin';M=':tenants/tenant/admin-accounts/admin-account/password';L=':admin-accounts/admin-account/password';K=':plugins';A.dal=_dal;A.mode=_mode;A.loop=_loop;A.fifolock=FifoLock();A.create_callbacks={};A.change_callbacks={};A.delete_callbacks={};A.subtree_change_callbacks={};A.somehow_change_callbacks={};A.leafref_callbacks={};A.periodic_callbacks={};A.onetime_callbacks={};A.plugins={};B=A.dal.handle_get_opstate_request('/ietf-yang-library:yang-library');F=A.loop.run_until_complete(B);G=pkg_resources.resource_filename('sztpd','yang/');A.dm=yangson.DataModel(json.dumps(F),[G]);A.val=ValidationLayer(A.dm,A.dal);B=A.dal.handle_get_opstate_request(_A+A.dal.app_ns+':preferences/system/plugins')
		try:D=A.loop.run_until_complete(B)
		except dal.NodeNotFound:pass
		else:
			if _U in D[A.dal.app_ns+K]:
				for C in D[A.dal.app_ns+K][_U]:
					H=C[_N];B=_handle_plugin_created('',{_U:C},'',A);A.loop.run_until_complete(B)
					if _O in C:
						for E in C[_O][_b]:X=E[_N];I='FOO/plugins/plugin='+H+'/BAR';B=_handle_function_created('',{_b:E},I,A);A.loop.run_until_complete(B)
		A.register_create_callback(_A+A.dal.app_ns+L,_handle_admin_passwd_created);A.register_change_callback(_A+A.dal.app_ns+L,_handle_admin_passwd_changed)
		if A.mode=='x':A.register_create_callback(_A+A.dal.app_ns+M,_handle_admin_passwd_created);A.register_change_callback(_A+A.dal.app_ns+M,_handle_admin_passwd_changed)
		A.register_create_callback(_A+A.dal.app_ns+':tenants/tenant',_handle_tenant_created);A.register_create_callback(_A+A.dal.app_ns+N,_handle_plugin_created);A.register_delete_callback(_A+A.dal.app_ns+N,_handle_plugin_deleted);A.register_create_callback(_A+A.dal.app_ns+O,_handle_function_created);A.register_delete_callback(_A+A.dal.app_ns+O,_handle_function_deleted);A.register_create_callback(_A+A.dal.app_ns+P,_handle_asymmetric_public_key_created_or_changed);A.register_change_callback(_A+A.dal.app_ns+P,_handle_asymmetric_public_key_created_or_changed);A.register_create_callback(_A+A.dal.app_ns+Q,_handle_asymmetric_private_key_created_or_changed);A.register_change_callback(_A+A.dal.app_ns+Q,_handle_asymmetric_private_key_created_or_changed);A.register_create_callback(_A+A.dal.app_ns+R,_handle_asymmetric_key_cert_created_or_changed);A.register_change_callback(_A+A.dal.app_ns+R,_handle_asymmetric_key_cert_created_or_changed);A.register_create_callback(_A+A.dal.app_ns+S,_handle_trust_anchor_cert_created_or_changed);A.register_change_callback(_A+A.dal.app_ns+S,_handle_trust_anchor_cert_created_or_changed)
		if A.mode=='x':A.register_create_callback(_A+A.dal.app_ns+T,_handle_asymmetric_public_key_created_or_changed);A.register_change_callback(_A+A.dal.app_ns+T,_handle_asymmetric_public_key_created_or_changed);A.register_create_callback(_A+A.dal.app_ns+U,_handle_asymmetric_private_key_created_or_changed);A.register_change_callback(_A+A.dal.app_ns+U,_handle_asymmetric_private_key_created_or_changed);A.register_create_callback(_A+A.dal.app_ns+V,_handle_asymmetric_key_cert_created_or_changed);A.register_change_callback(_A+A.dal.app_ns+V,_handle_asymmetric_key_cert_created_or_changed);A.register_create_callback(_A+A.dal.app_ns+W,_handle_trust_anchor_cert_created_or_changed);A.register_change_callback(_A+A.dal.app_ns+W,_handle_trust_anchor_cert_created_or_changed)
		A.register_change_callback(_A+A.dal.app_ns+':transport/listen',_handle_transport_changed);A.register_delete_callback(_A+A.dal.app_ns+':transport',_handle_transport_delete);A.register_periodic_callback(Period(24,TimeUnit.Hours),datetime.datetime(2000,1,1,0),_check_expirations)
		for J in A.dal.ref_stat_collectors:A.register_create_callback(J.replace('/reference-statistics',''),_handle_ref_stat_parent_created)
	def register_create_callback(A,schema_path,callback):
		C=callback;B=schema_path
		if B not in A.create_callbacks:A.create_callbacks[B]=[C]
		else:A.create_callbacks[B].append(C)
	def register_change_callback(A,schema_path,callback):
		C=callback;B=schema_path
		if B not in A.change_callbacks:A.change_callbacks[B]=[C]
		else:A.change_callbacks[B].append(C)
	def register_subtree_change_callback(A,schema_path,callback):
		C=callback;B=schema_path
		if B not in A.subtree_change_callbacks:A.subtree_change_callbacks[B]=[C]
		else:A.subtree_change_callbacks[B].append(C)
	def register_somehow_change_callback(A,schema_path,callback):
		C=callback;B=schema_path
		if B not in A.somehow_change_callbacks:A.somehow_change_callbacks[B]=[C]
		else:A.somehow_change_callbacks[B].append(C)
	def register_delete_callback(A,schema_path,callback):
		C=callback;B=schema_path
		if B not in A.delete_callbacks:A.delete_callbacks[B]=[C]
		else:A.delete_callbacks[B].append(C)
	def register_onetime_callback(A,timestamp,callback,opaque):
		B=callback
		if schema_path not in A.onetime_callbacks:A.onetime_callbacks[schema_path]=[B]
		else:A.onetime_callbacks[schema_path].append(B)
	def register_periodic_callback(A,period,anchor,callback):0
	def register_leafref_callback(A,schema_path,callback):
		C=callback;B=schema_path
		if B not in A.leafref_callbacks:A.leafref_callbacks[B]=[C]
		else:A.leafref_callbacks[B].append(C)
	async def _insert_audit_log_entry(A,tenant_name,audit_log_entry):
		C=audit_log_entry;B=tenant_name
		if C[_h]in{'GET','HEAD'}:return
		if B==_B:D=_A+A.dal.app_ns+':audit-log'
		else:F=A.dal.opaque();assert F=='x';D=_A+A.dal.app_ns+':tenants/tenant='+B+'/audit-log'
		E={};E[A.dal.app_ns+':log-entry']=C;await A.dal.handle_post_opstate_request(D,E)
	async def _check_auth(B,request,data_path):
		S='No authorization required for fresh installs.';R=':admin-accounts/admin-account';N='access-denied';M='failure';L='success';G='comment';F='outcome';D=request;A={};A['timestamp']=datetime.datetime.utcnow();A['source-ip']=D.remote;A['source-proxies']=list(D.forwarded);A['host']=D.host;A[_h]=D.method;A['path']=D.path;J=D.headers.get('AUTHORIZATION')
		if J is _B:
			H=await B.dal.num_elements_in_list(_A+B.dal.app_ns+R)
			if H==0:A[F]=L;A[G]=S;await B._insert_audit_log_entry(_B,A);return web.Response(status=200)
			A[F]=M;A[G]='No authorization specified in the HTTP header.';await B._insert_audit_log_entry(_B,A);C=web.Response(status=401);E=utils.gen_rc_errors(_D,N);C.text=json.dumps(E,indent=2);return C
		I,O=basicauth.decode(J);P=_A+B.dal.app_ns+':admin-accounts/admin-account='+I+'/password'
		try:Q=await B.dal.handle_get_config_request(P)
		except dal.NodeNotFound as T:
			H=await B.dal.num_elements_in_list(_A+B.dal.app_ns+R)
			if H==0:A[F]=L;A[G]=S;await B._insert_audit_log_entry(_B,A);return web.Response(status=200)
			A[F]=M;A[G]='Unknown admin: '+I;await B._insert_audit_log_entry(_B,A);C=web.Response(status=401);E=utils.gen_rc_errors(_D,N);C.text=json.dumps(E,indent=2);return C
		K=Q[B.dal.app_ns+':password'];assert K.startswith('$5$')
		if not sha256_crypt.verify(O,K):A[F]=M;A[G]='Password mismatch for admin '+I;await B._insert_audit_log_entry(_B,A);C=web.Response(status=401);E=utils.gen_rc_errors(_D,N);C.text=json.dumps(E,indent=2);return C
		A[F]=L;await B._insert_audit_log_entry(_B,A);return web.Response(status=200)
	async def handle_get_restconf_root(D,request):
		E=request;G=_A;A=await D._check_auth(E,G)
		if A.status==401:return A
		B,H=utils.check_http_headers(E,D.supported_media_types,accept_required=_P)
		if type(B)is web.Response:A=B;return A
		else:assert type(B)==str;C=B;assert C!=_J;F=utils.Encoding[C.rsplit(_K,1)[1]]
		A=web.Response(status=200);A.content_type=C
		if F==utils.Encoding.json:A.text='{\n    "ietf-restconf:restconf" : {\n        "data" : {},\n        "operations" : {},\n        "yang-library-version" : "2019-01-04"\n    }\n}\n'
		else:assert F==utils.Encoding.xml;A.text='<restconf xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">\n    <data/>\n    <operations/>\n    <yang-library-version>2016-06-21</yang-library-version>\n</restconf>\n'
		return A
	async def handle_get_yang_library_version(D,request):
		E=request;G=_A;A=await D._check_auth(E,G)
		if A.status==401:return A
		B,H=utils.check_http_headers(E,D.supported_media_types,accept_required=_P)
		if type(B)is web.Response:A=B;return A
		else:assert type(B)==str;C=B;assert C!=_J;F=utils.Encoding[C.rsplit(_K,1)[1]]
		A=web.Response(status=200);A.content_type=C
		if F==utils.Encoding.json:A.text='{\n  "ietf-restconf:yang-library-version" : "2019-01-04"\n}'
		else:assert F==utils.Encoding.xml;A.text='<yang-library-version xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">2019-01-04</yang-library-version>'
		return A
	async def handle_get_opstate_request(C,request):
		D=request;E,H=utils.parse_raw_path(D._message.path[RestconfServer.len_prefix_operational:]);A=await C._check_auth(D,E)
		if A.status==401:return A
		B,J=utils.check_http_headers(D,C.supported_media_types,accept_required=_P)
		if type(B)is web.Response:I=B;return I
		else:assert type(B)==str;F=B;assert F!=_J;K=utils.Encoding[F.rsplit(_K,1)[1]]
		A,G=await C.handle_get_opstate_request_lower_half(E,H)
		if G!=_B:A.text=json.dumps(G,indent=2)
		return A
	async def handle_get_opstate_request_lower_half(D,data_path,query_dict):
		B=query_dict
		async with D.fifolock(Read):
			if os.environ.get(_V)and _G in B:await asyncio.sleep(int(B[_G]))
			try:F=await D.dal.handle_get_opstate_request(data_path,B)
			except dal.NodeNotFound as C:A=web.Response(status=404);E=utils.gen_rc_errors(_D,_H,error_message=str(C));A.text=json.dumps(E,indent=2);return A,_B
			except NotImplementedError as C:A=web.Response(status=501);E=utils.gen_rc_errors(_E,_Q,error_message=str(C));A.text=json.dumps(resp_text_ob,indent=2j);return A,_B
			A=web.Response(status=200);A.content_type=_a;return A,F
	async def handle_get_config_request(C,request):
		D=request;E,H=utils.parse_raw_path(D._message.path[RestconfServer.len_prefix_running:]);A=await C._check_auth(D,E)
		if A.status==401:return A
		B,J=utils.check_http_headers(D,C.supported_media_types,accept_required=_P)
		if type(B)is web.Response:I=B;return I
		else:assert type(B)==str;F=B;assert F!=_J;K=utils.Encoding[F.rsplit(_K,1)[1]]
		A,G=await C.handle_get_config_request_lower_half(E,H)
		if G!=_B:A.text=json.dumps(G,indent=2)
		return A
	async def handle_get_config_request_lower_half(E,data_path,query_dict):
		F=data_path;D=query_dict
		async with E.fifolock(Read):
			try:await E.val.handle_get_config_request(F,D)
			except val.InvalidDataPath as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_F,error_message=str(B));A.text=json.dumps(C,indent=2);return A,_B
			except val.NonexistentSchemaNode as B:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_F,error_message=str(B));A.text=json.dumps(C,indent=2);return A,_B
			except val.NodeNotFound as B:A=web.Response(status=404);C=utils.gen_rc_errors(_D,_H,error_message=str(B));A.text=json.dumps(C,indent=2);return A,_B
			if os.environ.get(_V)and _G in D:await asyncio.sleep(int(D[_G]))
			try:G=await E.dal.handle_get_config_request(F,D)
			except dal.NodeNotFound as B:A=web.Response(status=404);C=utils.gen_rc_errors(_D,_H,error_message=str(B));A.text=json.dumps(C,indent=2);return A,_B
			A=web.Response(status=200);A.content_type=_a;return A,G
	async def handle_post_config_request(A,request):
		B=request;E,H=utils.parse_raw_path(B._message.path[A.len_prefix_running:]);F=await A._check_auth(B,E)
		if F.status==401:return F
		C,L=utils.check_http_headers(B,A.supported_media_types,accept_required=_R)
		if type(C)is web.Response:D=C;return D
		else:assert type(C)==str;G=C;assert G!=_J;M=utils.Encoding[G.rsplit(_K,1)[1]]
		try:I=await B.json()
		except json.decoder.JSONDecodeError as J:D=web.Response(status=400);K=utils.gen_rc_errors(_D,_i,error_message=_j+str(J));D.text=json.dumps(K,indent=2);return D
		return await A.handle_post_config_request_lower_half(E,H,I)
	async def handle_post_config_request_lower_half(D,data_path,query_dict,request_body):
		G=request_body;F=data_path;E=query_dict
		async with D.fifolock(Write):
			try:await D.val.handle_post_config_request(F,E,G)
			except (val.InvalidInputDocument,val.UnrecognizedQueryParameter,val.InvalidQueryParameter)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_F,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.MissingQueryParameter as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_k,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.NonexistentSchemaNode as B:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_F,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.ValidationFailed as B:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_F,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.ParentNodeNotFound as B:A=web.Response(status=404);C=utils.gen_rc_errors(_D,_H,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.UnrecognizedInputNode as B:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_H,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except NotImplementedError as B:A=web.Response(status=501);C=utils.gen_rc_errors(_E,_Q,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.NodeAlreadyExists as B:A=web.Response(status=409);C=utils.gen_rc_errors(_E,_l,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			if os.environ.get(_V)and _G in E:await asyncio.sleep(int(E[_G]))
			try:await D.dal.handle_post_config_request(F,E,G,D.create_callbacks,D.change_callbacks,D)
			except (dal.CreateCallbackFailed,dal.CreateOrChangeCallbackFailed,dal.ChangeCallbackFailed)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_m,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except (PluginNotFound,PluginSyntaxError,FunctionNotFound,FunctionNotCallable)as B:A=web.Response(status=501);C=utils.gen_rc_errors(_E,_Q,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except Exception as B:raise Exception(_n+str(B))
			D.val.inst=D.val.inst2;D.val.inst2=_B;await D.shared_post_commit_logic();return web.Response(status=201)
	async def handle_put_config_request(A,request):
		B=request;E,H=utils.parse_raw_path(B._message.path[A.len_prefix_running:]);F=await A._check_auth(B,E)
		if F.status==401:return F
		C,L=utils.check_http_headers(B,A.supported_media_types,accept_required=_R)
		if type(C)is web.Response:D=C;return D
		else:assert type(C)==str;G=C;assert G!=_J;M=utils.Encoding[G.rsplit(_K,1)[1]]
		try:I=await B.json()
		except json.decoder.JSONDecodeError as J:D=web.Response(status=400);K=utils.gen_rc_errors(_D,_i,error_message=_j+str(J));D.text=json.dumps(K,indent=2);return D
		return await A.handle_put_config_request_lower_half(E,H,I)
	async def handle_put_config_request_lower_half(D,data_path,query_dict,request_body):
		G=request_body;F=data_path;E=query_dict
		async with D.fifolock(Write):
			try:await D.val.handle_put_config_request(F,E,G)
			except val.InvalidDataPath as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_F,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.ParentNodeNotFound as B:A=web.Response(status=404);C=utils.gen_rc_errors(_D,_H,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.UnrecognizedInputNode as B:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_H,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except (val.NonexistentSchemaNode,val.ValidationFailed)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_F,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except (val.InvalidInputDocument,val.UnrecognizedQueryParameter)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_F,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.MissingQueryParameter as B:A=web.Response(status=400);C=utils.gen_rc_errors(_D,_k,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except val.NodeAlreadyExists as B:A=web.Response(status=409);C=utils.gen_rc_errors(_E,_l,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except NotImplementedError as B:A=web.Response(status=501);C=utils.gen_rc_errors(_E,_Q,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			if os.environ.get(_V)and _G in E:await asyncio.sleep(int(E[_G]))
			try:H=await D.dal.handle_put_config_request(F,E,G,D.create_callbacks,D.change_callbacks,D.delete_callbacks,D)
			except (dal.CreateCallbackFailed,dal.CreateOrChangeCallbackFailed,dal.ChangeCallbackFailed)as B:A=web.Response(status=400);C=utils.gen_rc_errors(_E,_m,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except (PluginNotFound,PluginSyntaxError,FunctionNotFound,FunctionNotCallable)as B:A=web.Response(status=501);C=utils.gen_rc_errors(_E,_Q,error_message=str(B));A.text=json.dumps(C,indent=2);return A
			except Exception as B:raise Exception("why wasn't this assertion caught by val? (assuming it's a YANG validation thing)"+str(B))
			D.val.inst=D.val.inst2;D.val.inst2=_B;await D.shared_post_commit_logic()
			if H==_P:return web.Response(status=201)
			else:return web.Response(status=204)
	async def handle_delete_config_request(A,request):
		C=request;D,G=utils.parse_raw_path(C._message.path[A.len_prefix_running:]);assert G=={};E=await A._check_auth(C,D)
		if E.status==401:return E
		B,J=utils.check_http_headers(C,A.supported_media_types,accept_required=_R)
		if type(B)is web.Response:H=B;return H
		else:
			assert type(B)==str;F=B
			if F==_J:I=_B
			else:I=utils.Encoding[F.rsplit(_K,1)[1]]
		return await A.handle_delete_config_request_lower_half(D)
	async def handle_delete_config_request_lower_half(A,data_path):
		E=data_path
		async with A.fifolock(Write):
			try:await A.val.handle_delete_config_request(E)
			except val.NonexistentSchemaNode as C:B=web.Response(status=400);D=utils.gen_rc_errors(_E,_F,error_message=str(C));B.text=json.dumps(D,indent=2);return B
			except val.NodeNotFound as C:B=web.Response(status=404);D=utils.gen_rc_errors(_D,_H,error_message=str(C));B.text=json.dumps(D,indent=2);return B
			except val.ValidationFailed as C:B=web.Response(status=400);D=utils.gen_rc_errors(_E,_F,error_message=str(C));B.text=json.dumps(D,indent=2);return B
			try:await A.dal.handle_delete_config_request(E,A.delete_callbacks,A.change_callbacks,A)
			except Exception as C:raise Exception(_n+str(C))
			A.val.inst=A.val.inst2;A.val.inst2=_B;await A.shared_post_commit_logic();return web.Response(status=204)
	async def shared_post_commit_logic(A):0
	async def handle_action_request(A,request):0
	async def handle_rpc_request(A,request):raise NotImplementedError('Native needs an RPC handler?  - client accessible!')
	def _handle_generate_symmetric_key_action(A,data_path,action_input):raise NotImplementedError(_W)
	def _handle_generate_asymmetric_key_action(A,data_path,action_input):raise NotImplementedError(_W)
	def _handle_resend_activation_email_action(A,data_path,action_input):raise NotImplementedError(_W)
	def _handle_generate_certificate_signing_request_action(A,data_path,action_input):raise NotImplementedError(_W)
async def _handle_tenant_created(watched_node_path,jsob,jsob_data_path,obj):jsob['tenant']['audit-log']={'log-entry':[]}
async def _handle_transport_changed(watched_node_path,jsob,jsob_data_path,obj):os.kill(os.getpid(),signal.SIGHUP)
async def _handle_transport_delete(watched_node_path,opaque):raise NotImplementedError('Deleting the /transport node itself cannot be constrained by YANG.')
async def _handle_plugin_created(watched_node_path,jsob,jsob_data_path,opaque):
	B=opaque;A=jsob[_U][_N];C=_o+A
	if A in B.plugins:E=sys.modules[C];del sys.modules[C];del E;del B.plugins[A]
	try:F=importlib.import_module(C)
	except ModuleNotFoundError as D:raise PluginNotFound(str(D))
	except SyntaxError as D:raise PluginSyntaxError('SyntaxError: '+str(D))
	B.plugins[A]={_p:F,_O:{}}
async def _handle_plugin_deleted(watched_node_path,opaque):C=opaque;A=re.sub(_c,_d,watched_node_path);B=_o+A;D=sys.modules[B];del sys.modules[B];del D;del C.plugins[A]
async def _handle_function_created(watched_node_path,jsob,jsob_data_path,opaque):
	B=opaque;C=re.sub(_c,_d,jsob_data_path);A=jsob[_b][_N]
	try:D=getattr(B.plugins[C][_p],A)
	except AttributeError as E:raise FunctionNotFound(str(E))
	if not callable(D):raise FunctionNotCallable("The plugin function name '"+A+"' is not callable.")
	B.plugins[C][_O][A]=D
async def _handle_function_deleted(watched_node_path,opaque):A=watched_node_path;B=opaque;C=re.sub(_c,_d,A);D=A.rsplit('=',1)[1];del B.plugins[C][_O][D]
async def _handle_admin_passwd_created(watched_node_path,jsob,jsob_data_path,obj):
	A=jsob
	def B(item):
		A=item;A[_q]=datetime.datetime.utcnow().strftime(_r)
		if _I in A and A[_I].startswith(_s):A[_I]=sha256_crypt.using(rounds=1000).hash(A[_I][3:])
	if type(A)==dict:B(A[_t])
	else:
		assert _R;assert type(A)==list
		for C in A:assert type(C)==dict;B(C)
async def _handle_admin_passwd_changed(watched_node_path,json,jsob_data_path,obj):
	def A(item):
		A=item;A[_q]=datetime.datetime.utcnow().strftime(_r)
		if _I in A and A[_I].startswith(_s):A[_I]=sha256_crypt.using(rounds=1000).hash(A[_I][3:])
		else:0
	assert json!=_B;assert jsob_data_path!=_B;A(json[_t])
async def _handle_ref_stat_parent_created(watched_node_path,jsob,jsob_data_path,obj):
	A=jsob;assert watched_node_path==jsob_data_path
	def B(item):item['reference-statistics']={'reference-count':0,'last-referenced':'never'}
	if type(A)==dict:D=next(iter(A));B(A[D])
	else:
		raise NotImplementedError('dead code?');assert type(A)==list
		for C in A:assert type(C)==dict;B(C)
def _handle_ref_stats_changed(leafrefed_node_data_path,obj):raise NotImplementedError('_handle_ref_stats_changed tested?')
def _handle_lingering_unreferenced_node_change(watched_node_path,obj):raise NotImplementedError(_u)
def _handle_expiring_certificate_change(watched_node_path,obj):raise NotImplementedError(_u)
async def _handle_asymmetric_public_key_created_or_changed(watched_node_path,jsob,jsob_data_path,obj):
	B=watched_node_path;A=jsob;I=A[_C][_e];E=base64.b64decode(I)
	if A[_C][_X]!=_v:raise dal.CreateOrChangeCallbackFailed(_w+A[_C][_X]+_Y+B.rsplit(_A,1)[0])
	try:O,J=decode_der(E,asn1Spec=rfc5280.SubjectPublicKeyInfo())
	except PyAsn1Error as D:raise dal.CreateOrChangeCallbackFailed(_x+B.rsplit(_A,1)[0]+_S+str(D)+_T)
	K=serialization.load_der_public_key(E);L=A[_C][_y];F=base64.b64decode(L)
	if A[_C][_Z]==_z:
		try:P,J=decode_der(F,asn1Spec=rfc5915.ECPrivateKey())
		except PyAsn1Error as D:raise dal.CreateOrChangeCallbackFailed('Parsing private key structure failed for '+B.rsplit(_A,1)[0]+_S+str(D)+_T)
	else:raise dal.CreateOrChangeCallbackFailed(_A0+A[_C][_Z]+_Y+B.rsplit(_A,1)[0])
	M=serialization.load_der_private_key(F,_B,_B);G=_A1;N=M.sign(G,ec.ECDSA(hashes.SHA256()))
	try:K.verify(N,G,ec.ECDSA(hashes.SHA256()))
	except InvalidSignature as D:raise dal.CreateOrChangeCallbackFailed(_A2+B.rsplit(_A,1)[0])
	if _L in A[_C]:
		if _M in A[_C][_L]:
			C=obj
			if C.dal.post_dal_callbacks is _B:C.dal.post_dal_callbacks=[]
			H=_handle_verify_asymmetric_key_and_certs_post_sweep,B.rsplit(_A,1)[0],C
			if H not in C.dal.post_dal_callbacks:C.dal.post_dal_callbacks.append(H)
async def _handle_asymmetric_private_key_created_or_changed(watched_node_path,jsob,jsob_data_path,obj):
	B=watched_node_path;A=jsob;I=A[_C][_y];E=base64.b64decode(I)
	if A[_C][_Z]==_z:O,J=decode_der(E,asn1Spec=rfc5915.ECPrivateKey())
	else:raise dal.CreateOrChangeCallbackFailed(_A0+A[_C][_Z]+_Y+B.rsplit(_A,1)[0]+_S+str(D)+_T)
	K=serialization.load_der_private_key(E,_B,_B);L=A[_C][_e];F=base64.b64decode(L)
	if A[_C][_X]!=_v:raise dal.CreateOrChangeCallbackFailed(_w+A[_C][_X]+_Y+B.rsplit(_A,1)[0])
	try:P,J=decode_der(F,asn1Spec=rfc5280.SubjectPublicKeyInfo())
	except PyAsn1Error as D:raise dal.CreateOrChangeCallbackFailed(_x+B.rsplit(_A,1)[0]+_S+str(D)+_T)
	M=serialization.load_der_public_key(F);G=_A1;N=K.sign(G,ec.ECDSA(hashes.SHA256()))
	try:M.verify(N,G,ec.ECDSA(hashes.SHA256()))
	except InvalidSignature as D:raise dal.CreateOrChangeCallbackFailed(_A2+B.rsplit(_A,1)[0])
	if _L in A[_C]:
		if _M in A[_C][_L]:
			C=obj
			if C.dal.post_dal_callbacks is _B:C.dal.post_dal_callbacks=[]
			H=_handle_verify_asymmetric_key_and_certs_post_sweep,B.rsplit(_A,1)[0],C
			if H not in C.dal.post_dal_callbacks:C.dal.post_dal_callbacks.append(H)
async def _handle_asymmetric_key_cert_created_or_changed(watched_node_path,jsob,jsob_data_path,obj):
	B=watched_node_path;I=jsob[_M][_f];J=base64.b64decode(I);K,O=decode_der(J,asn1Spec=rfc5652.ContentInfo());L=utils.degenerate_cms_obj_to_ders(K);A=[]
	for M in L:N=x509.load_der_x509_certificate(M);A.append(N)
	E=[B for B in A if B.extensions.get_extension_for_oid(ExtensionOID.BASIC_CONSTRAINTS).value.ca==_R]
	if len(E)==0:raise dal.CreateOrChangeCallbackFailed('End entity certificates must encode a certificate having "basic" constraint "ca" with value "False": '+B.rsplit(_A,1)[0])
	if len(E)>1:raise dal.CreateOrChangeCallbackFailed('End entity certificates must encode no more than one certificate having "basic" constraint "ca" with value "False" ('+str(len(E))+_A3+B.rsplit(_A,1)[0])
	G=E[0];A.remove(G);C=G
	while len(A):
		F=[B for B in A if B.subject==C.issuer]
		if len(F)==0:raise dal.CreateOrChangeCallbackFailed('End entity certificates must not encode superfluous certificates.  Found certificates unconnected to chain from the "leaf" certificate while looking for "'+str(C.subject)+_g+B.rsplit(_A,1)[0])
		if len(F)>1:raise dal.CreateOrChangeCallbackFailed('End entity certificates must not encode superfluous certificates.  CMS encodes multiple certificates having the same "subject" value ('+str(C.issuer)+'): '+B.rsplit(_A,1)[0])
		C=F[0];A.remove(C)
	D=obj
	if D.dal.post_dal_callbacks is _B:D.dal.post_dal_callbacks=[]
	H=_handle_verify_asymmetric_key_and_certs_post_sweep,B.rsplit(_A,3)[0],D
	if H not in D.dal.post_dal_callbacks:D.dal.post_dal_callbacks.append(H)
async def _handle_verify_asymmetric_key_and_certs_post_sweep(watched_node_path,conn,opaque):
	U='row_id';B=conn;A=watched_node_path;C=opaque;E=C.dal._get_row_data_for_list_path(A,B);F=re.sub('=[^/]*','',A);D=C.dal._get_jsob_for_row_id_in_table(F,E[U],B);I=D[_C][_e];J=base64.b64decode(I);K=serialization.load_der_public_key(J)
	if _L in D[_C]:
		if _M in D[_C][_L]:
			L=F+'/certificates/certificate';M=C.dal._find_rows_in_table_having_pid(L,E[U],{},B);G=M.fetchall();assert len(G)!=0
			for H in G:
				N=H['jsob'][_M][_f];O=base64.b64decode(N);P,V=decode_der(O,asn1Spec=rfc5652.ContentInfo());Q=utils.degenerate_cms_obj_to_ders(P)
				for R in Q:
					S=x509.load_der_x509_certificate(R);T=K.public_numbers()
					if S.public_key().public_numbers()==T:break
				else:raise dal.CreateOrChangeCallbackFailed('End entity certificates must encode a "leaf" certificate having a public key matching the asymmetric key\'s public key: '+A+'/certificates/certificate='+H[_N])
async def _handle_trust_anchor_cert_created_or_changed(watched_node_path,jsob,jsob_data_path,obj):
	B=watched_node_path;G=jsob[_M][_f];H=base64.b64decode(G)
	try:I,N=decode_der(H,asn1Spec=rfc5652.ContentInfo())
	except PyAsn1Error as J:raise dal.CreateOrChangeCallbackFailed('Parsing trust anchor certificate CMS structure failed for '+B.rsplit(_A,1)[0]+_S+str(J)+_T)
	K=utils.degenerate_cms_obj_to_ders(I);A=[]
	for L in K:M=x509.load_der_x509_certificate(L);A.append(M)
	D=[B for B in A if B.subject==B.issuer]
	if len(D)==0:raise dal.CreateOrChangeCallbackFailed('Trust anchor certificates must encode a root (self-signed) certificate: '+B.rsplit(_A,1)[0])
	if len(D)>1:raise dal.CreateOrChangeCallbackFailed('Trust anchor certificates must encode no more than one root (self-signed) certificate ('+str(len(D))+_A3+B.rsplit(_A,1)[0])
	F=D[0];A.remove(F);C=F
	while len(A):
		E=[B for B in A if B.issuer==C.subject]
		if len(E)==0:raise dal.CreateOrChangeCallbackFailed('Trust anchor certificates must not encode superfluous certificates.  Discovered additional certificates while looking for the issuer of "'+str(C.subject)+_g+B.rsplit(_A,1)[0])
		if len(E)>1:raise dal.CreateOrChangeCallbackFailed('Trust anchor certificates must encode a single chain of certificates.  Found '+str(len(E))+' certificates issued by "'+str(C.subject)+_g+B.rsplit(_A,1)[0])
		C=E[0];A.remove(C)
async def _check_expirations(nvh):0