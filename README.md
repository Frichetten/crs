# aws-research-scripts
Random tools to make research/testing easier.

As a researcher, I often manually perform certain checks while doing research. I've gathered these techniques from years of experience, however they may be tedious or time consuming to perform. To help ensure a consistent research methodology (i.e. I don't forget about these) i'm storing scripts to perform these checks here, along with the resources needed to perform them. An explanation of each one is below.

## enum-endpoint.py
```
usage: ./enum-endpoint.py <service name>
Enumerating: <service name>
<service name>.us-east-1.amazonaws.com
```
Resources used: `aws-regions.json`, `aws-stage-names.json`, `aws-endpoint-templates.json`

This script is used to try and find endpoints for a given service name (both production and non-production). It does this by brute forcing DNS based on the service name, regions, and the various endpoint templates I've gathered. If one (or more) is found, it is printed to the console.