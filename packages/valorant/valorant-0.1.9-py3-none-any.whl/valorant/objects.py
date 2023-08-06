class DTO(object):
    def __init__(self, obj):
        self.json = obj
        self.set_attributes(obj)

    def __str__(self):
        return str(self.json)

    def __repr__(self):
        return str(self.json)

    def set_attributes(self, attrs, sub=False):
        for attr, value in attrs.items():
            if sub and isinstance(value, dict):
                self.__setattr__(attr, DTO(value))
            else:
                self.__setattr__(attr, value)


class ActDTO(DTO):
    def __init__(self, obj):
        self.json = obj
        self.tagLine = None
        self.gameName = None
        self.set_attributes(obj)

    def __getattribute__(self, name):
        return super(ActDTO, self).__getattribute__(name)


class AccountDTO(DTO):
    def __getattribute__(self, name):
        return super(AccountDTO, self).__getattribute__(name)


class ContentItemDTO(DTO):
    def __getattribute__(self, name):
        return super(ContentItemDTO, self).__getattribute__(name)


class PlatformDataDTO(DTO):
    def __init__(self, obj):
        self.json = obj
        self.set_attributes(obj, sub=True)

    def __getattribute__(self, name):
        return super(PlatformDataDTO, self).__getattribute__(name)


class ContentList(list, object):
    def get(self, name: str, default=None):
        for item in self.copy():
            try:
                if item.name == name:
                    return item
                else: continue
            except AttributeError:
                if item == name:
                    return item
                else:
                    continue

        return default
