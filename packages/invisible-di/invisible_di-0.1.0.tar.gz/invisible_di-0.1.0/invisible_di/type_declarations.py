from typing import Optional, List, Dict, Callable, Any, Union

RegistrationID = Union[str, type, Callable]
ResolverCache = Optional[object]
Aliases = List[RegistrationID]
OptionalAliases = Optional[Aliases]
SuggestedArguments = Optional[Dict[str, Any]]
SuggestedArgumentAliases = Optional[Dict[str, str]]
