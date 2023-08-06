import datetime
import re
import collections
from typing import Mapping, List, Tuple, Union, Iterable, Dict, Any, overload, Optional, DefaultDict

from git import Repo, Commit
from typing_extensions import Literal

from we_are_venom.common_types import Ticket
from we_are_venom.commit import CommitInfo


@overload
def fetch_git_history(
    path: str,
    get_extended_commits_info: Literal[True],
    date_from: datetime.datetime = None,
    modules: Iterable[str] = None,
    date_to: datetime.datetime = None,
) -> List[CommitInfo]:
    pass


@overload
def fetch_git_history(
    path: str,
    get_extended_commits_info: Literal[False] = False,
    date_from: datetime.datetime = None,
    modules: Iterable[str] = None,
    date_to: datetime.datetime = None,
) -> List[Commit]:
    pass


def fetch_git_history(
    path: str,
    get_extended_commits_info: bool = False,
    date_from: datetime.datetime = None,
    modules: Iterable[str] = None,
    date_to: datetime.datetime = None,
) -> List[Union[Commit, CommitInfo]]:
    repo = Repo(path)
    date_to = date_to or datetime.datetime.now()
    modules = modules or []
    iter_commits_args: Dict[str, Any] = {'no_merges': True}
    if date_from:
        iter_commits_args['since'] = date_from
    if date_to:
        iter_commits_args['until'] = date_to
    raw_commits = list(repo.iter_commits(**iter_commits_args))
    if not get_extended_commits_info:
        return raw_commits
    return [fetch_full_commit_data(c, modules) for c in raw_commits]


def fetch_full_commit_data(raw_commit: Commit, modules: Iterable[str]) -> CommitInfo:
    return CommitInfo.from_raw_commit(raw_commit, modules)


def aggregate_commits_by_tickets(
    commits: List[CommitInfo],
    commit_regexp: str,
) -> Tuple[List[Ticket], List[CommitInfo]]:
    commits_map: DefaultDict[str, List[CommitInfo]] = collections.defaultdict(list)
    orphan_commits = []
    for commit in commits:
        ticket_id = _get_ticket_id(commit.commit.summary, commit_regexp)
        if ticket_id:
            commits_map[ticket_id].append(commit)
        else:
            orphan_commits.append(commit)
    return [Ticket(num=t, commits=c) for (t, c) in commits_map.items()], orphan_commits


def cherry_pick_tickets(tickets: List[Ticket]) -> Mapping[str, Mapping[str, str]]:
    pass


def _get_ticket_id(commit_message: str, commit_regexp: str) -> Optional[str]:
    commit_message = commit_message.split('\n')[0].strip()
    match = re.match(commit_regexp, commit_message)
    return match.groups()[1] if match else None
