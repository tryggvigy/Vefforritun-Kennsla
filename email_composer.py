#!/usr/bin/python
# -*- encoding: utf-8 -*-
from ODSReader import *

def in_list(word, list):
	for list_word in list:
		if list_word in word:
			return True
	return False

def get_table_headings(table):
	cmp_headings = table[1]
	cmp_percentages = table[2]
	whitelist = ['Hluti']
	blacklist = ['Nemandi']

	table_headings = []
	skip_nr = 0

	for i in range(len(cmp_headings)) :

		if in_list(cmp_headings[i], blacklist) :
			skip_nr = skip_nr + 1
			continue

		if in_list(cmp_headings[i], whitelist) :
				table_headings.append({ 'name' : cmp_headings[i], 'percentage' : '' })
				skip_nr = skip_nr + 1
				continue

		table_headings.append({ 'name' : cmp_headings[i], 'percentage' : cmp_percentages[i-skip_nr] })

	return table_headings

def make_header(table):
	vefforitun_str = table[0][0]
	proj_nr_str = table[0][1]

	heading = u"SJÁ VIÐHENGI FYRIR UMSÖGNINA ÞÍNA!\n\n"
	heading = heading + vefforitun_str + '\t' + proj_nr_str + '\n\n'

	info = ''
	try:
	 	info = table[0][2]
	 	heading = heading + info + '\n\n'
	except Exception, e:
		# print '\n[!] No extra info attached, continuing...\n'
		# no extra info specified, that's ok.
	 	pass

	heading = heading + u'Upplýsingar um einkunnagjöf:\n'

	table_headings = get_table_headings(table)

	for table_heading in table_headings :
		heading = heading + table_heading.get('name') + ' ' + table_heading.get('percentage') + '\n'

	return heading

def get_student(student_id, table):
	for row in table :
		if student_id in row:
			return row

def make_student_grade(student_id, table):
	grades = u'Nemandi: ' + student_id + '\n'
	table_headings = get_table_headings(table)
	student = get_student(student_id, table)
	student_name = student.pop(0) # pop the student name column, we will add that in later.
	i = 0
	for table_heading in table_headings:
		if table_heading.get('percentage') is not '' :
			table_heading['percentage'] = student[i] + '.00%'
			i = i + 1
		grades = grades + table_heading.get('name') + ' ' + table_heading.get('percentage') + '\n'

	# change the strign to float, divide by 10 and make into a string again
	student_final_grade = float(student.pop()) / 10
	student_final_grade = str(student_final_grade)

	grades = grades + '\nEinkunn: ' + student_final_grade
	return grades


def compose_email(table, student_id):
	email = make_header(table) + '\n'
	email = email + u'====================== ÞÍNAR EINKUNNIR ======================\n'
	email = email  + make_student_grade(student_id, table)
	email = email + '\n==============================================================\n\n'
	email = email + u'emailið er auto-generatað.'
	return email


def get_email_addresses(table):
	collection = []
	for row in table:
		first_cell = row[0]
		collection.append(first_cell)
	#cut off cells that come before the list of hi emails.
	email_addresses = collection[3:]

	return email_addresses


def main():
	import argparse, os
	script_dir = '.'

	parser = argparse.ArgumentParser(description='This program composed an email from a .ods file inside a specific project.')
	parser.add_argument('-b','--basedir', help='base directory of project.', required=True)
	parser._optionals.title = "flag arguments"
	args = vars(parser.parse_args())


	base_dir = os.path.join(script_dir, args['basedir'])
	projects_dir = os.path.join(base_dir, "YFIRFARID")
	ODS_FILE = os.path.join(base_dir, "yfirferd.ods")

	doc = ODSReader(ODS_FILE)
	table = doc.getSheet("Sheet1")

	print compose_email(table, 'trg8')
	# print get_email_addresses(table)

if __name__ == '__main__':
	main()
