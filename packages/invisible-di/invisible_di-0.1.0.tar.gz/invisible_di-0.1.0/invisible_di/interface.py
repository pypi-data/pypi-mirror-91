from typing import Optional, List, Dict, Callable, Any, Tuple, Union

Dependable = Union[str, type]
_Dependable = Union[Dependable, Callable]
Actionable = Union[type, Callable]
Arguments = Dict[str, Any]
ArgumentAliasMap = Dict[str, Dependable]
AdditionalResolver = Callable[..., Tuple[bool, Any]]


class ContainerInterface:
    def register(
            self,
            target: Optional[Dependable] = None,
            singleton: bool = False,
            aliases: Optional[List[Dependable]] = None,
    ) -> Optional[Callable]:
        pass

    def get(self, rid: Dependable, *args, **kwargs):
        pass

    def call(
            self,
            action: Actionable,
            suggested_arguments: Optional[Arguments] = None,
            suggested_aliases: Optional[ArgumentAliasMap] = None,
            additional_resolver: Optional[Callable] = None,
            *args, **kwargs,
    ) -> Any:
        pass
