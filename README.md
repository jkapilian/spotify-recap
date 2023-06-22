# Spotify Data Recap
This program takes Spotify's streaming history data and aggregates it weekly to create a JSON that tracks your listening habits over time by showing the most listened to tracks in a given week. Command line arguments allow you to customize how many songs should show up in your weekly listening ranking.
## Usage
### Obtaining the Data
* Go to https://www.spotify.com/us/account/privacy/ and log in with your account
* Click on either "Your Account Data" or "Prepare Extended streaming history"
  - The Account Data only includes listening history from the past year but takes less time to prepare while the extended streaming history includes data dating back to account creation
* Wait for an email to download account data as a ZIP
### Running the Script
* Clone this repo locally
* Run `python spotify.py -i INPUT -o OUTPUT -c CUTOFF` where
  - `INPUT` is a space-separated list of chronological Spotify data
  - `OUTPUT` is the intended destination of the aggregated data
  - `CUTOFF` is the minimum amount of total listening time of a song across a week to appear in the aggregated data in ms
* For example, if the downloaded data has 2 relevant data files `StreamingHistory0.json` and `StreamingHistory1.json`, the intended output is `Aggregated.json`, and you would like to see any songs listened to for more than 5 minutes in total across a given week (300000 ms), run `python spotify.py -i StreamingHistory0.json StreamingHistory1.json -o Aggregated.json -c 300000`
* Expected output should look like
    "2022-11-07": {
		"Jon Batiste - San Spirito": 580105,
		"Lin-Manuel Miranda - In the Heights": 493102,
		"Lake Street Dive - Stop Your Crying": 491784,
		"Lake Street Dive - Bad Self Portraits": 467641,
		"Lin-Manuel Miranda - 96,000": 441220,
		"Lawrence - Freckles (Live in LA)": 418780,
		"Lake Street Dive - Call off Your Dogs": 410506,
		"Vulfmon - Take Me to a Higher Place": 395122,
		"Lawrence - Try (Live in NYC)": 384333,
		"Karen Olivo - It Won't Be Long Now": 379237,
		"Doreen Montalvo - Finale": 341484,
		"Lawrence - Make A Move (Live in SF)": 335226,
		"Olga Merediz - Paciencia Y Fe": 310868,
		"Couch - Stand Up": 301278
    },
    ...