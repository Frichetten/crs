#!/usr/bin/env python3
import sys, json, socket

if len(sys.argv) != 2:
    print("Usage: ./enum-endpoint.py <service name>")
    sys.exit(1)

REGIONS = json.load(open("./resources/aws-regions.json", "r"))['AWS_REGIONS']
ENDPOINT_TEMPLATES = json.load(open("./resources/aws-endpoint-templates.json", "r"))['AWS_ENDPOINT_TEMPLATES']
STAGE_NAMES = json.load(open("./resources/aws-stage-names.json", "r"))['AWS_STAGE_NAMES']
SERVICE_NAME = sys.argv[1]

print(f"Enumerating: {SERVICE_NAME}")

for endpoint_template in ENDPOINT_TEMPLATES:
    search_space = []
    temp_endpoint = endpoint_template

    if "{region}" in temp_endpoint and "{stage}" in temp_endpoint:
        for region in REGIONS:
            for stage in STAGE_NAMES:
                search_space.append(temp_endpoint
                                    .replace("{service}", SERVICE_NAME)
                                    .replace("{region}", region)
                                    .replace("{stage}", stage))
                search_space.append(temp_endpoint
                                    .replace("{service}", f"{SERVICE_NAME}-{stage}")
                                    .replace("{region}", region)
                                    .replace("{stage}", stage))
    elif "{region}" in temp_endpoint:
        for region in REGIONS:
            search_space.append(temp_endpoint
                                .replace("{service}", SERVICE_NAME)
                                .replace("{region}", region))
            for stage in STAGE_NAMES:
                search_space.append(temp_endpoint
                                    .replace("{service}", f"{SERVICE_NAME}-{stage}")
                                    .replace("{region}", region))
    elif "{stage}" in temp_endpoint:
        for stage in STAGE_NAMES:
            search_space.append(temp_endpoint
                                .replace("{service}", SERVICE_NAME)
                                .replace("{stage}", stage))
            search_space.append(temp_endpoint
                                .replace("{service}", f"{SERVICE_NAME}-{stage}")
                                .replace("{stage}", stage))
    elif "{service}" in temp_endpoint:
            search_space.append(temp_endpoint
                                .replace("{service}", SERVICE_NAME))
            for stage in STAGE_NAMES:
                search_space.append(temp_endpoint
                                    .replace("{service}", f"{SERVICE_NAME}-{stage}"))

    for endpoint in search_space:
        try:
            socket.gethostbyname(endpoint)
            print(endpoint)
        except socket.gaierror as e:
            if "{" in endpoint or "}" in endpoint:
                print(f"Something went wrong: {endpoint}")
    