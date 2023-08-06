from localstack.utils.aws import aws_models
CATBV=super
CATBQ=None
CATBd=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  CATBV(LambdaLayer,self).__init__(arn)
  self.cwd=CATBQ
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.CATBd.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,CATBd,env=CATBQ):
  CATBV(RDSDatabase,self).__init__(CATBd,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,CATBd,env=CATBQ):
  CATBV(RDSCluster,self).__init__(CATBd,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,CATBd,env=CATBQ):
  CATBV(AppSyncAPI,self).__init__(CATBd,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,CATBd,env=CATBQ):
  CATBV(AmplifyApp,self).__init__(CATBd,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,CATBd,env=CATBQ):
  CATBV(ElastiCacheCluster,self).__init__(CATBd,env=env)
class TransferServer(BaseComponent):
 def __init__(self,CATBd,env=CATBQ):
  CATBV(TransferServer,self).__init__(CATBd,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,CATBd,env=CATBQ):
  CATBV(CloudFrontDistribution,self).__init__(CATBd,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,CATBd,env=CATBQ):
  CATBV(CodeCommitRepository,self).__init__(CATBd,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
