import json
from collections import OrderedDict
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer

import sys
sys.path.insert(0, '../')
from bing_spell_check_api import *


def copy_rankings[x], reverse = True)
	if x in copy_rankings:#.has_key(x):
		return -copy_rankings[x]
	else:
		return 0


def get_related_acts(search_query):

	file = open('actlist.txt' , 'r')

	abb_file = open('abbreviation_mapping.json', 'r')
	abb_dict = json.load(abb_file)
	acts = []
	
	tokenizer = RegexpTokenizer(r'\w+')
	act_tokens = tokenizer.tokenize(search_query)
	# print(act_tokens)

	numerical_part = []
	for word in act_tokens:
		if any(ch.isdigit() for ch in word):
			numerical_part.append(word)

	# print(numerical_part)



	for act in file:
		act = act.rstrip('\n')

		acts.append(act)
	for key in abb_dict:
		acts.append(key)

	file.close()

	# print(acts[:10])


	rel_acts = process.extract(search_query, acts, limit =50 ,scorer=fuzz.token_set_ratio)
	copy_rel_acts = []
	i = 0
	for act in rel_acts:
		if act[0] in abb_dict:#.has_key(act[0]):
			for x in abb_dict[act[0]]:
				copy_rel_acts.append((x,act[1]))
		else :
			copy_rel_acts.append(act)
	# print(str(rel_acts) + '\n')

	return copy_rel_acts, numerical_part

def get_related_cases(rel_acts):
	

	f = open('act_to_cases.json','r')

	act_to_case_dict = json.load(f)
	cases = []
	for act in rel_acts:
		# print(act)
		try:
			for x in act_to_case_dict[act[0]]:
				cases.append(x)
		except :
			pass

	# print(cases[0])

	cases_relv = set(cases)
	# print(cases_relv)
	return cases_relv



def cases_and_acts(search_query):
	# search_query = raw_input("search query = ")
	search_query1 = search_query.replace('.', '')

	try:
		search_query = corrected_text(search_query1)
	except:
		search_query = search_query1

	rel_acts, numerical_part = get_related_acts(search_query)	

	final_dict = {}
	rel_acts_wo_score = [x[0] for x in rel_acts]
	final_dict['acts'] = rel_acts_wo_score[:min(10,len(rel_acts_wo_score))]
	# print(rel_acts)
	cases = get_related_cases(rel_acts)
	# print(cases)
	cases = list(cases)
	cases = cases[:min(10,len(cases))]
	# print(cases)
	f = open('case_ranking.json','r')
	rankings = json.load(f)
	# print(rankings[:10])
	copy_rankings = {}
	scaling_ratio = 1000/6
	for x in rankings:
		# print(i)
		copy_rankings[x] = rankings[x]*scaling_ratio
	# print(copy_rankings)

	sorted_cases = sorted(cases, key = lambda x:copy_rankings[x], reverse = True)
	print(sorted_cases)
	cases_score_dict = []
	# print(sorted_cases)
	for case in sorted_cases:
		
		if case in copy_rankings:#.has_key(case):
			cases_score_dict.append(copy_rankings[case][0])

	final_dict['cases'] = cases_score_dict

	return final_dict
