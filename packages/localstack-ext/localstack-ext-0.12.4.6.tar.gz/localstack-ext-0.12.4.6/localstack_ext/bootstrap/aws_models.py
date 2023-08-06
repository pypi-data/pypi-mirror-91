from localstack.utils.aws import aws_models
dzoWk=super
dzoWr=None
dzoWF=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  dzoWk(LambdaLayer,self).__init__(arn)
  self.cwd=dzoWr
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.dzoWF.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,dzoWF,env=dzoWr):
  dzoWk(RDSDatabase,self).__init__(dzoWF,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,dzoWF,env=dzoWr):
  dzoWk(RDSCluster,self).__init__(dzoWF,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,dzoWF,env=dzoWr):
  dzoWk(AppSyncAPI,self).__init__(dzoWF,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,dzoWF,env=dzoWr):
  dzoWk(AmplifyApp,self).__init__(dzoWF,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,dzoWF,env=dzoWr):
  dzoWk(ElastiCacheCluster,self).__init__(dzoWF,env=env)
class TransferServer(BaseComponent):
 def __init__(self,dzoWF,env=dzoWr):
  dzoWk(TransferServer,self).__init__(dzoWF,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,dzoWF,env=dzoWr):
  dzoWk(CloudFrontDistribution,self).__init__(dzoWF,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,dzoWF,env=dzoWr):
  dzoWk(CodeCommitRepository,self).__init__(dzoWF,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
