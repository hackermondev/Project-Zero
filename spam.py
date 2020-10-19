import json

with open('spam_things/letter_pairs.json', 'r') as f:
	letter_pair_scores = json.loads(f.read())

with open('spam_things/things.txt', 'r') as f:
	things = f.read().strip().split('\n\n')

with open('spam_things/words.txt', 'r') as f:
	words_nosplit = f.read()
	words = words_nosplit.splitlines()
	

def get_score(phrase):
	score = 0
	for i in range(len(phrase) - 1):
		input_pair = phrase[i] + phrase[i + 1]
		score += letter_pair_scores.get(input_pair, 0)
	return score
