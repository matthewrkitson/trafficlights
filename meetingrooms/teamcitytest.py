#!/usr/bin/python3
import pdb;

import json
import requests
import getpass
from security import unprotect
from config import get_config
from lights import get_lights, red, green, on, off, all_on
from log import logger

config = get_config("teamcity")
username = config["username"]
password = getpass.getpass()

print(username, password)
auth = (username, password)
headers = { "accept": "application/json" }
lights = get_lights()

def build_status(buildId):
    url = "http://teamcity/app/rest/builds/buildType:" + buildId + ",failedToStart:any"
    buildResponse = requests.get(url, auth=auth, headers=headers)
    build = buildResponse.json()
    buildStatus = build["status"]
    return buildStatus

def get_counted_item(dict, key1, key2):
    if dict[key1]["count"] == 0: return []
    return dict[key1][key2]

def project_status(projectId):
    url = "http://teamcity/app/rest/projects/id:" + projectId
    projectResponse = requests.get(url, auth=auth, headers=headers)
    project = projectResponse.json()
    buildTypes = get_counted_item(project, "buildTypes", "buildType")
    subProjects = get_counted_item(project, "projects", "project")

    logger.info(projectId)
    status = True
    for buildType in buildTypes:
        buildStatus = build_status(buildType["id"])
        status = status and (buildStatus == "SUCCESS")
        logger.info("  Build Type ID: " + buildType["id"] + " " + buildStatus)

    for subProject in subProjects:
        projectStatus = project_status(subProject["id"])
        status = status and (projectStatus == "SUCCESS")
        logger.info("  Subproject ID: " + subProject["id"] + " " + projectStatus)

    return "SUCCESS" if status else "FAILURE"


for target in config["targets"]:
    type, id = target[0], target[1]

    if type == 'build':
        status = build_status(id)
        logger.info(id + ": " + status)
    elif type == 'project':
        status = project_status(id)
        logger.info(id + ": " + status)
    else:
        logger.info("Unrecognised target type: " + type)

