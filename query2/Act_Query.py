import re
from query2 import cases_and_acts
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

# inp_words = input()




def act_query(inp_words)

	inp_words = re.split(' |, |-|\(|\)', inp_words)s

	flag_sec = 0
	flag = 0
	sec_no = "-1"
	year = "-1"
	str_acts = ""

	for i in range(len(inp_words)):
		if inp_words == "":
			continue

		if inp_words[i][0] >= '0' and inp_words[i][0] <= '9' and len(inp_words[i]) == 4:
			year = inp_words[i]
			continue

		if flag == 0:
			if inp_words[i].lower() == "sec" or inp_words[i].lower() == \
				"sect" or inp_words[i].lower() == "secti" or inp_words[i].lower() == \
				"sectio" or inp_words[i].lower() == "section":

				flag = 1


			elif inp_words[i].lower() not in stop_words:
				str_acts += " "
				str_acts += inp_words[i]

		elif flag == 2 and inp_words[i].lower() not in stop_words:

			str_acts += " "
			str_acts += inp_words[i]

		elif inp_words[i][0] >= '0' and inp_words[i][0] <= '9':
			flag = 2
			sec_no = inp_words[i]

	if sec_no != '-1':
		sec_no = int(sec_no)

	if year != "-1":
		year = int(year)

	final_dict = cases_and_acts(str_acts[1:])

	final_dict["section"] = sec_no

	final_dict["year"] = year

	return final_dict

