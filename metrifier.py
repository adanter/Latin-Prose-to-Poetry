from scanner import Scansion
from nltk import word_tokenize
import re

class Metrifier():
	def __init__(self):
		self.scanner = Scansion()
		self.preprocess_regex = re.compile('[^a-zA-Z āēīōū]')
		self.macronized_vowels = 'āēīōū'


	# Works fine!
	def find_valid_sequences(self, text):
		"""
		Returns all grammatical, metrical permutations of list of tokens
		:param tokens: List of strings
		:return: List of lists of strings
		"""
		tokens = self.preprocess(text)
		return self._find_valid_sequences(tokens, [])


	# Works fine!
	def _find_valid_sequences(self, tokens, sequence):
		"""
		Recursive call for find_valid_sequences
		:param tokens: List of tokens to be added to sequence
		:param sequence: List of tokens
		:return: List of lists of tokens
		"""
		valid_sequences = []
		for token in tokens:
			new_sequence = list(sequence + [token])
			if self.metrical(new_sequence):
				if len(tokens) > 1:
					new_tokens = list(tokens)
					new_tokens.remove(token)
					recursive_results = self._find_valid_sequences(new_tokens, new_sequence)
					if recursive_results:
						valid_sequences += recursive_results
				else:
					if self.metrical(new_sequence, True):
						valid_sequences.append(new_sequence)
		return valid_sequences


	# Works fine!
	def is_valid_start(self, string, pattern, complete_match = False):
		"""
		Does the input string match a substring that starts at the beginning of pattern?
		:param string: string
		:param pattern: list (list of lists of strings)
		:param complete_match: bool Does the input need to match the entire pattern?
		:return: bool
		"""
		if len(string) == 0:
			return True
		if len(pattern) == 0:
			return False
		component = pattern[0]
		for option in component:
			option_fits = True
			if len(option) < len(string):
				for i in range(len(option)):
					if (option[i] != string[i]) and (string[i] != 'x'):
						option_fits = False
						break
				if option_fits:
					if self.is_valid_start(string[len(option):], pattern[1:], complete_match):
						return True
			else:
				for i in range(len(string)):
					if (option[i] != string[i]) and (string[i] != 'x'):
						option_fits = False
						break
				if option_fits:
					if not complete_match:
						return True
					else:
						if (len(option) == len(string)) and (len(pattern) == 1):
							return True
						else:
							return False
				# else: complete_match is True and input is too short to match the current option, so go to the next option
				# Whoops... These are the cases when I really want to return "true":
					# complete_match and (len(option) == len(string)) and option_fits and (len(pattern) == 1)
					# !complete_match and option_fits
		return False


	# Works fairly well
	# Still need to make sure that the "consonantal u as penultimate character" case is valid for majority of Latin words
	# Scanner also has a few bugs - e.g. scans "Lesbia atque amemus" as "¯˘˘˘˘˘¯x" instead of "¯˘¯˘¯x", ignoring both
	#   elision and vowel lengthening from 'tq' after 'a' in 'atque'
	def metrical(self, sequence, complete_match = False):
		"""
		Is the sequence metrical up to this point?
		If optional parameter is set to "True", only returns "True" if the sequence matches the entire meter.
		:param sequence: list of strings
		:param complete_match: boolean
		:return: bool
		"""
		text = self.sequence_to_string(sequence)
		# The scanner prints a bunch of unwanted pseudo-errors if the last vowel is macronized.  This shortens the vowel
		# ahead of time
		# if text[-1] not in self.macronized_vowels:
		# 	if (len(text) >= 2) and (text[-2] in self.macronized_vowels):
		# 		text = text[:-2] + self.demacronize_char(text[-2]) + text[-1]
		# else:
		# 	text = text[:-1] + self.demacronize_char(text[-1])
		# 	# Remove consonantal 'u' in front of final vowel
		# 	if (len(text) >= 2) and (text[-2] == 'u'):
		# 		text = text[:-2] + text[-1]
		scansion = self.scanner.scan_text(text)
		hendecasyllabic = [['˘¯', '¯˘', '¯¯'], ['¯˘˘¯˘¯˘¯'], ['˘', '¯']]
		is_metrical = self.is_valid_start(scansion[0], hendecasyllabic, complete_match)
		# print('Metrical?')
		# print(text)
		# print(scansion)
		# print(is_metrical)
		return is_metrical


	# Works fine!
	def sequence_to_string(self, sequence):
		"""
		Joins a list of words into a sentence
		:param sequence: List of strings
		:return: string
		"""
		text = ''
		for word in sequence:
			text += word + ' '
		return text[:-1]


	# Works fine!
	def demacronize_char(self, char):
		short_chars = {'ā':'a', 'ē':'e', 'ī':'i', 'ō':'o', 'ū':'u'}
		if char in short_chars:
			return short_chars[char]
		else:
			return char


	# Works fine!
	def preprocess(self, token_string):
		"""
		First, make the string lowercase.
		Second, remove all character other than spaces and characters in the Latin alphabet with or without macrons.
		Third, split the string on spaces into one-word tokens.
		:param token_string: string
		:return: list
		"""
		token_string = token_string.lower()
		token_string = self.preprocess_regex.sub('', token_string)
		tokens = word_tokenize(token_string)
		return tokens