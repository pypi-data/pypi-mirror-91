#!/usr/bin/python
#
# Copyright 2020 - A.L.I Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This is the API client development for COSMOS-API.
"""
import requests
import json

class Telemetry():
    """
    Simple Request maker for cosmos communication:
    - generate EndPoint for server.
    - generate hearder.
    - method to post telemetry json to server.
    """
    cosmos_ip = "dmtest.cosmos.ali.jp"

    def __init__(self, api_token):
        # Generate EndPoint URL
        self.generate_EndPoint()

        # Generate hearders
        self.token = api_token
        self.default_header = self.generate_header()
        self.json_header = self.generate_json_header()

        # Print ED ~ Status
        self.print_ED()

    def generate_EndPoint(self):
        # Generate EndPoint for Remote Server.
        self.ED_telemetry = 'https://' + Telemetry.cosmos_ip + '/api/drone/updatetm'
        self.ED_operation = 'https://' + Telemetry.cosmos_ip + '/api/drone/myoperation'

    def generate_header(self):
        # Generate simple header with token.
        return({'X-Api-Key': '{0}'.format(self.token)})

    def generate_json_header(self):
        # Generate header with data specification.
        header = {'Content-Type': 'application/json',
                    'Accept':'application/json',
                    'X-Api-Key': '{0}'.format(self.token)}
        return(header)

    def print_ED(self):
        # Print out EndPoint for information.
        print("\nCOSMOS_Requests initialized with:")
        print("  Token: {}".format(self.default_header))
        print("  ED_telemetry: {}".format(self.ED_telemetry))
        print("  ED_operation: {}\n".format(self.ED_operation))

    def send_telemetry(self, vehicle_state_json):
        # Dumps vehicle_state and Post telemetry data to ED_telemetry:
        response = requests.post(self.ED_telemetry,
                                headers=self.json_header,
                                data=json.dumps(vehicle_state_json))
        return(response)

    def get_operation(self):
        # Get request to extract operation details.
        response = requests.get(url=self.ED_operation, headers=self.default_header)
        operations = Operation(response)
        return(operations)

class Operation():
    """
    Operation helpers object to help parsing operation details from Cosmos Server.
    """

    def __init__(self, response):
        # Init object based on status_code
        self.status_code = response.status_code

        if self.status_code == 200:
            try:
                self.parse_operation(response.json())
            except Exception as e:
                print("Enable to parse operation: {}. Setting all to None.".format(e))
                self.status_code = -1

        else:
            print("Server error: {}".format(self.status_code))

    def parse_operation(self, response_json):
        # Parse the JSON operation
        self.MOCA = int(response_json["local_flight_alt"])
        self.waypoints = []
        self.mission = response_json["missions"]

        # WP extract
        for wp in response_json["waypoints"]:
            self.waypoints.append(WayPoint(wp))

    def get_wp(self, waypoint_slug):
        # Retrieved waypoint by waypoint slug
        if self.status_code == 200:
            target = [wp for wp in self.waypoints if wp.slug == waypoint_slug]
            if len(target)> 0:
                return target[0]
            else:
                print("No Waypoint found under the slug {}.".format(waypoint_slug))

    def display(self):
        # Display operation content
        if self.status_code == 200:
            print("Operation content:")
            print("MOCA: {}".format(self.MOCA))
            for wp in self.waypoints:
                wp.display()

class WayPoint():
    """
    Simple helper to parse Waypoint information.
    """
    def __init__(self, wp_json):
        self.latitude = wp_json['latitude']
        self.longitude = wp_json['longitude']
        self.altitude = wp_json['altitude']
        self.slug = wp_json['waypoint_slug']
        self.name = wp_json['waypoint_name']

    def coordinates(self):
        # Return tuples of this waypoint
        return (self.latitude, self.longitude, self.altitude)

    def display(self):
        # Simply print WP information
        print("Waypoint: {} ({})".format(self.name, self.slug))
        print("  lat: {} | lon: {} | alt: {} m.".format(self.latitude, self.longitude, self.altitude))
