import survey
import numpy

table = survey.Pregnancies()
table.ReadRecords()
count = 0
firsties = []
others = []

preglength = []

print 'Number of pregnancies', len(table.records)

for record in table.records:
	if record.outcome == 1:
		count += 1
		if record.birthord == 1:
			firsties.append(record)
		else:
			others.append(record)

for record in firsties:
	preglength.append(record.prglength)

firsties_duration = numpy.mean(preglength)

preglength = []

for record in others:
	preglength.append(record.prglength)

others_duration = numpy.mean(preglength)

print others_duration, firsties_duration
