#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

BASE_VPNAAS_ENDPOINT = '/vpnaas'
BASE_TUNNEL_ENDPOINT = '/tunnel'

BASE_VPNSERVER_URL = BASE_VPNAAS_ENDPOINT + '/vpnservers'
BASE_SINGLE_LB_URL = BASE_VPNSERVER_URL + '/{uuid}'
BASE_LB_STATS_URL = BASE_SINGLE_LB_URL + '/stats'
BASE_VPNSERVER_STATUS_URL = BASE_SINGLE_LB_URL + '/status'
BASE_VPNSERVER_FAILOVER_URL = BASE_SINGLE_LB_URL + '/failover'

BASE_LISTENER_URL = BASE_VPNAAS_ENDPOINT + '/listeners'
BASE_SINGLE_LISTENER_URL = BASE_LISTENER_URL + '/{uuid}'
BASE_LISTENER_STATS_URL = BASE_SINGLE_LISTENER_URL + '/stats'

BASE_USER_URL = BASE_VPNAAS_ENDPOINT + '/users'
BASE_SINGLE_USER_URL = BASE_USER_URL + '/{uuid}'
BASE_USER_STATS_URL = BASE_SINGLE_USER_URL + '/stats'

BASE_RESOURCE_URL = BASE_VPNAAS_ENDPOINT + '/resources'
BASE_SINGLE_RESOURCE_URL = BASE_RESOURCE_URL + '/{uuid}'
BASE_RESOURCE_STATS_URL = BASE_SINGLE_RESOURCE_URL + '/stats'

BASE_SECGROUP_URL = BASE_VPNAAS_ENDPOINT + '/secgroups'
BASE_SINGLE_SECGROUP_URL = BASE_SECGROUP_URL + '/{uuid}'
BASE_SECGROUP_STATS_URL = BASE_SINGLE_SECGROUP_URL + '/stats'

BASE_POOL_URL = BASE_VPNAAS_ENDPOINT + '/pools'
BASE_SINGLE_POOL_URL = BASE_POOL_URL + '/{pool_id}'

BASE_MEMBER_URL = BASE_SINGLE_POOL_URL + '/members'
BASE_SINGLE_MEMBER_URL = BASE_MEMBER_URL + '/{member_id}'

BASE_HEALTH_MONITOR_URL = BASE_VPNAAS_ENDPOINT + '/healthmonitors'
BASE_SINGLE_HEALTH_MONITOR_URL = BASE_HEALTH_MONITOR_URL + '/{uuid}'

BASE_L7POLICY_URL = BASE_VPNAAS_ENDPOINT + '/l7policies'
BASE_SINGLE_L7POLICY_URL = BASE_L7POLICY_URL + '/{policy_uuid}'
BASE_L7RULE_URL = BASE_SINGLE_L7POLICY_URL + '/rules'
BASE_SINGLE_L7RULE_URL = BASE_SINGLE_L7POLICY_URL + '/rules/{rule_uuid}'

BASE_QUOTA_URL = BASE_VPNAAS_ENDPOINT + '/quotas'
BASE_SINGLE_QUOTA_URL = BASE_QUOTA_URL + '/{uuid}'
BASE_QUOTA_DEFAULT_URL = BASE_QUOTA_URL + '/defaults'

BASE_AMPHORA_URL = BASE_TUNNEL_ENDPOINT + "/amphorae"
BASE_SINGLE_AMPHORA_URL = BASE_AMPHORA_URL + "/{uuid}"
BASE_AMPHORA_CONFIGURE_URL = BASE_SINGLE_AMPHORA_URL + '/config'
BASE_AMPHORA_FAILOVER_URL = BASE_SINGLE_AMPHORA_URL + '/failover'
BASE_AMPHORA_STATS_URL = BASE_SINGLE_AMPHORA_URL + '/stats'

BASE_PROVIDER_URL = BASE_VPNAAS_ENDPOINT + "/providers"
BASE_PROVIDER_FLAVOR_CAPABILITY_URL = (
    BASE_VPNAAS_ENDPOINT + "/providers/{provider}/flavor_capabilities")
BASE_PROVIDER_AVAILABILITY_ZONE_CAPABILITY_URL = (
    BASE_VPNAAS_ENDPOINT + "/providers/{provider}"
                          "/availability_zone_capabilities"
)

BASE_FLAVOR_URL = BASE_VPNAAS_ENDPOINT + "/flavors"
BASE_SINGLE_FLAVOR_URL = BASE_FLAVOR_URL + "/{uuid}"
BASE_FLAVORPROFILE_URL = BASE_VPNAAS_ENDPOINT + "/flavorprofiles"
BASE_SINGLE_FLAVORPROFILE_URL = BASE_FLAVORPROFILE_URL + "/{uuid}"

BASE_AVAILABILITYZONE_URL = BASE_VPNAAS_ENDPOINT + "/availabilityzones"
BASE_SINGLE_AVAILABILITYZONE_URL = BASE_AVAILABILITYZONE_URL + "/{name}"
BASE_AVAILABILITYZONEPROFILE_URL = (BASE_VPNAAS_ENDPOINT +
                                    "/availabilityzoneprofiles")
BASE_SINGLE_AVAILABILITYZONEPROFILE_URL = (BASE_AVAILABILITYZONEPROFILE_URL +
                                           "/{uuid}")
