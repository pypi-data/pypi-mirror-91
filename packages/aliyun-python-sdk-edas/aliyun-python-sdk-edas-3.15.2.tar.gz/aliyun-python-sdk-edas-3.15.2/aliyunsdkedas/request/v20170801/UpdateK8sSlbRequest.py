# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RoaRequest
from aliyunsdkedas.endpoint import endpoint_data

class UpdateK8sSlbRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'Edas', '2017-08-01', 'UpdateK8sSlb','edas')
		self.set_uri_pattern('/pop/v5/k8s/acs/k8s_slb_binding')
		self.set_method('PUT')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_Scheduler(self):
		return self.get_query_params().get('Scheduler')

	def set_Scheduler(self,Scheduler):
		self.add_query_param('Scheduler',Scheduler)

	def get_ServicePortInfos(self):
		return self.get_query_params().get('ServicePortInfos')

	def set_ServicePortInfos(self,ServicePortInfos):
		self.add_query_param('ServicePortInfos',ServicePortInfos)

	def get_SlbProtocol(self):
		return self.get_query_params().get('SlbProtocol')

	def set_SlbProtocol(self,SlbProtocol):
		self.add_query_param('SlbProtocol',SlbProtocol)

	def get_SlbName(self):
		return self.get_query_params().get('SlbName')

	def set_SlbName(self,SlbName):
		self.add_query_param('SlbName',SlbName)

	def get_Port(self):
		return self.get_query_params().get('Port')

	def set_Port(self,Port):
		self.add_query_param('Port',Port)

	def get_AppId(self):
		return self.get_query_params().get('AppId')

	def set_AppId(self,AppId):
		self.add_query_param('AppId',AppId)

	def get_Specification(self):
		return self.get_query_params().get('Specification')

	def set_Specification(self,Specification):
		self.add_query_param('Specification',Specification)

	def get_ClusterId(self):
		return self.get_query_params().get('ClusterId')

	def set_ClusterId(self,ClusterId):
		self.add_query_param('ClusterId',ClusterId)

	def get_Type(self):
		return self.get_query_params().get('Type')

	def set_Type(self,Type):
		self.add_query_param('Type',Type)

	def get_TargetPort(self):
		return self.get_query_params().get('TargetPort')

	def set_TargetPort(self,TargetPort):
		self.add_query_param('TargetPort',TargetPort)