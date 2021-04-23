from django.test import TestCase
import threading
import time
# from kazoo.client import KazooClient
#
# # Create your tests here.
#
# def zk_register():
#     nodePaht = "/bocloud/services/lycmdb"
#     host = "10.10.47.150"
#     port = "2181"
#     zk_conn = KazooClient(host+":"+port,auth_data=[("digest","bocloud:bocloud")])
#     zk_conn.start()
#
#     if not zk_conn.exists(nodePaht):
#        childPath = zk_conn.create(nodePaht)
#
# zk_register()

abc = """
python3-more-itertools-7.2.0-1.aix6.1.noarch.rpm
python3-jaraco.functools-3.0.0-1.aix6.1.noarch.rpm
python3-six-1.13.0-1.aix6.1.noarch.rpm
python3-cheroot-8.2.1-1.aix6.1.noarch.rpm
python3-jaraco.classes-3.1.0-1.aix6.1.noarch.rpm
python3-pytz-2019.3-1.aix6.1.noarch.rpm
python3-tempora-2.1.0-1.aix6.1.noarch.rpm
python3-portend-2.6-1.aix6.1.noarch.rpm
python3-jaraco.text-3.2.0-1.aix6.1.noarch.rpm
python3-jaraco.collections-3.0.0-1.aix6.1.noarch.rpm
python3-zc.lockfile-2.0-1.aix6.1.noarch.rpm
python3-cherrypy-18.5.0-1.aix6.1.noarch.rpm
python3-markupsafe-1.1.1-1.aix6.1.ppc.rpm
python3-jinja2-2.10.3-1.aix6.1.noarch.rpm
python3-msgpack-0.6.2-1.aix6.1.ppc.rpm
libyaml-0.2.2-1.aix6.1.ppc.rpm
python3-pyyaml-5.3.1-1.aix6.1.ppc.rpm
zeromq-4.3.3-1.aix6.1.ppc.rpm
python3-pyzmq-18.1.1-1.aix6.1.ppc.rpm
python3-certifi-2019.9.11-1.aix6.1.noarch.rpm
python3-chardet-3.0.4-1.aix6.1.noarch.rpm
python3-idna-2.8-1.aix6.1.noarch.rpm
python3-urllib3-1.25.7-1.aix6.1.noarch.rpm
python3-requests-2.22.0-1.aix6.1.noarch.rpm
python3-tornado-4.5.3-1.aix6.1.ppc.rpm
python3-argparse-1.4.0-1.aix6.1.noarch.rpm
python3-linecache2-1.0.0-1.aix6.1.noarch.rpm
python3-traceback2-1.4.0-1.aix6.1.noarch.rpm
python3-unittest2-1.1.0-1.aix6.1.noarch.rpm
python-2.7.18-1.aix6.1.ppc.rpm
pysqlite-2.8.3-2.aix6.1.ppc.rpm
python-iniparse-0.4-1.aix6.1.noarch.rpm
p11-kit-0.23.16-1.aix6.1.ppc.rpm
p11-kit-devel-0.23.16-1.aix6.1.ppc.rpm
p11-kit-tools-0.23.16-1.aix6.1.ppc.rpm
ca-certificates-2020.06.01-1.aix6.1.ppc.rpm
db-6.2.38-3.aix6.1.ppc.rpm
krb5-libs-1.16.1-5.aix6.1.ppc.rpm
yum-metadata-parser-1.1.4-2.aix6.1.ppc.rpm
cyrus-sasl-2.1.27-3.aix6.1.ppc.rpm
openldap-2.4.54-1.aix6.1.ppc.rpm
libssh2-1.9.0-4.aix6.1.ppc.rpm
libcurl-7.73.0-2.aix6.1.ppc.rpm
zlib-1.2.11-5.aix6.1.ppc.rpm
python-pycurl-7.19.5-3.aix6.1.noarch.rpm
python-urlgrabber-3.10.1-1.aix6.1.noarch.rpm
yum-utils-1.1.31-2.aix6.1.noarch.rpm
python3-backports_abc-0.5-1.aix6.1.noarch.rpm
python3-singledispatch-3.4.0.3-1.aix6.1.noarch.rpm
salt-minion-2019.2.5-1.aix6.1.noarch.rpm
"""

print(abc.replace("\n"," "))