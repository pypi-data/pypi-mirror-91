from typing import Optional, List
from tabulate import tabulate
from .input_api_client import InputApiClient

import click


client = InputApiClient(auth=None)

def _tabulate(body, headers, title=None):
    tab = tabulate(
        body,
        headers=headers,
        tablefmt='fancy_grid',
    )
    if title:
        title_len = len(title)
        spacing = len(tab.split('\n')[0])

        roof = "=" * spacing
        floor = "=" * spacing

        left_multi = spacing // 2 - title_len // 2 - 1

        title_text_left = " " * left_multi + title
        title_text = title_text_left

        title_house = roof + '\n' + title_text + '\n' + floor
        tab = title_house + '\n' + tab
    return tab


def _get_table(sequence, headers, title=None):
    body = []
    for p in sequence:
        body.append([vars(p)[h] for h in headers])
    return _tabulate(body, headers, title)


@click.group()
def cli():
    """A CLI wrapper for Annotell utilities"""


@click.command()
@click.argument('project_id', nargs=1, default=None, required=False, type=int)
@click.option('--get-requests', is_flag=True)
@click.option('--get-input-lists', is_flag=True)
@click.option('--get-invalidated-inputs', is_flag=True)
def projects(project_id, get_requests, get_input_lists, get_invalidated_inputs):
    print()
    if get_input_lists and project_id:
        list_of_input_lists = client.list_input_lists(project_id)
        headers = ["id", "project_id", "name", "created"]
        tab = _get_table(list_of_input_lists, headers, "INPUTLISTS")
        print(tab)
    elif get_requests and project_id:
        headers = ["id", "created", "project_id", "title", "description", "input_list_id", "input_batch_id", "external_id"]
        list_of_requests = client.get_requests_for_project_id(project_id=project_id)
        tab = _get_table(list_of_requests, headers, "REQUESTS")
        print(tab)
    elif get_invalidated_inputs and project_id:
        headers = ["internal_id", "external_id", "input_type", "invalidated", "invalidated_reason"]

        list_of_inputs = client.get_inputs(project_id=project_id, invalidated=True)
        tab = _get_table(list_of_inputs, headers, "INPUTS")
        print(tab)
    elif project_id:
        list_of_projects = client.list_projects()
        target_project = [p for p in list_of_projects if p.id == project_id]
        headers = ["id", "created", "title", "description", "deadline", "status", "external_id"]
        tab = _get_table(target_project, headers, "PROJECTS")
        print(tab)
    else:
        list_of_projects = client.list_projects()
        headers = ["id", "created", "title", "description", "deadline", "status", "external_id"]
        tab = _get_table(list_of_projects, headers, "PROJECTS")
        print(tab)


@click.command()
@click.argument("internal_ids", nargs=-1, required=True)
@click.option("--view", is_flag=True)
@click.option("--get-export-status", is_flag=True)
@click.option("--get-upload-status", is_flag=True)
@click.option("--get-input-lists", is_flag=True)
@click.option("--get-datas", is_flag=True)
def inputs(internal_ids, view, get_export_status, get_upload_status, get_input_lists, get_datas):
    print()
    if internal_ids and view:
        view_dict = client.get_view_links(list(internal_ids))
        body = []
        headers = ["internal_id", "view_link"]
        for internal_id, link in view_dict.items():
            body.append([
                internal_id, link
            ])
        tab = _tabulate(body, headers, title="VIEW LINKS FOR INPUTS")
        print(tab)
    elif internal_ids and get_export_status:
        status_dict = client.get_input_status(list(internal_ids))
        body = []
        headers = ["internal_id", "request_id", "export_ready"]
        for (internal_id, requests_status) in status_dict.items():
            for (request_id, status) in requests_status.items():
                body.append([internal_id, request_id, status])
        tab = _tabulate(body, headers, title="EXPORT STATUS FOR INPUTS")
        print(tab)
    elif internal_ids and get_upload_status:
        list_of_jobs = client.get_input_jobs_status(internal_ids=list(internal_ids))
        headers = ["id", "internal_id", "external_id", "filename", "status", "added", "error_message"]
        tab = _get_table(list_of_jobs, headers, "UPLOAD STATUS FOR INPUTS")
        print(tab)

    elif internal_ids and get_input_lists:
        dict_of_lists = client.get_input_lists_for_inputs(list(internal_ids))
        body = [[k, v] for k, v in dict_of_lists.items()]
        headers = ["internal_id", "input_list"]
        tab = _tabulate(body, headers, "INPUT LISTS FOR INPUTS")
        print(tab)

    elif internal_ids and get_datas:
        dict_of_datas = client.get_datas_for_inputs_by_internal_ids(internal_ids)
        headers = ["input", "datas"]
        padded_body = []
        for (input_obj, datas) in dict_of_datas.items():
            padded_body.append([input_obj, datas[0]])
            for data in datas[1:]:
                padded_body.append(["", data])
        tab = _tabulate(padded_body, headers, "DATAS IN INPUTS")
        print(tab)


