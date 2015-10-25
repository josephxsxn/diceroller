#nWoD Dice roller#
#Version 1#
##########

import random
import optparse

#PARSE CLI or use Defaults
parser = optparse.OptionParser(usage='Roll Some Dice!')
parser.add_option("-s", "--sides", dest="sides", help="Number of sides on the dice rolled - 6, 10, 20?", type=int, default=10)
parser.add_option("-n","--num",dest="num", help="Number of dice to roll.", type=int, default=1)
parser.add_option("-a","--again",dest="again", help="Reroll any dice above this number", type=int, default=10)
parser.add_option("-+","--above",dest="above", help="Count all dice rolls equal to or above this number", type=int,default=8)

(options, args) = parser.parse_args()
print ('running with ' + str(options))

rollsleft=options.num
dicerolls=[]
while rollsleft>0:
	roll=random.randint(1, options.sides)
	if roll >= options.again:
		dicerolls.append(roll)
	else:
		dicerolls.append(roll)
		rollsleft-=1
print ('Rolled ==> ' + str(dicerolls))
print ('Total Dice Rolled with \'agains\' ==>' + str(len(dicerolls)))

rollsuccess=[]
for roll in dicerolls:
	if roll >= options.above:
		rollsuccess.append(roll)
print ('Success Rolls => ' + str(rollsuccess))
print ('Success Count ==> ' + str(len(rollsuccess)))
