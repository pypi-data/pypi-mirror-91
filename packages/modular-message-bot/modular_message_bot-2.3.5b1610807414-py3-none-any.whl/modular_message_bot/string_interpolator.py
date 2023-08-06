import re


class StringInterpolator(object):
    def __init__(self, start: str, end: str):
        self.end = end
        self.start = start

    def interpolate(self, contents: str, replace_key: str, replace_value: str) -> str:
        replacement = self.start + replace_key + self.end
        return contents.replace(replacement, replace_value)

    def get_keys(self, contents: str) -> list:
        start = re.escape(self.start)
        end = re.escape(self.end)

        matches = re.findall(rf"{start}(.*?){end}", contents)
        return matches

    def is_interpolatable(self, contents: str, replace_key: str) -> bool:
        return replace_key in self.get_keys(contents)

    def interpolate_dict(self, dictionary: dict, replace_key: str, replace_value: str) -> dict:
        interpolated_dict = {}
        for key, value in dictionary.items():
            new_key = self.interpolate(key, replace_key, replace_value)
            if isinstance(value, dict):
                interpolated_dict[new_key] = self.interpolate_dict(value, replace_key, replace_value)
            elif isinstance(value, str):
                interpolated_dict[new_key] = self.interpolate(value, replace_key, replace_value)
            else:
                interpolated_dict[new_key] = value
        return interpolated_dict
