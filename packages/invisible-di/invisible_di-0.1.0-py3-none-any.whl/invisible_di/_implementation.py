from typing import Dict, Optional, List, Callable, Any, get_args
from dataclasses import dataclass
from .interface import ContainerInterface, Dependable, _Dependable, Actionable, Arguments, ArgumentAliasMap, \
    AdditionalResolver
from .defaults import \
    AutoResolverGenerator, default_auto_resolver_generator, \
    AliasWriter, default_alias_writer, \
    AnnotationResolver, default_annotation_resolver


@dataclass
class Registration:
    resolver: Optional[Callable] = None
    singleton: bool = False
    cache: Optional[Any] = None

    def resolve(self, container: ContainerInterface, *args, **kwargs):
        if self.cache is not None:
            return self.cache

        result = container.call(self.resolver, *args, **kwargs)

        if self.singleton:
            self.cache = result

        return result


class Container(ContainerInterface):
    _registry: Dict[_Dependable, Registration]

    def __init__(
            self,
            auto_resolver_generator: Optional[AutoResolverGenerator] = None,
            alias_writer: Optional[AliasWriter] = None,
            annotation_resolver: Optional[AnnotationResolver] = None,
    ):
        self._auto_resolver_generator = auto_resolver_generator or default_auto_resolver_generator
        self._alias_writer = alias_writer or default_alias_writer
        self._annotation_resolver = annotation_resolver or default_annotation_resolver

        registration = Registration(singleton=True, cache=self)

        self._registry = {
            ContainerInterface: registration,
            Container: registration,
        }

    def register(
            self,
            target: Optional[Dependable] = None,
            singleton: bool = False,
            aliases: Optional[List[Dependable]] = None,
    ) -> Optional[Callable]:
        if aliases is None:
            aliases = []

        if target:
            return self._register_target(target, singleton, aliases)

        return self._generate_decorator(singleton, aliases)

    def _register_target(self, target: Dependable, singleton: bool, aliases: List[Dependable]) -> None:
        if not isinstance(target, type):
            raise TypeError('If target is defined then it has to be an type')

        self._alias_writer(target, aliases)

        registration = Registration(resolver=self._auto_resolver_generator(target), singleton=singleton)

        for alias in aliases:
            self._registry[alias] = registration

        return None

    def _generate_decorator(self, singleton: bool, aliases: List[Dependable]):
        def decorator(resolver):
            registration = Registration(resolver=resolver, singleton=singleton)

            if not resolver.__annotations__ or 'return' not in resolver.__annotations__.keys():
                raise TypeError('Function MUST typehint a return type')

            self._alias_writer(resolver.__annotations__['return'], aliases)

            if resolver.__qualname__ != '_':
                aliases.append(resolver.__qualname__)

            for alias in (resolver, *aliases):
                self._registry[alias] = registration

            def wrapper(*args, **kwargs):
                return self.get(rid=resolver, *args, **kwargs)

            return wrapper

        return decorator

    def get(self, rid: Dependable, *args, **kwargs):
        if not isinstance(rid, get_args(Dependable)):
            raise TypeError(f'RID {rid!r} is not a valid dependable')

        if isinstance(rid, type) and rid.__module__ == 'builtins':
            raise TypeError(f'Cannot resolve builtins!')

        if rid not in self._registry:
            aliases: List[Dependable] = []
            self._alias_writer(rid, aliases)

            resolver = self._auto_resolver_generator(rid)

            for alias in aliases:
                self._registry[alias] = Registration(resolver=resolver)

        return self._registry[rid].resolve(self, *args, **kwargs)

    def call(
            self,
            action: Actionable,
            suggested_arguments: Optional[Arguments] = None,
            suggested_aliases: Optional[ArgumentAliasMap] = None,
            additional_resolver: Optional[AdditionalResolver] = None,
            *args, **kwargs,
    ) -> Any:
        suggested_arguments = suggested_arguments or {}
        suggested_aliases = suggested_aliases or {}

        annotations = self._annotation_resolver(action)

        arguments: Dict[str, Any] = {}
        for annotated_argument in annotations.arguments:
            if annotated_argument.name in suggested_arguments:
                arguments[annotated_argument.name] = suggested_arguments[annotated_argument.name]
                continue

            if annotated_argument.name in kwargs:
                arguments[annotated_argument.name] = kwargs[annotated_argument.name]
                continue

            if annotated_argument.name in suggested_aliases:
                arguments[annotated_argument.name] = self.get(suggested_aliases[annotated_argument.name])
                continue

            if annotated_argument.has_annotation and additional_resolver:
                has_result, result = self.call(
                    action=additional_resolver,
                    name=annotated_argument.name,
                    rid=annotated_argument.annotation,
                )

                if has_result:
                    arguments[annotated_argument.name] = result
                    continue

            if annotated_argument.has_default:
                arguments[annotated_argument.name] = annotated_argument.default
                continue

            if not annotated_argument.has_annotation:
                raise RuntimeError(f'Argument `{annotated_argument.name}` does not have a type hint and no suggested '
                                   f'value was provided. Container cannot resolve dependency!')

            arguments[annotated_argument.name] = self.get(annotated_argument.annotation)

        if annotations.has_kwargs:
            arguments = {**kwargs, **suggested_arguments, **arguments}

            for alias_argument, alias_dependable  in suggested_aliases.items():
                if alias_argument in arguments:
                    continue

                arguments[alias_argument] = self.get(alias_dependable)

        return action(*args, **arguments)
