RANK = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
SUIT = ["c", "d", "h", "s"]

def generate_starting_hands():
  starting_hands = []
  for i in range(13):
    for j in range(13):
      rank1 = RANK[i]
      rank2 = RANK[j]
      if i == j:
        # generate pair
        starting_hands.append([rank1 + 'h', rank2 + 'd'])
      if i > j:
        # generate offsuit
        starting_hands.append([rank1 + 'h', rank2 + 'd'])
        # generate suit
        starting_hands.append([rank1 + 'h', rank2 + 'h'])
  return starting_hands

number_of_opponent_clusters = 8

opponent_cluster = [
  ["3h2h", "4h2h", "5h2h", "6h2h", "7h2h", "4h3h", "5h3h", "6h3h", "7h3h", "5h4h", "6h4h", "3h2d", "4h2d", "4h3d", "5h2d", "5h3d", "5h4d", "6h2d", "6h3d", "6h4d", "6h5d", "7h2d", "7h3d", "7h4d", "8h2d", "8h3d"],
  ["8h2h", "9h2h", "Th2h", "8h3h", "9h3h", "7h4h", "8h4h", "9h4h", "7h5d", "8h4d", "8h5d", "9h2d", "9h3d", "9h4d", "9h5d", "Th2d", "Th3d", "Th4d", "Th5d", "Jh2d", "Jh3d"],
  ["Th3h", "Th4h", "6h5h", "7h5h", "8h5h", "9h5h", "Th5h", "7h6h", "8h6h", "9h6h", "Th6h", "8h7h", "9h7h", "9h8h", "7h6d", "8h6d", "8h7d", "9h6d", "9h7d", "9h8d", "Th6d", "Th7d", "Th8d"],

]

