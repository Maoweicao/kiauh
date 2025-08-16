from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Literal
StatusText = Literal[translate('installed_7bb440'), translate('not_installed_1aab9f'), 'Incomplete']
StatusCode = Literal[0, 1, 2]
StatusMap: Dict[StatusCode, StatusText] = {0: translate('not_installed_1aab9f'), 1: 'Incomplete', 2: translate('installed_7bb440')}

@dataclass
class ComponentStatus:
    status: StatusCode
    owner: str | None = None
    repo: str | None = None
    repo_url: str | None = None
    branch: str = ''
    local: str | None = None
    remote: str | None = None
    instances: int | None = None