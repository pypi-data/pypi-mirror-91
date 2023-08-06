import collections
from typing import NamedTuple, Mapping, Iterable, DefaultDict

from git import Commit
from unidiff import PatchSet

from we_are_venom.common_types import TouchedModuleInfo
from we_are_venom.utils.accumulation import _get_file_module


class CommitInfo(NamedTuple):
    commit: Commit
    touched_modules_info: Mapping[str, TouchedModuleInfo]
    raw_diff: str
    patches: PatchSet

    @property
    def total_lines(self) -> int:
        return self.added_lines + self.deleted_lines

    @property
    def added_lines(self) -> int:
        return sum(p.added for p in self.patches)

    @property
    def deleted_lines(self) -> int:
        return sum(p.removed for p in self.patches)

    @staticmethod
    def _get_touched_modules_info(
        patches: PatchSet,
        modules: Iterable[str],
    ) -> Mapping[str, TouchedModuleInfo]:
        added_lines_map: DefaultDict[str, int] = collections.defaultdict(int)
        removed_lines_map: DefaultDict[str, int] = collections.defaultdict(int)
        for changed_file in patches:
            filename = changed_file.path
            module = _get_file_module(filename, modules)
            if not module:
                continue
            added_lines_map[module] += changed_file.added
            removed_lines_map[module] += changed_file.removed
        touched_modules = set(list(added_lines_map.keys()) + list(removed_lines_map.keys()))
        return {
            t: TouchedModuleInfo(
                added_lines=added_lines_map.get(t, 0),
                deleted_lines=removed_lines_map.get(t, 0),
            )
            for t in touched_modules
        }

    @classmethod
    def from_raw_commit(cls, raw_commit: Commit, modules: Iterable[str]) -> 'CommitInfo':
        raw_diff = raw_commit.repo.git.diff(
            raw_commit.tree,
            raw_commit.parents[0] if raw_commit.parents else None,
        )
        patches = PatchSet(raw_diff)
        return CommitInfo(
            commit=raw_commit,
            touched_modules_info=cls._get_touched_modules_info(patches, modules),
            raw_diff=raw_diff,
            patches=patches,
        )
