import json


class MagicParams:

    def __init__(self, params_as_dict=None, on_missing_param='promt', **kwargs):
        self.on_missing_param = on_missing_param
        if params_as_dict:
            self.copy_from_dict(params_as_dict)

        if kwargs:
            self.copy_from_dict(kwargs)

    def to_dict(self):
        return self.__dict__

    def copy_from_dict(self, params_as_dict=None):
        self.__dict__.update(params_as_dict)
        return self

    def to_json(self, file_path: str = None):
        d = self.to_dict()
        json.dump(d, open(file_path, 'w'))
        return self

    def copy_from_json(self, file_path: str):
        d = json.load(open(file_path, 'r'))
        self.copy_from_dict(d)
        return self

    def copy_from_argparser(self):
        import argparse
        parser = argparse.ArgumentParser()
        for k, v in self.__dict__.items():
            parser.add_argument('--' + k, default=v, required=False)

        known, unknown = parser.parse_known_args()
        self.copy_from_dict(known.__dict__)

        for k, v in zip(unknown[:-1:2], unknown[1::2]):
            self.__dict__[k[2:]] = v

        return self

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        elif self.on_missing_param == 'promt':
            value = input('Enter value for {item}: '.format(item=item))
            self.__dict__[item] = value
            return value

        raise Exception('{item} doenst exists in MagicParams'.format(item=item))

    def __setattr__(self, item, value):
        self.__dict__[item] = value

    def __str__(self):
        return str(self.to_dict())




