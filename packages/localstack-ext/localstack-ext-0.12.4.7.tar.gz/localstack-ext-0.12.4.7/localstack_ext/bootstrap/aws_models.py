from localstack.utils.aws import aws_models
URFqf=super
URFqn=None
URFqa=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  URFqf(LambdaLayer,self).__init__(arn)
  self.cwd=URFqn
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.URFqa.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,URFqa,env=URFqn):
  URFqf(RDSDatabase,self).__init__(URFqa,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,URFqa,env=URFqn):
  URFqf(RDSCluster,self).__init__(URFqa,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,URFqa,env=URFqn):
  URFqf(AppSyncAPI,self).__init__(URFqa,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,URFqa,env=URFqn):
  URFqf(AmplifyApp,self).__init__(URFqa,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,URFqa,env=URFqn):
  URFqf(ElastiCacheCluster,self).__init__(URFqa,env=env)
class TransferServer(BaseComponent):
 def __init__(self,URFqa,env=URFqn):
  URFqf(TransferServer,self).__init__(URFqa,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,URFqa,env=URFqn):
  URFqf(CloudFrontDistribution,self).__init__(URFqa,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,URFqa,env=URFqn):
  URFqf(CodeCommitRepository,self).__init__(URFqa,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
