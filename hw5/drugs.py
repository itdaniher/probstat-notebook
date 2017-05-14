#!/usr/bin/python
PD=0.01
PN=0.99

P1D=0.6
P1N=0.01

population = 1000

users = population*PD
nonusers = population - users

confirmed_users = users * P1D
false_users = nonusers * P1N

probability = confirmed_users/(confirmed_users+false_users)
print confirmed_users, '/', confirmed_users+false_users
