"""
This file contains all the information required to get all the tools and data_types for all
the extension available to Janis! It will put them in a "TaggedRegistry" object, where you can
access a tool by it's name (with optional version).

You should be able to get all the tools + versions.
"""


from typing import Dict, List, Generic, TypeVar, Optional

from janis_core.utils.logger import Logger


class RegistryException(Exception):
    pass


T = TypeVar("T")


class Registry(Generic[T]):
    def __init__(self):
        self.registry: Dict[str, T] = {}

    def register(self, name: str, obj: T):
        if name in self.registry:
            return False
        self.registry[name] = obj
        return True

    def objects(self) -> List[T]:
        return list(self.registry.values())

    def get(self, type_name) -> Optional[T]:
        return self.registry.get(type_name)

    def __contains__(self, item):
        return item in self.registry


class TaggedRegistry(Generic[T]):
    def __init__(self, default_tag):

        self.registry: Dict[str, Dict[str, T]] = {}
        self.default_tag = default_tag
        # We'll specifically make registry[name]["latest"] = (obj: T, version: Comparable)

    def tag_or_default(self, tag):
        return tag if tag is not None else self.default_tag

    def register(self, name: str, tag: Optional[str], obj: T):

        d = self.registry.get(name) if name in self.registry else {}

        # We handle the default tag differently, so make sure the tag isn't
        # the default tag either.
        if tag is not None and tag != self.default_tag:
            if tag in d:
                return False
            d[tag] = obj

            if self.default_tag in d:
                prev, prev_tag = d[self.default_tag]
                if prev_tag is None or tag > prev_tag:
                    d[self.default_tag] = (obj, tag)
            else:
                d[self.default_tag] = (obj, tag)

        elif self.default_tag not in d:
            d[self.default_tag] = (obj, None)

        self.registry[name] = d
        return True

    def objects(self) -> List[List[T]]:
        return list(
            [
                list(y for y in x.values() if not isinstance(y, tuple))
                for x in self.registry.values()
            ]
        )

    def get(self, type_name, tag: Optional[str]) -> Optional[T]:
        if type_name not in self.registry:
            return None
        tagged_objs = self.registry[type_name]
        versions_without_default = set(tagged_objs.keys())
        if self.default_tag in versions_without_default:
            versions_without_default.remove(self.default_tag)

        Logger.debug(
            f"'{type_name}' has {len(versions_without_default)} versions ({', '.join(versions_without_default)})"
        )
        if tag is None or tag == self.default_tag:
            if self.default_tag in tagged_objs:
                Logger.info(
                    f"Using the default tag for '{type_name}' from {len(versions_without_default)} version(s): {', '.join(versions_without_default)}"
                )
                return tagged_objs.get(self.default_tag)[0]
            return None

        if tag not in tagged_objs:
            Logger.log(
                "Found collection '{tool}' in registry, but couldn't find tag '{tag}'".format(
                    tool=type_name, tag=tag
                )
            )
            return None

        return tagged_objs[tag]

    def __contains__(self, item):
        return item in self.registry
