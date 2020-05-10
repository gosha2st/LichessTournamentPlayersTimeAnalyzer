#Lichess Tournament Players' Time Analyzer
#by @gosha2st
#v1 created on 20200510

#This python script takes [*.pgn] tournament file with all games played in a tournament; and returns the list with:
# 1) usernames of everyone who participated in the tournament;
# 2) number of games they played;
# 3) amount of time they spent on actual playing (calculated based on games duration);
#in a separate [*.txt] file created in the same folder with the script; sorted by the last (third) parameter decreasing.

#This script is expected to work with all time controls and any increments.
#Berserk mode is handled properly.
#No external python modules needed.

#You need to specify only the input [*.pgn] tournament file, located in the same folder with this script:
#This file can be retrieved by an http-request:
#http://lichess.org/api/tournament/**tournament_id**/games?clocks=true
#For example: http://lichess.org/api/tournament/QEoFNbGg/games?clocks=true
input_tournament_pgn = 'lichess_tournament_2020.05.02_QEoFNbGg_streamers-battle.pgn'

file=open(input_tournament_pgn)
#number of seconds per game for each player defined by the tournament's standings:
#(will be retrieved from the input file by the script automatically):
secs_per_game = -1
dictime={}                  #dictionary data structure with players' names as keys and their time played as values
#dictionary data structure with players' names as keys and number of games they played as values:
dicnumgames={}
#number of games in the tournament taken into account by the script with at least 2 full moves played:
num_games = 0

line = file.readline()    #read the first line of the input file
while(line != ''):        #while not the end of the input file:
    #
    if(line[:8] == '''[White "'''):
        whiteplayer = line[8 : len(line)-3]       #save player who had white pieces in this game
        line=file.readline()
        blackplayer = line[8 : len(line)-3]       #save player who had black pieces in this game
    #
    if((secs_per_game == -1) and (line[:14] == '''[TimeControl "''')):
        plus_pos = line.find('+')
        #assign default number of seconds per game for each player in the tournament:
        secs_per_game = int(line[14 : plus_pos])
        secs_inc = int(line[plus_pos+1 : len(line)-3])      #assign default seconds increment
    #
    if((line[:3]=='1. ') and (len(line)>100)):      #if at least 2 full moves played in the game, analyze it:
        num_games += 1
        #
        start = line.find(':') + 1
        #starting time for white in seconds:
        white_start_time = int(line[start : start+2]) * 60 + int(line[start+3 : start+5])
        #
        subline = line[37:45]
        start = subline.find(':') + 1
        #starting time for black in seconds:
        black_start_time = int(subline[start : start+2]) * 60 + int(subline[start+3 : start+5])
        #
        subline = line[len(line)-65:]
        start = subline.find('.') - 2
        num_moves = int(subline[start : start+2]) - 1       #number of full moves played in the game
        #
        start = subline.find('%clk') + 7
        subline = subline[start:]
        if(subline.find('.') == -1):    #if '.' is in the sub-string (right after move number), then the first time is for white:
            white_end_time = int(subline[:2])*60 + int(subline[3:5])        #end time for white in seconds
            turn='b'    #next turn
        else:
            black_end_time = int(subline[:2])*60 + int(subline[3:5])        #end time for black in seconds
            turn='w'
        start=subline.find('%clk')+7        #find next (second) time
        subline=subline[start:]
        if(turn=='b'):
            black_end_time = int(subline[:2])*60 + int(subline[3:5])
        else:
            white_end_time = int(subline[:2])*60 + int(subline[3:5])
        #
        #calculate increment coefficient depending on whether Berserk was chosen by players:
        coeff = 0
        if(secs_per_game == white_start_time):      #if white didn't take Berserk:
            coeff += 1
        if(secs_per_game == black_start_time):      #if black didn't take Berserk:
            coeff += 1
        #
        #duration of the game analyzed:
        gamedur = white_start_time + black_start_time - white_end_time - black_end_time
        gamedur += secs_inc * num_moves * coeff
        #
        #add game duration for both white and black players to their played time:
        #and update the number of games they played:
        if(dictime.get(whiteplayer, 0) == 0):       #if whiteplayer not in the dictionary:
            dictime[whiteplayer] = gamedur
            dicnumgames[whiteplayer] = 1
        else:
            dictime[whiteplayer] += gamedur
            dicnumgames[whiteplayer] += 1
        if(dictime.get(blackplayer, 0) == 0):
            dictime[blackplayer] = gamedur
            dicnumgames[blackplayer] = 1
        else:
            dictime[blackplayer] += gamedur
            dicnumgames[blackplayer] += 1
    line=file.readline()        #read next file line

file.close()

#get list of all players sorted by the time they played in decreasing order:
names = sorted(dictime, key=dictime.get, reverse=True)

#create output file:
output_file_name = 'LichessTournament_' + str(secs_per_game//60) + '+' + str(secs_inc) + '_PlayersTime.txt'
file = open(output_file_name, 'w')
for name in names:
    file.write(name + '\nGames played:\t' + str(dicnumgames[name]) + '\nTime spent playing:\t' +
               str(dictime[name]//3600) + ' hour ' + str((dictime[name]%3600)//60) + ' minutes\n\n')
file.close()

print(num_games, ' games were analyzed.\nSee results in "', output_file_name, '"', sep='')
