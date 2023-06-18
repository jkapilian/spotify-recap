import json
import argparse
from datetime import datetime, timedelta

SPOTIFY_FORMAT = "%Y-%m-%d %H:%M"
STRUCTURE_FORMAT = "%Y-%m-%d"

def rankWeek(currentWeekRank, args):
    ret = {}
    for item in currentWeekRank:
        if currentWeekRank[item] >= args.cutoff:
            ret[item] = currentWeekRank[item]
    # TODO: sort
    return ret

def create_structure(args):
    currentWeek = None
    structure = {}
    currentWeekRank = {}
    for file in args.input:
        f = open(file, "r")
        data = json.loads(f.read())
        for item in data:
            date = datetime.strptime(item["endTime"], SPOTIFY_FORMAT).date()
            week = date + timedelta(days=-date.weekday())
            if week != currentWeek:
                if currentWeek != None:
                    structure[currentWeek.strftime(STRUCTURE_FORMAT)] = rankWeek(currentWeekRank, args)
                currentWeek = week
                currentWeekRank = {}
            formattedName = f'{item["artistName"]} - {item["trackName"]}'
            if formattedName in currentWeekRank:
                currentWeekRank[formattedName] += item["msPlayed"]
            else:
                currentWeekRank[formattedName] = item["msPlayed"]
        f.close()
    
    if currentWeek != None:
        structure[currentWeek.strftime(STRUCTURE_FORMAT)] = rankWeek(currentWeekRank, args)
    
    f = open(args.output, "w")
    f.write(json.dumps(structure))
    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Spotify data")
    parser.add_argument('-i', '--input', nargs='+', default=[], help="Input data files")
    parser.add_argument('-o', '--output', help="Output data file")
    parser.add_argument('-c', '--cutoff', help="Ms cutoff", type=int)
    args = parser.parse_args()
    create_structure(args)