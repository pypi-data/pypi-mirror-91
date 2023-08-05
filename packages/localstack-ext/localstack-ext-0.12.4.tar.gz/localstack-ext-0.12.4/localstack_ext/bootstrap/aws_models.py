from localstack.utils.aws import aws_models
TwfEg=super
TwfEb=None
TwfEU=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  TwfEg(LambdaLayer,self).__init__(arn)
  self.cwd=TwfEb
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.TwfEU.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,TwfEU,env=TwfEb):
  TwfEg(RDSDatabase,self).__init__(TwfEU,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,TwfEU,env=TwfEb):
  TwfEg(RDSCluster,self).__init__(TwfEU,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,TwfEU,env=TwfEb):
  TwfEg(AppSyncAPI,self).__init__(TwfEU,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,TwfEU,env=TwfEb):
  TwfEg(AmplifyApp,self).__init__(TwfEU,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,TwfEU,env=TwfEb):
  TwfEg(ElastiCacheCluster,self).__init__(TwfEU,env=env)
class TransferServer(BaseComponent):
 def __init__(self,TwfEU,env=TwfEb):
  TwfEg(TransferServer,self).__init__(TwfEU,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,TwfEU,env=TwfEb):
  TwfEg(CloudFrontDistribution,self).__init__(TwfEU,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,TwfEU,env=TwfEb):
  TwfEg(CodeCommitRepository,self).__init__(TwfEU,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
