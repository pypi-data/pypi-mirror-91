# Copyright (c) 2021 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_C='/ds/ietf-datastores:operational'
_B='/ds/ietf-datastores:running'
_A=None
import os,ssl,json,base64,pyasn1,asyncio,yangson,datetime,tempfile,basicauth
from .  import utils
from aiohttp import web
from .handler import RouteHandler
from pyasn1_modules import rfc5652
from pyasn1_modules import rfc5915
from pyasn1.codec.der.decoder import decode as der_decoder
from pyasn1.codec.der.encoder import encode as der_encoder
async def set_server_header(request,response):response.headers['Server']='<redacted>'
class RestconfServer:
	root='/restconf';prefix_running=root+_B;prefix_operational=root+_C;prefix_operations=root+'/operations';len_prefix_running=len(prefix_running);len_prefix_operational=len(prefix_operational);len_prefix_operations=len(prefix_operations)
	def __init__(A,loop,dal,endpoint_config,view_handler,facade_yl=_A):
		A3='client-certs';A2='local-truststore-reference';A1='ca-certs';A0='client-authentication';z='cert-data';y='ASCII';x=':keystore/asymmetric-keys/asymmetric-key=';w='reference';v='server-identity';u='local-port';t='http';Y='tcp-server-parameters';O='certificate';N='tls-server-parameters';M='/ds/ietf-datastores:running{tail:.*}';L='/';G=dal;E='https';C=endpoint_config;B=view_handler;A.len_prefix_running=len(A.root+_B);A.len_prefix_operational=len(A.root+_C);A.loop=loop;A.dal=G;A.name=C['name'];A.view_handler=B;A.app=web.Application();A.app.on_response_prepare.append(set_server_header);A.app.router.add_get('/.well-known/host-meta',A.handle_get_host_meta);A.app.router.add_get(A.root,B.handle_get_restconf_root);A.app.router.add_get(A.root+L,B.handle_get_restconf_root);A.app.router.add_get(A.root+'/yang-library-version',B.handle_get_yang_library_version);A.app.router.add_get(A.root+'/ds/ietf-datastores:operational{tail:.*}',B.handle_get_opstate_request);A.app.router.add_get(A.root+M,B.handle_get_config_request);A.app.router.add_put(A.root+M,B.handle_put_config_request);A.app.router.add_post(A.root+M,B.handle_post_config_request);A.app.router.add_delete(A.root+M,B.handle_delete_config_request);A.app.router.add_post(A.root+'/ds/ietf-datastores:operational/{tail:.*}',B.handle_action_request);A.app.router.add_post(A.root+'/operations/{tail:.*}',B.handle_rpc_request)
		if t in C:F=t
		else:assert E in C;F=E
		A.local_address=C[F][Y]['local-address'];A.local_port=os.environ.get('SZTPD_DEFAULT_PORT',8080)
		if u in C[F][Y]:A.local_port=C[F][Y][u]
		D=_A
		if F==E:
			P=C[E][N][v][O][w]['asymmetric-key'];I=A.dal.handle_get_config_request(L+A.dal.app_ns+x+P);Z=A.loop.run_until_complete(I);Q=Z[A.dal.app_ns+':asymmetric-key'][0]['cleartext-private-key'];a=base64.b64decode(Q);b,A4=der_decoder(a,asn1Spec=rfc5915.ECPrivateKey());c=der_encoder(b);R=base64.b64encode(c).decode(y);assert Q==R;d='-----BEGIN EC PRIVATE KEY-----\n'+R+'\n-----END EC PRIVATE KEY-----\n';e=C[E][N][v][O][w][O];I=A.dal.handle_get_config_request(L+A.dal.app_ns+x+P+'/certificates/certificate='+e);f=A.loop.run_until_complete(I);g=f[A.dal.app_ns+':certificate'][0][z];h=base64.b64decode(g);i,j=der_decoder(h,asn1Spec=rfc5652.ContentInfo());k=i.getComponentByName('content');l,j=der_decoder(k,asn1Spec=rfc5652.SignedData());S=l.getComponentByName('certificates');T=''
			for m in range(len(S)):n=S[m][0];o=der_encoder(n);p=base64.b64encode(o).decode(y);T+='-----BEGIN CERTIFICATE-----\n'+p+'\n-----END CERTIFICATE-----\n'
			D=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH);D.verify_mode=ssl.CERT_OPTIONAL
			with tempfile.TemporaryDirectory()as U:
				V=U+'key.pem';W=U+'certs.pem'
				with open(V,'w')as q:q.write(d)
				with open(W,'w')as r:r.write(T)
				D.load_cert_chain(W,V)
			if A0 in C[E][N]:
				H=C[E][N][A0]
				def X(truststore_ref):
					C=G.handle_get_config_request(L+G.app_ns+':truststore/certificate-bags/certificate-bag='+truststore_ref);D=A.loop.run_until_complete(C);B=[]
					for E in D[G.app_ns+':certificate-bag'][0][O]:F=base64.b64decode(E[z]);H,I=der_decoder(F,asn1Spec=rfc5652.ContentInfo());assert not I;B+=utils.degenerate_cms_obj_to_ders(H)
					return B
				J=[]
				if A1 in H:K=H[A1][A2];J+=X(K)
				if A3 in H:K=H[A3][A2];J+=X(K)
				s=utils.der_dict_to_multipart_pem({'CERTIFICATE':J});D.load_verify_locations(cadata=s)
		if F==E:assert not D is _A
		else:assert D is _A
		A.runner=web.AppRunner(A.app);A.loop.run_until_complete(A.runner.setup());A.site=web.TCPSite(A.runner,host=A.local_address,port=A.local_port,ssl_context=D,reuse_port=True);A.loop.run_until_complete(A.site.start())
	async def handle_get_host_meta(B,request):A=web.Response();A.content_type='application/xrd+xml';A.text='<XRD xmlns="http://docs.oasis-open.org/ns/xri/xrd-1.0">\n  <Link rel="restconf" href="/restconf"/>\n</XRD>';return A