from azure.identity import ClientSecretCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import RunFilterParameters
import time
import functools as ft
# import yaml
# from datetime import datetime, timedelta
# import time
# import os, sys


def authenticate(clientid, secret, tenant):
    """
    Wraps the ClientSecretCredential object. Handle these values with care! Best practice is to securely set them as environment variables in CI/CD pipelines or non-source control managed configs if testing locally.
    """
    credentials = ClientSecretCredential(
        client_id=clientid, 
        client_secret=secret, 
        tenant_id=tenant
    )
    return credentials


def connect_to_df(credentials, subscription_id):
    """
    This connects to the specified data factory instance.
    """
    adf_client = DataFactoryManagementClient(credentials, subscription_id)
    return adf_client

def create_pipeline_run(adf_client, pipeline_args):
    """
    This creates a pipeline run. Pipeline_args are resource_group_name,factory_name, pipeline_name and optional parameters={}
    """
    run_response = adf_client.pipelines.create_run(**pipeline_args)
    return run_response

def monitor_pipeline_run(adf_client, get_run_args):
    "This returns a specific pipeline run for use in other functions. Get_run_args are resource_group_name, factory_name, and run_id. Get the run_id after creating the pipeline_run using create_pipeline_run then pass the get_run_args variable to this function."
    pipeline_run = adf_client.pipeline_runs.get(**get_run_args)
    return pipeline_run

def wait_for_pipeline_to_finish(adf_client, get_run_args):
    """
    This simply waits for a pipeline to finish. Pass the data factory client along with the get_run_args including the specific run id. That will get passed to the internal instance of moinitor_pipeline_run.
    """
    i = 1
    pipeline_run = monitor_pipeline_run(adf_client, get_run_args)
    while pipeline_run.status in ["Queued", "InProgress", "Canceling"]:
        time.sleep(10)
        print("loop #%s" % i)
        print(pipeline_run.status)
        pipeline_run = monitor_pipeline_run(adf_client, get_run_args)
        i+=1
    print(pipeline_run.status)
    return pipeline_run.status

def get_specific_activity(adf_client, get_run_args, activity_name):
    """
    This queries the a specific pipeline run and returns a dictionary representation of the activity under test. Get_run_args will need the run_id of the specific pipeline run. The activity name needs to be unique and a valid string.
    """
    pipelinerun = monitor_pipeline_run(adf_client, get_run_args)
    filters = RunFilterParameters(last_updated_after=pipelinerun.run_start, last_updated_before=pipelinerun.run_end)
    factoryname = get_run_args['factory_name']
    resourcegroup = get_run_args['resource_group_name']
    activityruns = adf_client.activity_runs.query_by_pipeline_run(
    factory_name = factoryname,
    run_id= pipelinerun.run_id,
    filter_parameters = filters,
    resource_group_name = resourcegroup)
    activity_search = [x.as_dict() for x in activityruns.value if x.as_dict()['activity_name'] == activity_name]
    if activity_search == []:
        print("No activity with name {} found.".format(activity_name))
        return
    elif len(activity_search)>1:
        print("More than one activity found with name {}. Name your activities more specifically.".format(activity_name))
        return
    elif len(activity_search) == 1:
        print("Activity {} found".format(activity_name))
        activity = activity_search[0]
        return activity
    else:
        print("Something else went randomly wrong in looking for activity {}.".format(activity_name))
        return

def get_activity_attribute(activity, attribute_search):
    """
    This returns the requested attribute from the activity dictionary. The attribute can be of any arbitrary depth but must be passed as a list. For example: ["output", "writeRows"]. 
    """
    if type(attribute_search) == str:
        attribute = activity[attribute_search]
        return attribute
    elif type(attribute_search) == list:
        attribute = ft.reduce(lambda val, key: val.get(key) if val else None, attribute_search, activity)
        return attribute
    else:
        print("Need to pass str or list for attribute_search")
        return

def process_attribute_search_string(attribute_search_base):
    """
    This processes string input into ouput that can then be input into the get_activity_attribute function. The function processes strings like '[Output, rowsWritten]' to a list like ['Output', 'rowsWritten']
    """
    if "[" in attribute_search_base:
        attribute_search = list(map(str, attribute_search_base.strip('[]').split(',')))
        attribute_search = [x.replace(" ", "") for x in attribute_search]
    elif "[" not in attribute_search_base:
        attribute_search = attribute_search_base
    else:
        print("Invalid construction for attribute search passed, setting attribute search to None")
        attribute_search = None   
    return attribute_search