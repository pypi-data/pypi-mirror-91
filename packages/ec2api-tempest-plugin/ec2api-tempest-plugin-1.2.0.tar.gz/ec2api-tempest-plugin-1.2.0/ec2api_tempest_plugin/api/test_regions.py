# Copyright 2014 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tempest.lib import decorators

from ec2api_tempest_plugin import base
from ec2api_tempest_plugin import config

CONF = config.CONF


class RegionTest(base.EC2TestCase):

    @decorators.idempotent_id('f303e87e-4e5f-4110-a5da-5f690acb44ba')
    def test_describe_regions(self):
        data = self.client.describe_regions()
        self.assertNotEmpty(data['Regions'])

        region = CONF.aws.aws_region
        if not region:
            return

        regions = [r['RegionName'] for r in data['Regions']]
        self.assertIn(region, regions)

    @decorators.idempotent_id('be38f383-4637-4581-bb62-b47c1463f0a1')
    def test_describe_zones(self):
        data = self.client.describe_availability_zones()
        self.assertNotEmpty(data['AvailabilityZones'])

        region = CONF.aws.aws_region
        if not region:
            return

        # TODO(andrey-mp): add checking of other fields of returned data
