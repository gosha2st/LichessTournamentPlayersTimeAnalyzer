# LichessTournamentPlayersTimeAnalyzer
Python script that takes Lichess tournament [.pgn] file with all games played in a tournament; and returns the list with:

1) usernames of everyone who participated in the tournament;

2) number of games they played;

3) amount of time they spent on actual playing (calculated based on games duration);

in a separate [.txt] file created in the same folder with the script; sorted by the last (third) parameter decreasing.

This script is expected to work with all time controls and any increments.

Berserk mode is handled properly.

No external python modules needed.
# How to use:

You need to specify in the code only the input [.pgn] tournament file.

This file can be retrieved by an http-request: http://lichess.org/api/tournament/**tournament_id**/games?clocks=true.

For example: http://lichess.org/api/tournament/QEoFNbGg/games?clocks=true
