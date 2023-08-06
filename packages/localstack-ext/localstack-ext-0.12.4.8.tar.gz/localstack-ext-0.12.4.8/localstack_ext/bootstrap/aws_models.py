from localstack.utils.aws import aws_models
OXUYJ=super
OXUYH=None
OXUYK=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  OXUYJ(LambdaLayer,self).__init__(arn)
  self.cwd=OXUYH
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.OXUYK.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,OXUYK,env=OXUYH):
  OXUYJ(RDSDatabase,self).__init__(OXUYK,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,OXUYK,env=OXUYH):
  OXUYJ(RDSCluster,self).__init__(OXUYK,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,OXUYK,env=OXUYH):
  OXUYJ(AppSyncAPI,self).__init__(OXUYK,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,OXUYK,env=OXUYH):
  OXUYJ(AmplifyApp,self).__init__(OXUYK,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,OXUYK,env=OXUYH):
  OXUYJ(ElastiCacheCluster,self).__init__(OXUYK,env=env)
class TransferServer(BaseComponent):
 def __init__(self,OXUYK,env=OXUYH):
  OXUYJ(TransferServer,self).__init__(OXUYK,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,OXUYK,env=OXUYH):
  OXUYJ(CloudFrontDistribution,self).__init__(OXUYK,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,OXUYK,env=OXUYH):
  OXUYJ(CodeCommitRepository,self).__init__(OXUYK,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
