# COSMOS API client

This is a simple client package to help you connect your drone to COSMOS API by:
- Generating End-Points.
- Generating and processing Post-Request to the End-point.
- Parsing Operation content.

For a complete API description, please refer to [COSMOS-API](https://dmtest.cosmos.ali.jp/docapi).

## How to use
After getting the token from COSMOS: ```api_token_example```, you can connect and update the telemetry with:
```python
import cosmos_api

api_token = "api_token_example"
telemetry_updater = cosmos_api.Telemetry(api_token)
vehicle_state = {"activity": "idle", --- ,"battery": "90%"}
response = telemetry_updater.send_telemetry(vehicle_state)
```

## How to build your **vehicle_state**

**vehicle_state** is a *python dict* variable which include the essential telemetry from the drone.
This variable will be passed to the server as a json dump.

A basic template can be:
```python
vehicle_state = {
        "activity": "idle",
        "stamp": 1602,
        "gps_0": {
            "fix": 3,
            "numsat": 10},
        "mode": "STABILIZE",
        "velocity": [0.0, -0.01, 0.0],
        "battery": {
            "level": 100,
            "current": 0.0,
            "voltage": 12.587},
        "state": "STANDBY",
        "location": {
            "global_frame": {
                "lat": 35.9341147,
                "lon": 139.5689006,
                "alt": 0}},
        "ground_speed": 0.0,
        "attitude": {
            "pitch": 0.0004752922395709902,
            "roll": 0.0007311428198590875,
            "yaw": -3.1402206420898438},
        "armed": False,
        "order_feedback": {
            "message": "",
            "type": ""},
        "heading": 180}
```

## Operation
Cosmos provide operation information to the drone via ```/api/drone/myoperation``` endpoint.
You can get all the information with:
```python
operation = self.telemetry_updater.get_operation()
operation.display()

# Extract Waypoint with slug:
wp = operation.get_wp("A")
wp.display()
lat, lon, alt = wp.coordinates()
```

# API description

## ```constructor```

- Description
```shell
Send the telemetry to COSMOS server, .

Parameters
----------
api_token : str
    A string of the shared api token obtained from the server.

Returns
-------
cosmos_api.Telemetry Object
    A helper to send drone telemetry to cosmos server.
```

- Use with:
```python
telemetry_updater = cosmos_api.Telemetry(api_token)
```

## ```send_telemetry```
- Description
```shell
Post the telemetry to COSMOS server, to the correct EndPoint with a functional header generated with the shared token.

Parameters
----------
vehicle_state : dict
    vehicle_state a dictionary including drone telemetry field.

Returns
-------
requests.Response Object
    The response to the post request. Please refer to requests documentation and bellow for error codes.
```

- Use with:
```python
response = telemetry_updater.send_telemetry(vehicle_state)
```

- Server Code:
```
OK = 200: Telemetry posted correctly.
WRONGTELEMETRY = 400: Wrong or incomplete telemetry format.
WRONGTOKEN = 401: No drone registered under the used token.
```

## ```get_operation```
- Description
```shell
Get the information of the active operation of the drone. This helper will report error code, and parse the operation content.

Parameters
----------
None

Returns
-------
cosmos_api.Operation Object
    The content of the operation parsed under Operation-Object attribute. (see Operation Object documentation)
```

- Use with:
```python
operation = telemetry_updater.get_operation()
```

## class ```Operation```

- Description
A class used to access operation content.

### Attributes
----------
- ```status_code``` : int \
    server status code error.
- ```MOCA``` : int \
    Minimun Obstacle Cleared Altitude of the operation in meter.
- ```waypoints``` : list of WayPoint object \
    List of all the waypoint formated under the WayPoint Object.
- ```mission``` : json \
    Specific mission content. (TODO)

### Methods
-------
- ```display()```:\
Prints the operation content.
- ```get_wp(waypoint_slug)```:\
Retrieve Waypoint by slug.
Args: waypoint_slug (string)
Return: waypoint (WayPoint object).


- Use with:
```python
operation = telemetry_updater.get_operation()
operation.display()
wp = operation.get_wp("A")
wp.display()
lat, lon, alt = wp.coordinates()
```

## class ```WayPoint```

- Description
A class used to acces Waypoint information.

### Attributes
----------
- ```name``` : str\
    Waypoint name on the MAP.
- ```slug``` : str\
    Short name of the Waypoint.\
- ```latitude``` : double\
    latitude of the waypoint in °.
- ```longitude``` : double\
    longitude of the waypoint in °.
- ```altitude``` : float\
    altitude of the waypoint in meter.

### Methods
-------
- ```display()```\
Prints the waypoint content.

- ```coordinates()```\
Return a tuple containing (latitude, longitude, altitude).