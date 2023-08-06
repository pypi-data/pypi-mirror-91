import datetime
from typing import NamedTuple, Optional, List

if False:  # TYPE_CHECKING
    from we_are_venom.commit import CommitInfo  # noqa: F401


class ModuleAccumulation(NamedTuple):
    module_name: str
    touched_lines: int
    total_lines: Optional[int]
    is_accumulated: Optional[bool]


class Ticket(NamedTuple):
    num: str
    commits: List['CommitInfo']

    @property
    def touched_lines(self) -> int:
        return self.added_lines + self.deleted_lines

    @property
    def added_lines(self) -> int:
        return sum(c.added_lines for c in self.commits)

    @property
    def deleted_lines(self) -> int:
        return sum(c.deleted_lines for c in self.commits)

    @property
    def latest_commit_date(self) -> datetime.datetime:
        return max(c.commit.committed_datetime for c in self.commits)

    @property
    def earliest_commit_date(self) -> datetime.datetime:
        return min(c.commit.committed_datetime for c in self.commits)


class TouchedModuleInfo(NamedTuple):
    added_lines: int
    deleted_lines: int
