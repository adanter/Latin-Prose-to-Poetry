from metrifier import Metrifier


def hendecasyllablic_recall_test(filename, metrifier):
	"""
	Attempts to metrify a file full of proper hendecasyllabic poetry, then returns the recall value:  the number of
	lines that it recognized as metrical in their original configuration out of the total number of lines.
	:param filename: string Name of a text file containing macronized lines of hendecasyllabic poetry
	:param metrifier: Metrifier
	:return:
	"""
	file = open(filename, 'r', encoding='utf8')
	total_lines = 0
	correct_lines = 0
	for line in file:
		sequence = metrifier.preprocess(line)
		permutations = metrifier.find_valid_sequences(line)
		total_lines += 1
		print('Line number: ', total_lines)
		if sequence in permutations:
			correct_lines += 1
		print('Correct lines: ', correct_lines)
	file.close()
	recall = correct_lines/total_lines
	return recall


def get_accepted_meters(filename, num_to_find, metrifier):
	file = open(filename, 'r', encoding='utf8')
	accepted_sequences = []
	for line in file:
		valid_meters = metrifier.find_valid_sequences(line)
		if valid_meters:
			accepted_sequences.append(valid_meters[0])
		if len(accepted_sequences) >= num_to_find:
			break
	results = {}
	for i in range(min(num_to_find, len(accepted_sequences))):
		text = metrifier.sequence_to_string(accepted_sequences[i])
		meter = metrifier.scanner.scan_text(text)
		results[text] = meter
	return results


def main():
	while True:
		print('Enter the number for the process you wish to run, or "q" to quit:')
		print('1: Get the scansion for a line of Latin text')
		print('2: Rearrange Latin text to fit a meter')
		print('3: Run a recall test (this may take a few minutes)')
		print('4: Get a set of "metrical" lines and their scansions (useful for estimating accuracy)')
		user_input = ''
		while user_input not in ['1','2','3','4','q']:
			user_input = input('')
		if user_input == 'q':
			return
		metrifier = Metrifier()
		if user_input == '1':
			text = input('Enter the text which you wish to scan:\n')
			print('Scansion:')
			print(metrifier.scanner.scan_text(text))
			print('--------------------')
		elif user_input == '2':
			text = input('Enter the text which you wish to metrify:\n')
			options = metrifier.find_valid_sequences(text)
			if len(options) >= 1:
				print('Valid permutations:')
				print(options)
			else:
				print('No valid permutations found.')
			print('--------------------')
		elif user_input == '3':
			filename = input('Enter the name of the poetry file you wish to read in, or press "enter"'
							 ' to use hendecasyllabics.txt:\n')
			if filename == '':
				filename = 'hendecasyllabics.txt'
			print('Running test...')
			print('Recall = ', hendecasyllablic_recall_test(filename, metrifier))
			print('--------------------')
		else:
			filename = input('Enter the name of the text file you wish to read in, or press "enter"'
							 ' to use hendecasyllabics.txt:\n')
			if filename == '':
				filename = 'hendecasyllabics.txt'
			number = input('Enter the number of lines and scansions you would like to return:\n')
			print('Working...')
			accepted_meters = get_accepted_meters(filename, int(number), metrifier)
			for text, meter in accepted_meters.items():
				print(text)
				print(meter)
			print('--------------------')
main()