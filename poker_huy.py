import itertools
from deuces import Evaluator, Card
import concurrent.futures
import json

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
SUITS = ["c", "d", "h", "s"]

def generate_starting_hands():
  starting_hands = []
  for i in range(13):
    for j in range(13):
      rank1 = RANKS[i]
      rank2 = RANKS[j]
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

opponent_clusters = [
  ["3h2h", "4h2h", "5h2h", "6h2h", "7h2h", "4h3h", "5h3h", "6h3h", "7h3h", "5h4h", "6h4h", "3h2d", "4h2d", "4h3d", "5h2d", "5h3d", "5h4d", "6h2d", "6h3d", "6h4d", "6h5d", "7h2d", "7h3d", "7h4d", "8h2d", "8h3d"],
  ["8h2h", "9h2h", "Th2h", "8h3h", "9h3h", "7h4h", "8h4h", "9h4h", "7h5d", "8h4d", "8h5d", "9h2d", "9h3d", "9h4d", "9h5d", "Th2d", "Th3d", "Th4d", "Th5d", "Jh2d", "Jh3d"],
  ["Th3h", "Th4h", "6h5h", "7h5h", "8h5h", "9h5h", "Th5h", "7h6h", "8h6h", "9h6h", "Th6h", "8h7h", "9h7h", "9h8h", "7h6d", "8h6d", "8h7d", "9h6d", "9h7d", "9h8d", "Th6d", "Th7d", "Th8d"],
  ["2h2d", "Jh2h", "Qh2h", "Kh2h", "Jh3h", "Qh3h", "Jh4h", "Qh4h", "Jh5h", "Qh5h", "Jh6h", "Jh4d", "Jh5d", "Jh6d", "Jh7d", "Qh2d", "Qh3d", "Qh4d", "Qh5d", "Qh6d", "Qh7d", "Kh2d", "Kh3d", "Kh4d"],
  ["Qh6h", "Th7h", "Jh7h", "Qh7h", "Th8h", "Jh8h", "Qh8h", "Th9h", "Jh9h", "Qh9h", "JhTh", "Th9d", "Jh8d", "Jh9d", "JhTd", "Qh8d", "Qh9d", "QhTd", "QhJd"],
  ["3h3d", "4h4d", "5h5d", "Ah2h", "Kh3h", "Ah3h", "Kh4h", "Ah4h", "Kh5h", "Ah5h", "Kh6h", "Ah6h", "Kh7h", "Kh8h", "Kh5d", "Kh6d", "Kh7d", "Kh8d", "Kh9d", "Ah2d", "Ah3d", "Ah4d", "Ah5d", "Ah6d", "Ah7d", "Ah8d"],
  ["6h6d", "7h7d", "Ah7h", "Ah8h", "Kh9h", "Ah9h", "QhTh", "KhTh", "AhTh", "QhJh", "KhJh", "AhJh", "KhQh", "AhQh", "AhKh", "KhTd", "KhJd", "KhQd", "Ah9d", "AhTd", "AhJd", "AhQd", "AhKd"],
  ["8h8d", "9h9d", "ThTd", "JhJd", "QhQd", "KhKd", "AhAd"]
]

all_hands = generate_starting_hands()
hands_to_cluster = {}

for index, cluster in enumerate(opponent_clusters):
  for hand in cluster:
    hands_to_cluster[hand] = index + 1

for column_index, column in enumerate(["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]):
  for row_index ,row in enumerate(["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]):
    if column_index > row_index:
      hand = column + 'h' + row + 'h'
    else:
      hand = row + 'h' + column + 'd'
    print(hands_to_cluster[hand])
  print("\n")


evaluator = Evaluator()

# Định nghĩa hàm process_private_card ra ngoài để có thể pickle
def process_private_card(private_card, SUITS, RANKS, evaluator, opponent_clusters):
    deck = [RANK + SUIT for SUIT in SUITS for RANK in RANKS]
    deck.remove(private_card[0])
    deck.remove(private_card[1])
    public_cards = list(itertools.combinations(deck, 5))
    result = {}
    count_public_card = 0

    for public_card in public_cards:
        ochs_vector = calculate_ochs(private_card, public_card, evaluator, opponent_clusters)
        result[''.join(private_card) + ''.join(public_card)] = ochs_vector
        count_public_card += 1
        print(f"Processed {count_public_card}/{len(public_cards)} public hands for {private_card}")
    return result

def precompute_ochs_features():
    ochs_table = {}
    all_hands = generate_starting_hands()  # Giả sử rằng bạn đã có một hàm để tạo ra tất cả các lá bài riêng tư có thể có
    SUITS = ['c', 'd', 'h', 's']  # Chỉnh sửa các biến này cho phù hợp
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    executor = concurrent.futures.ProcessPoolExecutor()
    futures = [executor.submit(process_private_card, private_card, SUITS, RANKS, evaluator, opponent_clusters) for private_card in all_hands]
    count_private_card = 0
    for future in concurrent.futures.as_completed(futures):
        ochs_table.update(future.result())
        count_private_card += 1
        print(f"Completed {count_private_card}/{len(all_hands)} private hands")

    return ochs_table

def calculate_ochs(private_card, public_card, evaluator, opponent_clusters):
    ochs_vector = {}
    private_card_object = [Card.new(card) for card in private_card]
    public_card_object = [Card.new(card) for card in public_card]

    for cluster_index, cluster in enumerate(opponent_clusters):
        wins = 0
        valid_comparisons = 0  # Số lần so sánh hợp lệ

        for opponent_hand in cluster:
            # Kiểm tra trùng lặp giữa opponent_hand và public_card
            if any(card in public_card for card in [opponent_hand[0:2], opponent_hand[2:4]]):
                continue

            # Nếu không trùng lặp, thực hiện so sánh
            opponent_hand_object = [Card.new(opponent_hand[0:2]), Card.new(opponent_hand[2:4])]
            if evaluator.evaluate(public_card_object, private_card_object) > evaluator.evaluate(public_card_object, opponent_hand_object):
                wins += 1
            valid_comparisons += 1  # Tăng số lần so sánh hợp lệ

        # Tính tỷ lệ thắng và lưu vào ochs_vector
        if valid_comparisons > 0:
            win_rate = wins / valid_comparisons
        else:
            win_rate = 0  # Trường hợp không có so sánh hợp lệ nào
        ochs_vector[cluster_index] = win_rate

    return ochs_vector

ochs_table = precompute_ochs_features()

# Ghi kết quả ra file JSON sau khi hoàn thành tính toán
with open('ochs_table.json', 'w') as f:
  json.dump(ochs_table, f)
