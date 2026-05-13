import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


CRICBUZZ_LIVE_BASE_URL = "https://cricbuzz-live.vercel.app"
REQUEST_TIMEOUT_SECONDS = 12


class LiveMatchAPIError(Exception):
    """Raised when live cricket data cannot be fetched or parsed."""


@dataclass
class LiveScoreSnapshot:
    match_id: str
    title: str
    status: str
    batting_team: str | None
    bowling_team: str | None
    score: int
    wickets: int
    overs: float
    current_run_rate: float
    required_run_rate: float
    target: int | None
    striker: str | None
    non_striker: str | None
    bowler: str | None
    partnership: str | None
    fetched_at: datetime
    raw: dict

    @property
    def balls_completed(self):
        completed_overs = int(self.overs)
        legal_balls = round((self.overs - completed_overs) * 10)
        return completed_overs * 6 + legal_balls

    @property
    def balls_left(self):
        return max(120 - self.balls_completed, 0)

    @property
    def wickets_left(self):
        return max(10 - self.wickets, 0)

    def to_dict(self):
        return {
            "match_id": self.match_id,
            "title": self.title,
            "status": self.status,
            "batting_team": self.batting_team,
            "bowling_team": self.bowling_team,
            "score": self.score,
            "wickets": self.wickets,
            "overs": self.overs,
            "current_run_rate": self.current_run_rate,
            "required_run_rate": self.required_run_rate,
            "target": self.target,
            "striker": self.striker,
            "non_striker": self.non_striker,
            "bowler": self.bowler,
            "partnership": self.partnership,
            "balls_left": self.balls_left,
            "wickets_left": self.wickets_left,
            "fetched_at": self.fetched_at.isoformat(),
        }


def _request_json(path, query=None):
    url = f"{CRICBUZZ_LIVE_BASE_URL}{path}"
    if query:
        url = f"{url}?{urlencode(query)}"

    request = Request(
        url,
        headers={
            "User-Agent": "IPL-AI-Analytics/1.0",
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            payload = response.read().decode("utf-8")
            return json.loads(payload)
    except HTTPError as exc:
        raise LiveMatchAPIError(f"Live API returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise LiveMatchAPIError("Live API is unavailable. Please try again later.") from exc
    except json.JSONDecodeError as exc:
        raise LiveMatchAPIError("Live API returned an invalid JSON response.") from exc


def fetch_live_matches(match_type="league"):
    """Fetch live matches from the unofficial Cricbuzz live endpoint."""
    payload = _request_json(
        "/v1/matches/live",
        query={
            "type": match_type,
        },
    )
    matches = payload.get("data", {}).get("matches", [])

    if not isinstance(matches, list):
        raise LiveMatchAPIError("Live matches response did not contain a match list.")

    return matches


def fetch_match_score(match_id):
    """Fetch live score details for one match id."""
    payload = _request_json(f"/v1/score/{match_id}")
    data = payload.get("data")

    if not isinstance(data, dict):
        raise LiveMatchAPIError("Live score response did not contain score data.")

    return data


def parse_live_score(match_id, score_payload):
    """Normalize an unofficial Cricbuzz score payload into a stable snapshot."""
    live_score = score_payload.get("liveScore") or score_payload.get("score") or ""
    score_data = _parse_score_line(live_score)
    title = score_payload.get("title", "Live Match")
    status = score_payload.get("update") or score_payload.get("status") or "Live"
    teams = _parse_teams_from_title(title)

    current_run_rate = _parse_float(
        score_payload.get("runRate")
        or score_payload.get("currentRunRate")
        or score_payload.get("crr")
    )
    if current_run_rate == 0 and score_data["overs"] > 0:
        current_run_rate = round(score_data["score"] / score_data["overs"], 2)

    runs_needed = _parse_runs_needed(status)
    target = _parse_target(status)
    if target is None and runs_needed is not None:
        target = score_data["score"] + runs_needed
    required_run_rate = _parse_required_rate(status)
    batting_team = score_data["team"] or score_payload.get("battingTeam")
    bowling_team = _infer_bowling_team(batting_team, teams)

    return LiveScoreSnapshot(
        match_id=str(match_id),
        title=title,
        status=status,
        batting_team=batting_team,
        bowling_team=bowling_team,
        score=score_data["score"],
        wickets=score_data["wickets"],
        overs=score_data["overs"],
        current_run_rate=current_run_rate,
        required_run_rate=required_run_rate,
        target=target,
        striker=score_payload.get("batsmanOne") or score_payload.get("batterone"),
        non_striker=score_payload.get("batsmanTwo") or score_payload.get("battertwo"),
        bowler=score_payload.get("bowlerOne") or score_payload.get("bowlerone"),
        partnership=score_payload.get("partnership"),
        fetched_at=datetime.now(timezone.utc),
        raw=score_payload,
    )


def get_live_score_snapshot(match_id):
    """Fetch and parse one live match score snapshot."""
    score_payload = fetch_match_score(match_id)
    return parse_live_score(match_id, score_payload)


def _parse_score_line(score_line):
    pattern = r"(?P<team>.+?)\s+(?P<score>\d+)\/(?P<wickets>\d+)\s+\((?P<overs>\d+(?:\.\d+)?)"
    match = re.search(pattern, score_line)

    if not match:
        return {
            "team": None,
            "score": 0,
            "wickets": 0,
            "overs": 0.0,
        }

    return {
        "team": match.group("team").strip(),
        "score": int(match.group("score")),
        "wickets": int(match.group("wickets")),
        "overs": float(match.group("overs")),
    }


def _parse_teams_from_title(title):
    title = title.split(",")[0]

    if " vs " not in title:
        return []

    return [team.strip() for team in title.split(" vs ", maxsplit=1)]


def _infer_bowling_team(batting_team, teams):
    if not batting_team or len(teams) != 2:
        return None

    batting_team_normalized = batting_team.strip().lower()

    for team in teams:
        if team.strip().lower() == batting_team_normalized:
            return next(other for other in teams if other != team)

    for team in teams:
        team_normalized = team.strip().lower()
        if batting_team_normalized in team_normalized or team_normalized in batting_team_normalized:
            return next(other for other in teams if other != team)

    return None


def _parse_runs_needed(status):
    match = re.search(r"(?:need|needs)\s+(\d+)\s+runs?", status, flags=re.IGNORECASE)

    if match:
        return int(match.group(1))

    return None


def _parse_target(status):
    target_match = re.search(r"target\s+(\d+)", status, flags=re.IGNORECASE)
    if target_match:
        return int(target_match.group(1))

    return None


def _parse_required_rate(status):
    match = re.search(r"(?:rrr|required rate)[:\s]+(\d+(?:\.\d+)?)", status, flags=re.IGNORECASE)
    if match:
        return float(match.group(1))

    need_match = re.search(
        r"(?:need|needs)\s+(\d+)\s+runs?\s+in\s+(\d+)\s+balls?",
        status,
        flags=re.IGNORECASE,
    )
    if need_match:
        runs = int(need_match.group(1))
        balls = int(need_match.group(2))
        return round((runs * 6) / balls, 2) if balls else 0.0

    return 0.0


def _parse_float(value):
    if value is None:
        return 0.0

    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0
