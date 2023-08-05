import os
import pkg_resources
import pydoc
import time

from mule.error import messages
from mule.util import file_util
from mule.util import get_dict_value


def get_validated_mule_yaml(mule_config):
    # Note that agents are optional!

    mule_config_keys = mule_config.keys()

    if 'jobs' not in mule_config_keys:
        raise Exception(messages.FIELD_NOT_FOUND.format('jobs'))
    if 'tasks' not in mule_config_keys:
        raise Exception(messages.FIELD_NOT_FOUND.format('tasks'))

    agent_configs = mule_config['agents'] if 'agents' in mule_config else []
    jobs_configs = mule_config['jobs']
    task_configs = mule_config['tasks']

    mule_configs = [
        ("jobs", jobs_configs, validate_block),
        ("tasks", task_configs, validate_tasks)
    ]

    if len(agent_configs):
        mule_configs.append(("agents", agent_configs, validate_list))

    for (name, config, fn) in mule_configs:
        try:
            fn(name, config)
        except Exception as error:
            raise Exception(messages.FIELD_VALUE_COULD_NOT_BE_VALIDATED.format(
                name,
                str(error)
            ))

    return agent_configs, jobs_configs, task_configs


def validate_block(name, config):
    if not type(config) == dict:
        raise Exception(messages.FIELD_VALUE_WRONG_TYPE.format(name, dict, type(config)))


def validate_list(name, config):
    if not type(config) == list:
        raise Exception(messages.FIELD_VALUE_WRONG_TYPE.format(name, list, type(config)))


def validate_tasks(name, task_configs):
    validate_list(name, task_configs)
    for index, config in enumerate(task_configs):
        validate_block(name, config)


def validate_typed_fields(task_id, task_fields, task_required_typed_fields, task_optional_typed_fields):
    for required_field, required_field_type in task_required_typed_fields:
        required_field_index = required_field.split('.')
        required_field_value = get_dict_value(task_fields, required_field_index)
        if required_field_value is None:
            raise Exception(messages.TASK_MISSING_REQUIRED_FIELDS.format(
                task_id,
                required_field,
                task_required_typed_fields,
            ))
        if not type(required_field_value) == required_field_type:
            raise Exception(messages.TASK_FIELD_IS_WRONG_TYPE.format(
                task_id,
                required_field,
                required_field_type,
                type(required_field_value)
            ))
    for optional_field, optional_field_type in task_optional_typed_fields:
        optional_field_index = optional_field.split('.')
        optional_field_value = get_dict_value(task_fields, optional_field_index)
        if optional_field_value is not None:
            if not type(optional_field_value) == optional_field_type:
                raise Exception(messages.TASK_FIELD_IS_WRONG_TYPE.format(
                    task_id,
                    optional_field,
                    optional_field_type,
                    type(optional_field_value)
                ))


def validateTaskConfig(task_config):
    if 'task' not in task_config:
        raise Exception(messages.TASK_FIELD_MISSING)


def get_plugin(name):
    return [
        entry_point.load()
        for entry_point in pkg_resources.iter_entry_points(group="mule.plugin")
        if name == entry_point.name
    ]


def get_cls(task_config):
    # TODO: Fix up the exception handling here.
    task_name = task_config['task']
    try:
        found = False
        name, cls = task_name.split('.')
        module = get_plugin(name)
        if len(module):
            # For now, pick whichever modules wins.
            for key, val in module[0].__dict__.items():
                if key == cls:
                    found = True
                    return val(task_config)
        if not found:
            raise Exception(messages.CANNOT_LOCATE_TASK.format(task_name))
    except:
        raise Exception(messages.CANNOT_LOCATE_TASK.format(task_name))


def get_validated_tasks(job_context, dependencies):
    tasks_tbd = []
    while len(dependencies) > 0:
        dependency = dependencies.pop(0)
        task_context = job_context.get_field(f"{dependency[0]}")
        if not task_context:
            raise Exception(messages.CANNOT_LOCATE_TASK_CONFIGS.format(dependency[1], dependency[0]))
        tasks_tbd.append(get_cls(task_context['inputs']))
    return tasks_tbd


def validateRequiredTaskFieldsPresent(task_id, fields, required_fields):
    for field in required_fields:
        if field not in fields.keys():
            raise Exception(messages.TASK_MISSING_REQUIRED_FIELDS.format(
                task_id,
                field,
                str(required_fields)
            ))
