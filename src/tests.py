# Test output
from src.ranking import CsvParser, Ranking

class Tests:
    def __init__(self, input, output, sample_input, sample_output):
        self.input = input
        self.output = output
        self.sample_input = sample_input
        self.sample_output = sample_output

    def verify_rankings(self):
        rankings = [rank[0] for rank in self.output]
        if rankings != sorted(rankings):
            return False
        return True

    def all_teams_in_output(self):
        team1 = [x[0][:-2] for x in self.input] # Team 1 teams
        team2 = [x[1][:-2] for x in self.input] # Team 2 teams
        teams_input = set(team1 + team2)
        teams_output = set([x[1] for x in self.output])
        if teams_input != teams_output:
            return False
        return True 
    
    def regression_test(self):
        csv_in = CsvParser(self.sample_input).parse_input()
        expected_output = CsvParser(self.sample_output).parse_input()

        my_ranking = Ranking(csv_in)
        my_ranking.calculate_points()
        actual_output = my_ranking.get_rankings()

        if actual_output != expected_output:
            return False

        return True


    def run_all_tests(self):
        status = ''
        if not self.verify_rankings():
            status += '\nRankings do not follow standard competition ranking.'
        if not self.all_teams_in_output():
            status += '\nAll input teams are not present in output.'
        if not self.regression_test():
            status += '\nSample input does not yield sample output in regression test.'
        return status