import json
import argparse
from datetime import datetime, timedelta

SPOTIFY_FORMAT = "%Y-%m-%d %H:%M"
EXTENDED_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
STRUCTURE_FORMAT = "%Y-%m-%d"

def rankWeek(currentWeekRank, args):
    ret = {}
    for item in currentWeekRank:
        if currentWeekRank[item] >= args.cutoff:
            ret[item] = currentWeekRank[item]
    # creative solution from https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
    return dict(sorted(ret.items(), key=lambda x:x[1], reverse=True))

def create_structure(args):
    currentWeek = None
    structure = {}
    currentWeekRank = {}
    for file in args.input:
        f = open(file, "r")
        data = json.loads(f.read())
        for item in data:
            if args.extended:
                date = datetime.strptime(item["ts"], EXTENDED_FORMAT).date()
            else:
                date = datetime.strptime(item["endTime"], SPOTIFY_FORMAT).date()
            
            week = date + timedelta(days=-date.weekday())
            if week != currentWeek:
                if currentWeek != None:
                    structure[currentWeek.strftime(STRUCTURE_FORMAT)] = rankWeek(currentWeekRank, args)
                currentWeek = week
                currentWeekRank = {}
            
            if args.extended:
                formattedName = f'{item["master_metadata_album_artist_name"]} - {item["master_metadata_track_name"]}'
            else:
                formattedName = f'{item["artistName"]} - {item["trackName"]}'
            
            if formattedName in currentWeekRank:
                currentWeekRank[formattedName] += (item["ms_played"] if args.extended else item["msPlayed"])
            else:
                currentWeekRank[formattedName] = (item["ms_played"] if args.extended else item["msPlayed"])
        f.close()
    
    if currentWeek != None:
        structure[currentWeek.strftime(STRUCTURE_FORMAT)] = rankWeek(currentWeekRank, args)
    
    f = open(args.output, "w")
    f.write(json.dumps(structure))
    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Spotify data")
    parser.add_argument('-i', '--input', nargs='+', default=[], help="Input data files", required=True)
    parser.add_argument('-o', '--output', help="Output data file", required=True)
    parser.add_argument('-c', '--cutoff', help="Ms cutoff", type=int, required=True)
    parser.add_argument('-e', '--extended', help="Whether this is extended history", action="store_true")
    args = parser.parse_args()
    create_structure(args)