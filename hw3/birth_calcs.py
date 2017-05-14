import survey
import percentile

table = survey.Pregnancies()
table.ReadRecords()

birthWeightFirsties = []
birthWeightOthers = []
myBirthWeight = 8.5

firsties = []
others = []

for record in table.records:
    if record.outcome == 1:
        if record.birthord == 1:
            firsties.append(record)
        else:
            others.append(record)

for record in firsties:
	if type(record.birthwgt_lb) and type(record.birthwgt_oz) == int:
		birthWeightFirsties.append(record.birthwgt_lb + record.birthwgt_oz/16.0)

weightFirstiesPercentile = percentile.percentile(birthWeightFirsties, myBirthWeight)

for record in others:
	if type(record.birthwgt_lb) and type(record.birthwgt_oz) == int:
		birthWeightOthers.append(record.birthwgt_lb + record.birthwgt_oz/16.0)

weightOthersPercentile = percentile.percentile(birthWeightOthers, myBirthWeight)

print "percentile birthweight among firsties:", weightFirstiesPercentile
print "percentile birthweight among others:", weightOthersPercentile

