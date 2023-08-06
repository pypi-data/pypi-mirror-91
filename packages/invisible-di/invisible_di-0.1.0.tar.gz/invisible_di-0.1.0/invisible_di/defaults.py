from typing import Callable, List, Optional, Any
import inspect
from dataclasses import dataclass, field
from .interface import ContainerInterface, Dependable, _Dependable, Actionable


AutoResolverGenerator = Callable[[Dependable], Callable]


def default_auto_resolver_generator(rid: Dependable) -> Callable:
    def auto_resolver(container: ContainerInterface, *args, **kwargs):
        return container.call(action=rid, *args, **kwargs)

    return auto_resolver


AliasWriter = Callable[[_Dependable, List[_Dependable]], None]


def default_alias_writer(rid: Dependable, aliases: List[Dependable]) -> None:
    if isinstance(rid, type):
        aliases.append('{}.{}'.format(rid.__module__, rid.__qualname__))

    aliases.append(rid)


@dataclass
class ArgumentAnnotation:
    name: str
    has_annotation: bool = False
    annotation: Optional[Dependable] = None
    has_default: bool = False
    default: Optional[Any] = None


@dataclass
class ActionableAnnotations:
    arguments: List[ArgumentAnnotation] = field(default_factory=list)
    has_kwargs: bool = False


AnnotationResolver = Callable[[Actionable], ActionableAnnotations]


def default_annotation_resolver(action: Actionable) -> ActionableAnnotations:
    args_spec = inspect.getfullargspec(action)

    offset = len(args_spec.args or []) - len(args_spec.defaults or [])

    result = ActionableAnnotations(has_kwargs=bool(args_spec.varkw))

    for index, argument_name in enumerate(args_spec.args):
        if argument_name == 'self':
            continue

        aa = ArgumentAnnotation(name=argument_name)

        if argument_name in args_spec.annotations:
            aa.has_annotation = True
            aa.annotation = args_spec.annotations[argument_name]

        if index >= offset:
            aa.has_default = True
            aa.default = args_spec.defaults[index-offset]

        result.arguments.append(aa)

    return result
