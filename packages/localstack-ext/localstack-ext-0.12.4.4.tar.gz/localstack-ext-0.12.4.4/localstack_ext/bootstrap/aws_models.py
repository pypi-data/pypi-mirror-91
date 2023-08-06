from localstack.utils.aws import aws_models
JrDdq=super
JrDdM=None
JrDdK=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  JrDdq(LambdaLayer,self).__init__(arn)
  self.cwd=JrDdM
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.JrDdK.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,JrDdK,env=JrDdM):
  JrDdq(RDSDatabase,self).__init__(JrDdK,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,JrDdK,env=JrDdM):
  JrDdq(RDSCluster,self).__init__(JrDdK,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,JrDdK,env=JrDdM):
  JrDdq(AppSyncAPI,self).__init__(JrDdK,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,JrDdK,env=JrDdM):
  JrDdq(AmplifyApp,self).__init__(JrDdK,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,JrDdK,env=JrDdM):
  JrDdq(ElastiCacheCluster,self).__init__(JrDdK,env=env)
class TransferServer(BaseComponent):
 def __init__(self,JrDdK,env=JrDdM):
  JrDdq(TransferServer,self).__init__(JrDdK,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,JrDdK,env=JrDdM):
  JrDdq(CloudFrontDistribution,self).__init__(JrDdK,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,JrDdK,env=JrDdM):
  JrDdq(CodeCommitRepository,self).__init__(JrDdK,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
