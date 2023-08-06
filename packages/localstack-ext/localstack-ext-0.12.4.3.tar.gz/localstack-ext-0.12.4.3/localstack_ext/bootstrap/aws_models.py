from localstack.utils.aws import aws_models
zLPAF=super
zLPAu=None
zLPAg=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  zLPAF(LambdaLayer,self).__init__(arn)
  self.cwd=zLPAu
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.zLPAg.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,zLPAg,env=zLPAu):
  zLPAF(RDSDatabase,self).__init__(zLPAg,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,zLPAg,env=zLPAu):
  zLPAF(RDSCluster,self).__init__(zLPAg,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,zLPAg,env=zLPAu):
  zLPAF(AppSyncAPI,self).__init__(zLPAg,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,zLPAg,env=zLPAu):
  zLPAF(AmplifyApp,self).__init__(zLPAg,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,zLPAg,env=zLPAu):
  zLPAF(ElastiCacheCluster,self).__init__(zLPAg,env=env)
class TransferServer(BaseComponent):
 def __init__(self,zLPAg,env=zLPAu):
  zLPAF(TransferServer,self).__init__(zLPAg,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,zLPAg,env=zLPAu):
  zLPAF(CloudFrontDistribution,self).__init__(zLPAg,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,zLPAg,env=zLPAu):
  zLPAF(CodeCommitRepository,self).__init__(zLPAg,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
