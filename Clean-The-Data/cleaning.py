import csv
import random

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

if __name__ == "__main__":
	rows = read_the_csv("../Data/bhcf1609.csv")

	print "Read {} rows from disk".format(len(rows))

	# rows = clean_the_data(rows)

	write_to_disk(rows, "../Building-Data/buildme.csv", "../Scoring-Data/scoreme.csv", 9)