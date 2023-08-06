import datetime
import os
from typing import Tuple

from click import group, option, argument, Path, echo, DateTime
from rich import print

from we_are_venom.utils.accumulation import (
    calclulate_module_accumulation_info,
    calculate_total_accumulation_percent,
)
from we_are_venom.utils.config import load_config_from
from we_are_venom.utils.git import (
    fetch_git_history, aggregate_commits_by_tickets, cherry_pick_tickets,
)
from we_are_venom.utils.output import (
    output_accumulation_table, output_commits, output_review_report,
)
from we_are_venom.utils.review import calculate_total_review_stat


@group()
def cli() -> None:
    pass


@cli.command()  # noqa: CFQ002
@argument('path')
@argument('date_from', type=DateTime())
@argument('date_to', type=DateTime())
@argument('web_base_repo_url')
@option('--min_lines', type=int, default=0)
@option('--module', '-m', 'modules', multiple=True)
@option('--generate_pretty_changesets', is_flag=True, default=False)
@option('--short', is_flag=True, default=False)
@option('--config_file_name', default='setup.cfg')
@option('--config_file_path', type=Path(exists=True, dir_okay=False, resolve_path=True))
def grand_code_review(  # noqa: CFQ002
    path: str,
    date_from: datetime.datetime,
    date_to: datetime.datetime,
    web_base_repo_url: str,
    min_lines: int,
    modules: Tuple[str],
    generate_pretty_changesets: bool,
    short: bool,
    config_file_name: str,
    config_file_path: str,
    max_dates_between_commits: int = 14,
) -> None:
    if not modules:
        config_path = config_file_path or os.path.join(path, config_file_name)
        if not os.path.exists(config_path):
            echo(f'{config_path} does not exists. Please, provide venom config as docs says.')

        config = load_config_from(config_path)
        if not config:
            echo(f'Error loading config from {config_path}.', err=True)
            return
        modules = config['modules']
    commit_regexp = r'^(Revert .+|Merge .+|((\w{3,5})-\d{1,4}): .+)'
    commits = fetch_git_history(
        path,
        date_from=date_from,
        date_to=date_to,
        modules=modules,
        get_extended_commits_info=True,
    )
    all_tickets, orphan_commits = aggregate_commits_by_tickets(commits, commit_regexp)
    tickets = [
        t for t in all_tickets
        if (
            t.touched_lines >= min_lines
            or (t.latest_commit_date - t.earliest_commit_date).days > max_dates_between_commits
        )
    ]
    small_tickets = [t for t in all_tickets if t not in tickets]
    total_stat = calculate_total_review_stat(tickets, small_tickets, orphan_commits)
    pretty_changesets_map = cherry_pick_tickets(tickets) if generate_pretty_changesets else None
    output_review_report(
        tickets,
        pretty_changesets_map,
        total_stat,
        web_base_repo_url,
        short,
    )


@cli.command()
@argument('email')
@argument('path', type=Path(exists=True, file_okay=False, resolve_path=True))
@option('--verbose', is_flag=True, default=False)
@option('--config_file_name', default='setup.cfg')
@option('--config_file_path', type=Path(exists=True, dir_okay=False, resolve_path=True))
def check(
    email: str,
    path: str,
    verbose: bool,
    config_file_name: str,
    config_file_path: str,
) -> None:
    if not os.path.exists(os.path.join(path, '.git')):
        echo(f'{path} is not git root.', err=True)
        return

    config_path = config_file_path or os.path.join(path, config_file_name)
    if not os.path.exists(config_path):
        echo(f'{config_path} does not exists. Please, provide venom config as docs says.')

    config = load_config_from(config_path)
    if not config:
        echo(f'Error loading config from {config_path}.', err=True)
        return

    date_from = datetime.datetime.now() - datetime.timedelta(days=config['history_depth_years'] * 365)
    raw_git_history = [c for c in fetch_git_history(path, date_from=date_from) if c.author.email == email]
    if verbose:
        output_commits(raw_git_history)
    module_accumulation_info = calclulate_module_accumulation_info(raw_git_history, email, config)
    total_accumulation_percent = calculate_total_accumulation_percent(module_accumulation_info)
    output_accumulation_table(module_accumulation_info)
    print(f'[bold]Total accumulation rate: {total_accumulation_percent}%[/bold]')  # noqa: T001


if __name__ == '__main__':
    cli()
