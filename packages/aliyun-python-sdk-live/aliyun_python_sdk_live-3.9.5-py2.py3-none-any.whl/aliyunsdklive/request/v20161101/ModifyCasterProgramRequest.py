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

from aliyunsdkcore.request import RpcRequest
from aliyunsdklive.endpoint import endpoint_data

class ModifyCasterProgramRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'live', '2016-11-01', 'ModifyCasterProgram','live')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_Episode(self):
		return self.get_query_params().get('Episode')

	def set_Episode(self, Episodes):
		for depth1 in range(len(Episodes)):
			if Episodes[depth1].get('EpisodeId') is not None:
				self.add_query_param('Episode.' + str(depth1 + 1) + '.EpisodeId', Episodes[depth1].get('EpisodeId'))
			if Episodes[depth1].get('EpisodeType') is not None:
				self.add_query_param('Episode.' + str(depth1 + 1) + '.EpisodeType', Episodes[depth1].get('EpisodeType'))
			if Episodes[depth1].get('EpisodeName') is not None:
				self.add_query_param('Episode.' + str(depth1 + 1) + '.EpisodeName', Episodes[depth1].get('EpisodeName'))
			if Episodes[depth1].get('ResourceId') is not None:
				self.add_query_param('Episode.' + str(depth1 + 1) + '.ResourceId', Episodes[depth1].get('ResourceId'))
			if Episodes[depth1].get('ComponentId') is not None:
				for depth2 in range(len(Episodes[depth1].get('ComponentId'))):
					if Episodes[depth1].get('ComponentId')[depth2] is not None:
						self.add_query_param('Episode.' + str(depth1 + 1) + '.ComponentId.' + str(depth2 + 1) , Episodes[depth1].get('ComponentId')[depth2])
			if Episodes[depth1].get('StartTime') is not None:
				self.add_query_param('Episode.' + str(depth1 + 1) + '.StartTime', Episodes[depth1].get('StartTime'))
			if Episodes[depth1].get('EndTime') is not None:
				self.add_query_param('Episode.' + str(depth1 + 1) + '.EndTime', Episodes[depth1].get('EndTime'))
			if Episodes[depth1].get('SwitchType') is not None:
				self.add_query_param('Episode.' + str(depth1 + 1) + '.SwitchType', Episodes[depth1].get('SwitchType'))

	def get_CasterId(self):
		return self.get_query_params().get('CasterId')

	def set_CasterId(self,CasterId):
		self.add_query_param('CasterId',CasterId)

	def get_OwnerId(self):
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)