@click.command(name="inputs-externalid")
@click.argument("external_ids", nargs=-1, required=True)
@click.option("--get-upload-status", is_flag=True)
@click.option("--get-datas", is_flag=True)
def inputs_externalid(external_ids, get_upload_status, get_datas):
    print()
    if external_ids and get_upload_status:
        headers = ["id", "internal_id", "external_id", "filename", "status", "added", "error_message"]
        list_of_jobs = client.get_input_jobs_status(external_ids=list(external_ids))
        tab = _get_table(list_of_jobs, headers, title="UPLOAD STATUS FOR INPUTS")
        print(tab)
    elif external_ids and get_datas:
        dict_of_datas = client.get_datas_for_inputs_by_external_ids(external_ids)
        headers = ["input", "datas"]
        padded_body = []
        for (input_obj, datas) in dict_of_datas.items():
            padded_body.append([input_obj, datas[0]])
            for data in datas[1:]:
                padded_body.append(["", data])
        tab = _tabulate(padded_body, headers, "DATAS IN INPUTS")
        print(tab)

    else:
        to_internal_dict = client.get_internal_ids_for_external_ids(list(external_ids))
        body = []
        headers = ["external_id", "internal_id"]
        for external_id, internal_ids in to_internal_dict.items():
            for internal_id in internal_ids:
                body.append(
                    [external_id, internal_id]
                )
        tab = _tabulate(body, headers, title="EXTERNAL IDS TO INTERNAL IDS")
        print(tab)


@click.command()
@click.argument('id', nargs=1, default=None, required=False, type=int)
@click.option('--raw', is_flag=True)
def calibration(id, raw):
    print()
    list_of_calibrations = client.get_calibration_data(id, None)
    if id:
        headers = ["id", "external_id", "created"]
        tab = _get_table(list_of_calibrations, headers, "CALIBRATION")
        print(tab)
        if raw:
            print()
            [print(calib.calibration) for calib in list_of_calibrations]
    else:
        headers = ["id", "external_id", "created"]
        tab = _get_table(list_of_calibrations, headers, "CALIBRATION")
        print(tab)


@click.command(name="calibration-externalid")
@click.argument("external_id", nargs=1, required=True)
def calibration_externalid(external_id):
    print()
    list_of_calibrations = client.get_calibration_data(None, external_id)
    headers = ["id", "external_id", "created"]
    tab = _get_table(list_of_calibrations, headers, "CALIBRATION")
    print(tab)


@click.argument('request_ids', nargs=-1)
@click.command()
def requests(request_ids):
    headers = ["id", "created", "project_id", "title", "description", "input_list_id", "input_batch_id", "external_id"]
    request_ids_list = [int(rid) for rid in request_ids]
    dict_of_requests = client.get_requests_for_request_ids(
        request_ids=request_ids_list
    )
    list_of_requests = [dict_of_requests[k] for k in request_ids_list]
    tab = _get_table(list_of_requests, headers, "REQUESTS")
    print(tab)


@click.command(name="input-lists")
@click.argument('input_list_id', nargs=1, type=int, default=None, required=False)
@click.option('--get-requests', is_flag=True)
def input_lists(input_list_id, get_requests):
    print()
    if input_list_id and get_requests:
        headers = ["id", "created", "project_id", "title", "description", "input_list_id"]
        list_of_requests = client.get_requests_for_input_lists(input_list_id)
        tab = _get_table(list_of_requests, headers, "REQUESTS")
        print(tab)

@click.command(name="batches")
@click.argument('project', nargs=1, type=str, default=None, required=False)
def input_batch(project):
    print()
    if project:
        headers = ["external_id", "title",  "status", "created", "updated"]
        list_of_batches = client.list_project_batches(project)
        tab = _get_table(list_of_batches, headers, "BATCHES")
        print(tab)


cli.add_command(projects)
cli.add_command(inputs)
cli.add_command(inputs_externalid)
cli.add_command(calibration)
cli.add_command(calibration_externalid)
cli.add_command(requests)
cli.add_command(input_lists)
cli.add_command(input_batch)


def main():
    cli(prog_name="annoutil")
