import csv
import random
import pandas as pd

def read_the_csv(filename):
	rt = []
	with open(filename, "r") as f:
		for row in csv.reader(f):
			rt.append(row)
	return rt

def write_to_disk(rows, buildpath, scorepath, score_ratio):
	build = csv.writer(open(buildpath, "w"))
	score = csv.writer(open(scorepath, "w"))
	headers = rows[0]

	build.writerow(headers)
	score.writerow(headers)

	build_count = 0
	score_count = 0

	for row in rows[1:]:
		y = random.randint(1, 10)
		if y <= score_ratio:
			build.writerow(row)
			build_count += 1
		else:
			score.writerow(row)
			score_count += 1

	print "Wrote {} rows to build".format(build_count)
	print "Wrote {} rows to score".format(score_count)
	print "And that's witholding {}% for scoring".format(100 * score_count/len(rows))

def drop_columns(rows):
	print "Checking column validity on {} rows".format(len(rows))
	rt = []
	row_checker = {}

	keep_these_columns = {}

	for i in range(len(rows[0])):
		row_checker[i] = " "

	for row in rows[1:]:
		for idx, each in enumerate(row):
			default = row_checker[idx]
			if default != each:
				if default == " ":
					row_checker[idx] = each
				else:
					keep_these_columns[idx] = True

	print "Found {} columns to keep out of {} total".format(len(keep_these_columns), len(rows[0]))

	for row in rows:
		new_row = []
		for idx, each in enumerate(row):
			if idx in keep_these_columns:
				new_row.append(each)
		rt.append(new_row)

	print "Sending back {} rows and {} columns".format(len(rt), len(rt[0]))

	return rt


if __name__ == "__main__":
	rows = read_the_csv("../Data/bhcf1609.csv")

	print "Read {} rows from disk".format(len(rows))

	rows = drop_columns(rows)

	# write_to_disk(rows, "../Building-Data/buildme.csv", "../Scoring-Data/scoreme.csv", 9)