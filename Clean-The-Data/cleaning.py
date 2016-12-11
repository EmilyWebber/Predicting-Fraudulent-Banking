from __future__ import division
import csv
import random
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("ggplot")

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

def graph_missing_values(values):
	plt.plot(values)
	plt.title("Distribution of missing values")
	plt.ylabel("Count of missing values")
	plt.xlabel("Column number the count refers to")
	plt.show()

def check_integer_conversion(rows):
	print "About to check {} rows for integer compatibility".format(len(rows))
	rt = []

	drop_columns = {}

	for row in rows[1:]:
		for idx, each in enumerate(row):
			try:
				i = int(each)
			except:
				if idx not in drop_columns:
					drop_columns[idx] = 0
				else:
					drop_columns[idx] += 1

	# v = list(drop_columns.values())

	# v.sort()

	# based on this graph I'm decided to only use features when their count of missing values is <= 175.
	# pretty clear jump in the graph to back that up
	# graph_missing_values(v)

	for row in rows:
		new_row = []
		for idx, each in enumerate(row):
			count = drop_columns[idx]
			if count <= 175:
				new_row.append(each)
		rt.append(new_row)

	dropped = 0

	for key, value in drop_columns.items():
		if value <= 175:
			dropped += 1

	print "Found {} columns to drop because of missing values, keeping {}".format(dropped, len(rows[0]) - dropped)

	return rt

def label_the_data(rows):

	rows[0].append("Label")

	for row in rows[1:]:
		label = random.randint(0, 1)
		row.append(label)

	return rows


if __name__ == "__main__":
	rows = read_the_csv("../Data/bhcf1609.csv")

	print "Read {} rows from disk".format(len(rows))

	rows = drop_columns(rows)

	rows = check_integer_conversion(rows)

	print "========================================"

	rows = label_the_data(rows)

	write_to_disk(rows, "../Building-Data/buildme.csv", "../Scoring-Data/scoreme.csv", 9)