from localstack.utils.aws import aws_models
sCWNj=super
sCWNI=None
sCWNV=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  sCWNj(LambdaLayer,self).__init__(arn)
  self.cwd=sCWNI
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.sCWNV.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,sCWNV,env=sCWNI):
  sCWNj(RDSDatabase,self).__init__(sCWNV,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,sCWNV,env=sCWNI):
  sCWNj(RDSCluster,self).__init__(sCWNV,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,sCWNV,env=sCWNI):
  sCWNj(AppSyncAPI,self).__init__(sCWNV,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,sCWNV,env=sCWNI):
  sCWNj(AmplifyApp,self).__init__(sCWNV,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,sCWNV,env=sCWNI):
  sCWNj(ElastiCacheCluster,self).__init__(sCWNV,env=env)
class TransferServer(BaseComponent):
 def __init__(self,sCWNV,env=sCWNI):
  sCWNj(TransferServer,self).__init__(sCWNV,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,sCWNV,env=sCWNI):
  sCWNj(CloudFrontDistribution,self).__init__(sCWNV,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,sCWNV,env=sCWNI):
  sCWNj(CodeCommitRepository,self).__init__(sCWNV,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
