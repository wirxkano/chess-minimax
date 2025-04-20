import argparse

class Utils:
  @staticmethod
  def printUsage():
    # print("Run command: python main.py 1 0 <difficulty>")
    print("Difficulty options: easy, medium, hard")

  @staticmethod
  def chess_label(pos):
    row, col = pos
    letters = 'abcdefgh'
    numbers = '12345678'
    column_label = letters[col]
    row_label = numbers[7 - row]
    return f"{row_label}{column_label}"
  
  @staticmethod
  def parse_arguments():
    parser = argparse.ArgumentParser(description="Run a chess game between players or agents.")
    parser.add_argument('--mode', required=True, choices=['ava', 'pva', 'pvp'],
                        help='Game mode: ava (agent vs agent), pva (player vs agent), pvp (player vs player)')
    parser.add_argument('--first', required=True, choices=['w', 'b'],
                        help='Which side goes first: w (white) or b (black)')
    parser.add_argument('--difficulty', required=True, choices=['easy', 'medium', 'hard'],
                        help='Difficulty level for AI (only used in games with agent)')

    return parser.parse_args()