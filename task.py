import argparse

from src.ranking import CsvParser, CsvWriter, Ranking
from src.tests import Tests


def entrypoint() -> None:
    """Main entry point for the hockey ranker CLI.

    Raises:
        FileNotFoundError: If the input_file argument points to a file that does not exist.
        TypeError: If the input_file argument points to a non-file (eg, a directory).
    """
    parser = argparse.ArgumentParser(
        description="CLI to rank teams from a list of game results"
    )
    parser.add_argument("input_file", help="Location of input CSV")
    parser.add_argument("output_file", help="Location to write output CSV")

    # Parse out the input file
    args = parser.parse_args()

    # Here are your two arguments: the input CSV and the output CSV
    input_file = args.input_file
    output_file = args.output_file

    # Guaranteed input/output files in problem description
    if input_file is None:
        input_file = "input/league-sample-games.csv"
    if output_file is None:
        output_file = "output/expected-output.csv"

    csv_in = CsvParser(file=input_file)
    games = csv_in.parse_input() 

    my_ranking = Ranking(games)
    my_ranking.calculate_points()
    output = my_ranking.get_rankings()

    # Verify output
    tests = Tests(input=games, output=output, sample_input="input/league-sample-games.csv",
        sample_output="output/expected-output.csv")
    status = tests.run_all_tests()
    if len(status) != 0:
        print(status)

    # Write output csv file
    csv_out = CsvWriter(output=output, output_location=output_file)
    csv_out.write_output()


if __name__ == "__main__":
    entrypoint()
