from localstack.utils.aws import aws_models
uXBKN=super
uXBKc=None
uXBKE=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  uXBKN(LambdaLayer,self).__init__(arn)
  self.cwd=uXBKc
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.uXBKE.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,uXBKE,env=uXBKc):
  uXBKN(RDSDatabase,self).__init__(uXBKE,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,uXBKE,env=uXBKc):
  uXBKN(RDSCluster,self).__init__(uXBKE,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,uXBKE,env=uXBKc):
  uXBKN(AppSyncAPI,self).__init__(uXBKE,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,uXBKE,env=uXBKc):
  uXBKN(AmplifyApp,self).__init__(uXBKE,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,uXBKE,env=uXBKc):
  uXBKN(ElastiCacheCluster,self).__init__(uXBKE,env=env)
class TransferServer(BaseComponent):
 def __init__(self,uXBKE,env=uXBKc):
  uXBKN(TransferServer,self).__init__(uXBKE,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,uXBKE,env=uXBKc):
  uXBKN(CloudFrontDistribution,self).__init__(uXBKE,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,uXBKE,env=uXBKc):
  uXBKN(CodeCommitRepository,self).__init__(uXBKE,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
