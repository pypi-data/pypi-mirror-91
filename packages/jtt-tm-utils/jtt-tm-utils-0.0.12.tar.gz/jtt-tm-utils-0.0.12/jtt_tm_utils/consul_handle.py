from consul import Consul

import sys

import collections

from .log import logger

CService =collections.namedtuple('CService','ip port agent_ip')
CRedisService = collections.namedtuple('CRedisService','ip port db')
CDatabaseService = collections.namedtuple('CDatabaseService','dbdriver ip port dbname user pwd')
# CMongoService = collections.namedtuple('CMongoService','host port username password authSource')
def cservice_to_address(service):
    return '%s:%s' % (service.ip,service.port)

class ConsulAgent:
    def __init__(self,node_name,ip,services=None):
        self.node_name = node_name
        self.ip = ip
        self._services = services

    def combine_address(self,port):
        return '%s:%s' %(self.ip,port)

    def combine_service_id(self,name,port):
        return '%s:%s:%s' %(self.node_name,name,port)

class ConsulReader():
    def __init__(self):
        self._consul =None
        self._agent =None

    @property
    def consul(self):
        if self._consul is None:
            self._consul =Consul()
        return self._consul

    @property
    def agent(self):
        if self._agent is None:
            try:
                agent_self = self.consul.agent.self()
                self._agent = ConsulAgent(agent_self['Member'].get('Name'),
                                          agent_self['Member'].get('Addr'),
                                          self.consul.catalog.services()[1])

            except Exception as e:
                logger.error('读取consul 服务失败,error:%s' % (e))

                sys.exit(-1)

        return self._agent

    def read_key(self,key,raise_error=False):
        v =self.consul.kv.get(key)[1]
        if v is None:
            if raise_error:
                raise Exception('consul: not has key %s' % key)
            else:
                sys.exit('consul: not has key %s' % key)
        return v['Value'].decode()

    def read_services(self,service_name,tag,raise_error=False,key =None,**args):
        try:
            srvs = self.consul.catalog.service(service_name, tag=tag,**args)[1]

            if key is not None:
                port = self.read_key('%s_%s_%s' %(service_name,tag,key),raise_error=raise_error)
            else:
                port =None
            re =[]
            for srv in srvs or []:
                re.append(CService(ip=srv['ServiceAddress'],
                         port=port or srv['ServicePort'],
                         agent_ip=srv['Address']))
            return re
        except Exception as e:
            logger.error('consul:%s,%s error:%s' % (service_name,tag,str(e)))
            self._consul =None
            if raise_error:
                raise Exception('consul:%s,%s, error:%s' % (service_name,tag,str(e)))
            else:
                sys.exit('consul:%s,%s, error:%s' % (service_name,tag,str(e)))

    def read_service(self,service_name,tag,raise_error=False,key =None,**args):
        srvs = self.read_services(service_name,tag,raise_error,key,**args)
        if len(srvs) <= 0:
            logger.error('consul:%s,%s error:config is not exists' % (service_name,tag))
            if raise_error:
                raise Exception('consul:%s,%s error:config is not exists' % (service_name,tag))
            else:
                sys.exit('consul:%s,%s error:config is not exists' % (service_name,tag))
        return srvs[0]

    def read_service_as_address(self,service_name,tag,raise_error=False,key =None,**args):
        srv = self.read_service(service_name,tag,raise_error,key,**args)
        return cservice_to_address(srv)

    def read_redis(self,tag,as_slave=False):
        try:
            if as_slave:
                agent_self = self.consul.agent.self()
                member = agent_self['Member']
                node_name = member.get('NodeName')
                srv = self.read_service('redis', tag, raise_error=True, near=node_name)
            else:
                srv = self.read_service('redis',tag,raise_error=True)

            try:
                db = self.read_key('redis_%s_db' % tag)
            except:
                db =0

            return CRedisService(srv.ip,srv.port,db)

        except Exception as e:
            logger.error('consul:redis error:%s' % str(e))
            sys.exit('consul:redis error:%s' % str(e))

    def redis_as_url(self,tag,**args):
        credis = self.read_redis(tag,**args)
        return 'redis://%s:%s/%s' % (credis.ip,credis.port,credis.db)

    def service_as_url(self,service_name,tag,raise_error=False,key =None,protocol ='http',**args):
        service = self.read_service(service_name,tag,raise_error,key,**args)
        return '%s://%s' % (protocol,cservice_to_address(service))

    def kafka_servers(self,tag=None):
        srvs =self.read_services('kafka',tag=tag)
        if len(srvs)<=0:
            logger.error('consul not set kafka')
            sys.exit('consul not set kafka')
        addresses = [cservice_to_address(srv) for srv in srvs]
        return ','.join(addresses)

    def read_database(self,dbname):
        dbsrv =self.read_service('database',dbname)
        driver_key = self.read_key('%s_dbdriver' % dbname)
        return CDatabaseService('mssql+pymssql' if driver_key=='mssql' else 'mysql+mysqldb',
                                dbsrv.ip,
                                dbsrv.port,
                                self.read_key('%s_db_name'% dbname),
                                self.read_key('%s_login_user' % dbname),
                                self.read_key('%s_login_pw' % dbname))

    def database_as_url(self,dbname):
        dbsrv = self.read_database(dbname)
        return "{dbdriver}://{us}:{pw}@{host}:{port}/{name}".format(
                 dbdriver =dbsrv.dbdriver,us=dbsrv.user,pw=dbsrv.pwd,
                 host=dbsrv.ip,port=dbsrv.port,name=dbsrv.dbname)

    def database_as_json(self,dbname):
        dbsrv = self.read_database(dbname)
        return {'host':dbsrv.ip,
                       'port':dbsrv.port,
                       'db':dbsrv.dbname,
                       'user':dbsrv.user,
                       'password':dbsrv.pwd}

    def read_mongo(self,dbname):
        dbsrv = self.read_service('mongo', dbname)
        return {'host':dbsrv.ip,
                'port':dbsrv.port,
                'username':self.read_key('mongo_%s_user' % dbname),
                'password':self.read_key('mongo_%s_pw' % dbname),
                'authSource': dbname}

    def mongo_as_url(self,dbname):
        dbconfig = self.read_mongo(dbname)
        return 'mongodb://{username}:{password}@{host}:{port}/{authSource}'.format(**dbconfig)

    def register_service(self,name,port,host=None,tags =None,check=None,token=None):
        if host is None:
            host = self.agent.ip
        try:

            self.consul.agent.service.register(name, service_id=self.agent.combine_service_id( name, port ), address=host,
                                        port=port, tags=tags, check=check, token=token)
            logger.info('註冊%s到consul成功！' % name)
        except Exception as e:
            logger.error('注册 %s服务失败,error:%s' % (name, e))

            sys.exit('注册 %s服务失败,error:%s' % (name, e))

    def deregister_service(self,name,port):
        try:
            service_id=self.agent.combine_service_id( name, port )
            self.consul.agent.service.deregister(service_id)

            logger.info('删除(%s)成功！' % name)
        except Exception as e:
            logger.error('删除 %s服务失败,error:%s' % (name, e))

            sys.exit('删除 %s服务失败,error:%s' % (name, e))

consul_reader = ConsulReader()


