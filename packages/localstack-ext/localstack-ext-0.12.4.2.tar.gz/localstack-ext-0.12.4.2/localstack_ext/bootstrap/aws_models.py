from localstack.utils.aws import aws_models
qiOEr=super
qiOEF=None
qiOEG=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  qiOEr(LambdaLayer,self).__init__(arn)
  self.cwd=qiOEF
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.qiOEG.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,qiOEG,env=qiOEF):
  qiOEr(RDSDatabase,self).__init__(qiOEG,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,qiOEG,env=qiOEF):
  qiOEr(RDSCluster,self).__init__(qiOEG,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,qiOEG,env=qiOEF):
  qiOEr(AppSyncAPI,self).__init__(qiOEG,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,qiOEG,env=qiOEF):
  qiOEr(AmplifyApp,self).__init__(qiOEG,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,qiOEG,env=qiOEF):
  qiOEr(ElastiCacheCluster,self).__init__(qiOEG,env=env)
class TransferServer(BaseComponent):
 def __init__(self,qiOEG,env=qiOEF):
  qiOEr(TransferServer,self).__init__(qiOEG,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,qiOEG,env=qiOEF):
  qiOEr(CloudFrontDistribution,self).__init__(qiOEG,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,qiOEG,env=qiOEF):
  qiOEr(CodeCommitRepository,self).__init__(qiOEG,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
