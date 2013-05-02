def get_frequencies(sequences):
	seqs_frequencies = {seq: (sequences.count(seq) / len(sequences)) for seq in set(sequences)}
	return seqs_frequencies