import csv
import json
from collections import Counter
from pathlib import Path


ipl_dir = Path(__file__).parent

def convert_csv_to_json(file_name):
    with (ipl_dir / "dataSets" / f"{file_name}.csv").open(
        newline="", encoding="utf-8"
    ) as file:
        return list(csv.DictReader(file))

def run_function(func):
    file_name = func.__name__
    result_file = ipl_dir / "solutions" / f"{file_name}.json"
    result = func()
    with result_file.open("w", encoding="utf-8") as file:
            json.dump(result, file, indent=4)
    return result

matches = convert_csv_to_json('matches')
deliveries = convert_csv_to_json('deliveries')

@run_function
def matchesPlayedPerYear():
    counts = Counter(match['season'] for match in matches)
    return counts

@run_function
def matchesWonPerTeamPerYear():

    counts = Counter((match['winner'], match['season']) for match in matches)
    dist = {}
    for (winner, season), count in counts.items():
        dist.setdefault(winner, {})[season] = count

    """
        dist = {}
        for match in matches:
        winner = match['winner']
        if winner not in dist:
            dist[winner] = {}
        season = match['season']
        if season not in dist[winner]:
            dist[winner][season] = 1
        else:
            dist[winner][season] += 1
    """

    return dist


@run_function
def runsConcededPerTeamInTheYear2016():
    obj = Counter(
        (delivery['bowling_team'], int(delivery['extra_runs']))
        for delivery in deliveries
        if delivery['match_id'] in {
         match['id'] for match in matches if match['season'] == '2016'
      }
    )

    runs_conceded = {}
    for (bowling_team, runs), count in obj.items():
        runs_conceded[bowling_team] = runs_conceded.get(bowling_team, 0) + runs * count
                
    return runs_conceded


