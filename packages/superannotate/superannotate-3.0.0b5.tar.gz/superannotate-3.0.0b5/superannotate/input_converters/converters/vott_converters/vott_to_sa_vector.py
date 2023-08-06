import json
import numpy as np


def _create_classes(classes_map):
    classes_loader = []
    for key in classes_map:
        color = np.random.choice(range(256), size=3)
        hexcolor = "#%02x%02x%02x" % tuple(color)
        sa_classes = {'name': key, 'color': hexcolor, 'attribute_groups': []}
        classes_loader.append(sa_classes)
    return classes_loader


def vott_object_detection_to_sa_vector(file_list):
    sa_jsons = {}
    classes = []
    for json_file in file_list:
        json_data = json.load(open(json_file))
        file_name = json_data['asset']['name'] + '___objects.json'

        instances = json_data['regions']
        sa_loader = []
        for instance in instances:
            for tag in instance['tags']:
                classes.append(tag)
            sa_obj = {
                'className': instance['tags'][0],
                'attributes': [],
                'probability': 100,
                'locked': False,
                'visible': True,
                'groupId': 0
            }
            if instance['type'] == 'RECTANGLE' or instance['type'] == 'POLYGON':
                sa_obj['type'] = 'bbox'
                sa_obj['points'] = {
                    'x1':
                        instance['boundingBox']['left'],
                    'y1':
                        instance['boundingBox']['top'],
                    'x2':
                        instance['boundingBox']['left'] +
                        instance['boundingBox']['width'],
                    'y2':
                        instance['boundingBox']['top'] +
                        instance['boundingBox']['height'],
                }
                sa_loader.append(sa_obj.copy())

        sa_jsons[file_name] = sa_loader

    sa_classes = _create_classes(set(classes))
    return sa_jsons, sa_classes


def vott_instance_segmentation_to_sa_vector(file_list):
    sa_jsons = {}
    classes = []
    for json_file in file_list:
        json_data = json.load(open(json_file))
        file_name = json_data['asset']['name'] + '___objects.json'

        instances = json_data['regions']
        sa_loader = []
        for instance in instances:
            classes.append(instance['tags'][0])
            for tag in instance['tags']:
                classes.append(tag)

            sa_obj = {
                'className': instance['tags'][0],
                'attributes': [],
                'probability': 100,
                'locked': False,
                'visible': True,
                'groupId': 0
            }
            if instance['type'] == 'POLYGON':
                sa_obj['type'] = 'polygon'
                sa_obj['points'] = []
                for point in instance['points']:
                    sa_obj['points'].append(point['x'])
                    sa_obj['points'].append(point['y'])
                sa_loader.append(sa_obj.copy())

        sa_jsons[file_name] = sa_loader

    sa_classes = _create_classes(set(classes))
    return sa_jsons, sa_classes


def vott_to_sa(file_list):
    sa_jsons = {}
    classes = []
    for json_file in file_list:
        json_data = json.load(open(json_file))
        file_name = json_data['asset']['name'] + '___objects.json'

        instances = json_data['regions']
        sa_loader = []
        for instance in instances:
            classes.append(instance['tags'][0])
            for tag in instance['tags']:
                classes.append(tag)

            sa_obj = {
                'className': instance['tags'][0],
                'attributes': [],
                'probability': 100,
                'locked': False,
                'visible': True,
                'groupId': 0
            }
            if instance['type'] == 'RECTANGLE':
                sa_obj['type'] = 'bbox'
                sa_obj['points'] = {
                    'x1':
                        instance['boundingBox']['left'],
                    'y1':
                        instance['boundingBox']['top'],
                    'x2':
                        instance['boundingBox']['left'] +
                        instance['boundingBox']['width'],
                    'y2':
                        instance['boundingBox']['top'] +
                        instance['boundingBox']['height'],
                }
                sa_loader.append(sa_obj.copy())
            elif instance['type'] == 'POLYGON':
                sa_obj['type'] = 'polygon'
                sa_obj['points'] = []
                for point in instance['points']:
                    sa_obj['points'].append(point['x'])
                    sa_obj['points'].append(point['y'])
                sa_loader.append(sa_obj.copy())

        sa_jsons[file_name] = sa_loader

    sa_classes = _create_classes(set(classes))
    return sa_jsons, sa_classes
