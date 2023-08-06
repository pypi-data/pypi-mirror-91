from copy import deepcopy
from logging import getLogger
from os import path

from jinja2 import Template

logger = getLogger(__name__)


class ParseError(Exception):
    pass


def parse_type(string):
    if (check := {'string': 'str', 'array': 'list', 'object': 'dict',
                  'boolean': 'bool', 'integer': 'int', 'number': 'float'}.setdefault(string, None)) is not None:
        return check
    prefixes = ('#/components/schemas/', '#/components/parameters/')
    for prefix in prefixes:
        if string.startswith(prefix):
            return string.removeprefix(prefix)
    print(string)


def get_item_type(item_data):
    if (no_type := 'type' not in item_data) and ('$ref' not in item_data):
        raise ParseError('dict component property item type')
    item_type = parse_type(item_data['$ref' if no_type else 'type'])
    return item_type


def stage_1_dict_components(data: dict):
    # 执行分流过程
    if set(data['components'].keys()) - {'schemas', 'parameters'}:
        raise ParseError('data.components.schemas')
    components: dict[str, dict]
    components = data['components']['schemas']
    components = {k: v for k, v in components.items() if 'type' in v and v['type'] == 'object'}

    # 解析数据
    # {component_name: {'properties': {property_name: {'type': property_type,
    #                                                  'item_type': item_type}}}}
    result = {}
    for component_name, component_data in components.items():
        parsed_component = result.setdefault(component_name, {})
        parsed_properties = parsed_component.setdefault('properties', {})
        if 'properties' not in component_data:
            continue
        for property_name, property_data in component_data['properties'].items():
            parsed_property_data = parsed_properties.setdefault(property_name, {})
            property_data: dict
            if '$ref' in property_data:
                property_type = parse_type(property_data['$ref'])
            elif 'type' in property_data:
                property_type = parse_type(property_data['type'])
            else:
                raise ParseError('dict component property type')
            parsed_property_data['type'] = property_type
            if property_type == 'list':
                parsed_property_data['item_type'] = get_item_type(property_data['items'])
    return result


def stage_2_list_components(data: dict):
    # 分流
    components = data['components']['schemas']
    components = {k: v for k, v in components.items() if 'type' in v and v['type'] == 'array'}

    # 解析数据
    parsed_components = {}
    for component_name, component_data in components.items():
        parsed_component_data = parsed_components.setdefault(component_name, {})
        if 'items' not in component_data:
            raise ParseError('list component items not found')
        parsed_component_data['item_type'] = get_item_type(component_data['items'])
    return parsed_components


def stage_3_alias_components(data: dict):
    # 分流
    components = data['components']['schemas']
    components = {k: v for k, v in components.items() if 'type' in v and v['type'] not in ('array', 'object')}

    # 解析数据
    parsed_components = {}
    for component_name, component_data in components.items():
        parsed_component = parsed_components.setdefault(component_name, {})
        parsed_component['type'] = parse_type(component_data['type'])
    return parsed_components


def stage_4_parameters(data: dict):
    if 'parameters' not in data['components']:
        return {}
    parameters: dict = data['components']['parameters']
    parsed_parameters = {}
    for parameter_name, parameter_data in parameters.items():
        parsed_parameter = parsed_parameters.setdefault(parameter_name, {})
        schema_data: dict = parameter_data['schema']
        parsed_parameter['type'] = parse_type(schema_data['type'])
    return parsed_parameters


def stage_5_ref_components(data: dict):
    # 分流
    components = data['components']['schemas']
    components = {k: v for k, v in components.items() if 'type' not in v}
    if not components:
        return {}

    # 解析数据
    parsed_components = {}
    for component_name, component_data in components.items():
        parsed_component = parsed_components.setdefault(component_name, {})
        parsed_component['type'] = parse_type(component_data['$ref'])
    return parsed_components


def stage_6_operations(data: dict):
    paths = data['paths']
    parsed_operations = {}
    for url, url_data in paths.items():
        for method, method_data in url_data.items():
            parsed_operation_data = parsed_operations.setdefault(method_data['operationId'], {})
            parsed_operation_data['url'] = url
            parsed_operation_data['method'] = method.upper()

            parsed_query_parameter_data_list = parsed_operation_data.setdefault('query_parameters', {})
            parsed_path_parameter_data_list = parsed_operation_data.setdefault('path_parameters', {})
            parsed_response_data_list = parsed_operation_data.setdefault('responses', {})

            if 'parameters' in method_data:
                for parameter_data in method_data['parameters']:
                    if '$ref' in parameter_data:
                        ref: str = parameter_data['$ref']
                        ref = ref.rsplit('/', maxsplit=1)[1]
                        parameter_data = data['components']['parameters'][ref]
                    parameter_data: dict = deepcopy(parameter_data)

                    if parameter_data['in'] == 'query':
                        parsed_parameter_data = parsed_query_parameter_data_list.setdefault(parameter_data['name'], {})
                    elif parameter_data['in'] == 'path':
                        parsed_parameter_data = parsed_path_parameter_data_list.setdefault(parameter_data['name'], {})
                    else:
                        raise ParseError('parameter data in')
                    parsed_parameter_data['required'] = parameter_data.setdefault('required', False)
                    parsed_parameter_data['default'] = parameter_data.setdefault('default', None)
                    schema_data = parameter_data['schema']
                    parsed_parameter_data['type'] = parse_type(schema_data['type'])
                    if parsed_parameter_data['type'] == 'list':
                        parsed_parameter_data['item_type'] = parse_type(schema_data['items']['type'])

            if 'responses' in method_data:
                for status_code, response_data in method_data['responses'].items():
                    if 'application/json' in response_data['content']:
                        parsed_response_data = parsed_response_data_list.setdefault(status_code, {})
                        response_type = parse_type(response_data['content']['application/json']['schema']['$ref'])
                        parsed_response_data['type'] = response_type
                    elif 'application/hal+json' in response_data['content']:
                        parsed_response_data = parsed_response_data_list.setdefault(status_code, {})
                        response_type = parse_type(response_data['content']['application/hal+json']['schema']['$ref'])
                        parsed_response_data['type'] = response_type
                    else:
                        logger.warning(f'Could not parse response: {url}, {method}, {status_code}')
    return parsed_operations


def module_to_class_name(name: str):
    result = [name[0].upper()]
    upper_flag = False
    for char in name[1:]:
        if char == '_':
            upper_flag = True
            continue
        if upper_flag:
            result.append(char.upper())
            upper_flag = False
        else:
            result.append(char)
    return ''.join(result)


def render(module: str, data: dict, template: Template = None):
    class_name = module_to_class_name(module)
    if template is None:
        template_path = path.join(path.dirname(path.abspath(__file__)), 'api.pyt') if template is None else template
        with open(template_path, 'r', encoding='utf-8') as f:
            template = Template(f.read())
    return template.render(
        class_name=class_name,
        dict_components=stage_1_dict_components(data),
        list_components=stage_2_list_components(data),
        alias_components=stage_3_alias_components(data),
        parameters=stage_4_parameters(data),
        ref_components=stage_5_ref_components(data),
        operations=stage_6_operations(data),
    )
