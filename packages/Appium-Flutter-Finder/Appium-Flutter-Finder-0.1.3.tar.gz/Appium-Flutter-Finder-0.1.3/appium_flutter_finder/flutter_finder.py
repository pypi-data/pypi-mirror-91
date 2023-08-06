import base64
import json

from appium.webdriver.webelement import WebElement

def _bytes(value):
    try:
        return bytes(value, 'UTF-8')  # Python 3
    except TypeError:
        return value  # Python 2


class FlutterElement(WebElement):
    def __init__(self, driver, element_id):
        super(FlutterElement, self).__init__(
            driver, element_id, w3c=True
        )


class FlutterFinder(object):
    def by_ancestor(self, serialized_finder, matching, match_root=False):
        return self._by_ancestor_or_descendant(
            type_='Ancestor',
            serialized_finder=serialized_finder,
            matching=matching,
            match_root=match_root
        )

    def by_descendant(self, serialized_finder, matching, match_root=False):
        return self._by_ancestor_or_descendant(
            type_='Descendant',
            serialized_finder=serialized_finder,
            matching=matching,
            match_root=match_root
        )

    def by_semantics_label(self, label, isRegExp=False):
        return self._serialize(dict(
            finderType='BySemanticsLabel',
            isRegExp=isRegExp,
            label=label
        ))

    def by_tooltip(self, text):
        return self._serialize(dict(
            finderType='ByTooltipMessage',
            text=text
        ))

    def by_text(self, text):
        return self._serialize(dict(
            finderType='ByText',
            text=text
        ))

    def by_type(self, type_):
        return self._serialize(dict(
            finderType='ByType',
            type=type_
        ))

    def by_value_key(self, key):
        return self._serialize(dict(
            finderType='ByValueKey',
            keyValueString=key,
            keyValueType='String' if isinstance(key, str) else 'int'
        ))

    def page_back(self):
        return self._serialize(dict(
            finderType='PageBack'
        ))

    def _serialize(self, finder_dict):
        return base64.b64encode(_bytes(json.dumps(finder_dict))).decode('UTF-8')

    def _by_ancestor_or_descendant(self, type_, serialized_finder, matching, match_root=False):
        param = dict(finderType=type_, matchRoot=match_root)

        try:
            finder = json.dumps(base64.b64decode(serialized_finder))
        except:
            finder = dict()
        for finder_key, finder_value in finder.items():
            param['of_{}'.format(finder_key)] = finder_value

        try:
            matching = json.dumps(base64.b64decode(matching))
        except:
            matching = dict()
        for matching_key, matching_value in matching.items():
            param['matching_{}'.format(matching_key)] = matching_value

        return self._serialize(param)
