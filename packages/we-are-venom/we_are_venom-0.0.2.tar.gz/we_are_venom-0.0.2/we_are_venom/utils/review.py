from typing import List, Mapping, Any

from we_are_venom.commit import CommitInfo
from we_are_venom.common_types import Ticket


def calculate_total_review_stat(
    tickets: List[Ticket],
    small_tickets: List[Ticket],
    orphan_commits: List[CommitInfo],
) -> Mapping[str, Any]:
    commits_in_tickets = sum(len(t.commits) for t in tickets)

    missed_lines = sum(t.touched_lines for t in small_tickets) + sum(c.total_lines for c in orphan_commits)

    total_stat = {
        'commits_in_tickets': commits_in_tickets,
        'loc_touched_in_tickets': sum(t.touched_lines for t in tickets),
        'tickets_amount': len(tickets),
        'avg_lines_per_ticket': int(sum(t.touched_lines for t in tickets) / len(tickets)) if tickets else 0,
        'missed_lines': missed_lines,
    }

    total_stat['period_coverage'] = int(
        total_stat['loc_touched_in_tickets']
        / (total_stat['loc_touched_in_tickets'] + missed_lines)
        * 100,
    )
    return total_stat
