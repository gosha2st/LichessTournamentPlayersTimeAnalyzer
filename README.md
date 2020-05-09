# LichessTournamentPlayersTimeAnalyzer
Python script that takes tournament [.pgn] file with all games played in a tournament, and returns the amount of time each player spent on actual playing (calculated based on games duration) in a separate [.txt] file created in the same folder with the script.

This script is expected to work with all time controls and any increments.

Berserk mode is handled properly.

No external python modules needed.
# How to use:

You need to specify in the code only the input [.pgn] tournament file, located in the same folder with this script.

This file can be retrieved by an http-request: http://lichess.org/api/tournament/**tournament_id**/games?clocks=true.

For example: http://lichess.org/api/tournament/QEoFNbGg/games?clocks=true
