from enum import Enum


class PyEnumMixin(Enum):

    """
        Verify ids are conseucetive. If there are duplicate ids, then
        ids will be overwritten and there will be holes in the numbers
        Specify __VERIFYIDS__ to starting id
        Specify __SKIPIDS__ as an array of ids to skip over
    """

    @classmethod
    def _build_cache(cls):
        id_to_name = {}
        name_to_id = {}

        for _ in cls:
            id_to_name[_.value] = _.name
            name_to_id[_.name] = _.value

        cls._cache_1 = id_to_name
        cls._cache_2 = name_to_id

    @classmethod
    def num_to_name(cls):
        if not getattr(cls, "_cache_1", None):
            cls._build_cache()
        return cls._cache_1

    @classmethod
    def num_to_friendly_name(cls):
        name_dict = {}
        for num, name in iter(cls.num_to_name().items()):
            name_dict[num] = name.replace("_", " ").title()
        return name_dict

    @classmethod
    def get_titled_name(cls, key):
        return cls.get_name(key).replace("_", " ").title()

    @classmethod
    def get_name(cls, key):
        assert key in cls.num_to_name(), "Not valid key: %s" % key
        return cls.num_to_name()[key]

    @classmethod
    def get_ids(cls):
        return cls.num_to_name().keys()

    @classmethod
    def get_names(cls):
        return cls.num_to_name().values()

    @classmethod
    def is_key(cls, val):
        return val in cls.num_to_name()

    @classmethod
    def is_name(cls, val):
        return val in cls.to_dict()

    @classmethod
    def name_to_num(cls, name):
        if not getattr(cls, "_cache_2", None):
            cls._build_cache()
        return cls._cache_2.get(name)

    @classmethod
    def to_dict(cls):
        if not getattr(cls, "_cache_2", None):
            cls._build_cache()
        return cls._cache_2
