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

class UpdateCasterSceneAudioRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'live', '2016-11-01', 'UpdateCasterSceneAudio','live')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_CasterId(self):
		return self.get_query_params().get('CasterId')

	def set_CasterId(self,CasterId):
		self.add_query_param('CasterId',CasterId)

	def get_OwnerId(self):
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)

	def get_AudioLayer(self):
		return self.get_query_params().get('AudioLayer')

	def set_AudioLayer(self, AudioLayers):
		for depth1 in range(len(AudioLayers)):
			if AudioLayers[depth1].get('VolumeRate') is not None:
				self.add_query_param('AudioLayer.' + str(depth1 + 1) + '.VolumeRate', AudioLayers[depth1].get('VolumeRate'))
			if AudioLayers[depth1].get('ValidChannel') is not None:
				self.add_query_param('AudioLayer.' + str(depth1 + 1) + '.ValidChannel', AudioLayers[depth1].get('ValidChannel'))
			if AudioLayers[depth1].get('FixedDelayDuration') is not None:
				self.add_query_param('AudioLayer.' + str(depth1 + 1) + '.FixedDelayDuration', AudioLayers[depth1].get('FixedDelayDuration'))

	def get_SceneId(self):
		return self.get_query_params().get('SceneId')

	def set_SceneId(self,SceneId):
		self.add_query_param('SceneId',SceneId)

	def get_MixList(self):
		return self.get_query_params().get('MixList')

	def set_MixList(self, MixLists):
		for depth1 in range(len(MixLists)):
			if MixLists[depth1] is not None:
				self.add_query_param('MixList.' + str(depth1 + 1) , MixLists[depth1])

	def get_FollowEnable(self):
		return self.get_query_params().get('FollowEnable')

	def set_FollowEnable(self,FollowEnable):
		self.add_query_param('FollowEnable',FollowEnable)