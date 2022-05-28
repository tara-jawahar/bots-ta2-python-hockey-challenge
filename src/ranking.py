from collections import defaultdict
import csv

class CsvParser:
    def __init__(self, file):
        self.file = file
    
    def parse_input(self):
        """Use native csv reader to parse input"""
        with open(self.file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            games = [row for row in reader][1:]
        return games

class CsvWriter:
    def __init__(self, output, output_location):
        self.output = output
        self.output_location = output_location

    def write_output(self):
        """Write out csv with header"""
        with open(self.output_location, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Place','Team','Score'])
            for line in self.output:
                writer.writerow(line)

class Ranking:
    def __init__(self, games):
        self.games = games
        self.total_scores = defaultdict(int) # initalize all values to 0
        self.sorted_teams = None
    
    def calculate_points(self):
        """Iterate through games and calculate rank points"""
        for game in self.games:
            team1, team2 = game[0][:-2], game[1][:-2]
            team1_score, team2_score = int(game[0][-1]), int(game[1][-1])
            if team1_score > team2_score: # Team 1 wins
                self.total_scores[team1] += 3
                self.total_scores[team2] += 0
            elif team1_score == team2_score: # Tie
                self.total_scores[team1] += 1
                self.total_scores[team2] += 1
            else: # Team 2 wins
                self.total_scores[team2] += 3
                self.total_scores[team1] += 0
    
    def sort_teams(self):
        """Sort by score and then by alphabetical order"""
        self.sorted_teams = sorted(self.total_scores, reverse=True, 
            key=lambda x: (self.total_scores[x], ord(x[0])*-1))

    def get_pts(self, i):
        """Helper to access a team's points given its index in sorted_teams"""
        return self.total_scores[self.sorted_teams[i]]
        
    def format_pt_vals(self, i):
        """Takes care of singular vs. plural grammatical logic in rankings"""
        pt_val = self.get_pts(i)
        pt_str = ' pt' if pt_val == 1 else ' pts'
        return str(pt_val) + pt_str

    def get_rankings(self):
        """Use rank points to calculate actual rankings, accounting for ties"""
        self.sort_teams()

        if len(self.sorted_teams) == 0:
            return []

        output = []
        cur_ranking = 1
        num_ties = 0

        output += [[str(cur_ranking), self.sorted_teams[0] , self.format_pt_vals(0)]]

        for i in range(1, len(self.sorted_teams)):
            cur_team_pts, prev_team_pts = self.get_pts(i), self.get_pts(i-1)
            if cur_team_pts == prev_team_pts:
                num_ties += 1
                output += [[str(cur_ranking), self.sorted_teams[i], self.format_pt_vals(i)]]
            else:
                cur_ranking += 1 + num_ties # Increment ranking if there were previous ties
                output += [[str(cur_ranking), self.sorted_teams[i], self.format_pt_vals(i)]]
                num_ties = 0

        return output
