#!/usr/bin/python
import random
winners1 = []
winners2 = []
for i in range(1000):
	dice1 = random.randint(1,6)
	dice2 = random.randint(1,6)
	if dice1 + dice2 == 8:
		winners1.append(dice1)
		winners2.append(dice2)
dice1 = list(set(winners1))
dice2 = list(set(winners2))
print dice1, dice2
