from localstack.utils.aws import aws_models
dqlxn=super
dqlxW=None
dqlxT=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  dqlxn(LambdaLayer,self).__init__(arn)
  self.cwd=dqlxW
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.dqlxT.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,dqlxT,env=dqlxW):
  dqlxn(RDSDatabase,self).__init__(dqlxT,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,dqlxT,env=dqlxW):
  dqlxn(RDSCluster,self).__init__(dqlxT,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,dqlxT,env=dqlxW):
  dqlxn(AppSyncAPI,self).__init__(dqlxT,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,dqlxT,env=dqlxW):
  dqlxn(AmplifyApp,self).__init__(dqlxT,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,dqlxT,env=dqlxW):
  dqlxn(ElastiCacheCluster,self).__init__(dqlxT,env=env)
class TransferServer(BaseComponent):
 def __init__(self,dqlxT,env=dqlxW):
  dqlxn(TransferServer,self).__init__(dqlxT,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,dqlxT,env=dqlxW):
  dqlxn(CloudFrontDistribution,self).__init__(dqlxT,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,dqlxT,env=dqlxW):
  dqlxn(CodeCommitRepository,self).__init__(dqlxT,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
