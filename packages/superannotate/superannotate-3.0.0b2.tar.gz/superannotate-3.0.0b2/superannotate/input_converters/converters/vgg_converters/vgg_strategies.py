import json

from .vgg_converter import VGGConverter
from .vgg_to_sa_vector import vgg_object_detection_to_sa_vector, vgg_instance_segmentation_to_sa_vector, vgg_to_sa

from ....common import dump_output


class VGGObjectDetectionStrategy(VGGConverter):
    name = "ObjectDetection converter"

    def __init__(self, args):
        super().__init__(args)
        self.__setup_conversion_algorithm()

    def __setup_conversion_algorithm(self):
        if self.direction == "to":
            raise NotImplementedError("Doesn't support yet")
        else:
            if self.project_type == "Vector":
                if self.task == "object_detection":
                    self.conversion_algorithm = vgg_object_detection_to_sa_vector
                elif self.task == 'instance_segmentation':
                    self.conversion_algorithm = vgg_instance_segmentation_to_sa_vector
                elif self.task == 'vector_annotation':
                    self.conversion_algorithm = vgg_to_sa

    def __str__(self):
        return '{} object'.format(self.name)

    def to_sa_format(self):
        json_data = self.get_file_list()
        id_generator = self._make_id_generator()
        sa_jsons, sa_classes = self.conversion_algorithm(
            json_data, id_generator
        )
        dump_output(self.output_dir, self.platform, sa_classes, sa_jsons)

    def _make_id_generator(self):
        cur_id = 0
        while True:
            cur_id += 1
            yield cur_id
