#nWoD Dice roller#
#Version 1#
##########

import random
import optparse


#PARSE CLI or use Defaults
def build_parser():
	parser = optparse.OptionParser(usage='Roll Some Dice!')
	parser.add_option("-s", "--sides", dest="sides", help="Number of sides on the dice rolled - 6, 10, 20?", type=int, default=10)
	parser.add_option("-n","--num",dest="num", help="Number of dice to roll.", type=int, default=1)
	parser.add_option("-a","--again",dest="again", help="Reroll any dice equal to or above this number", type=int, default=10)
	parser.add_option("-+","--above",dest="above", help="Count all dice rolls equal to or above this number", type=int,default=8)
	parser.add_option("-w","--web",dest="web", help="setup rest server on 8080", type=int, default=0)
	
	(options, args) = parser.parse_args()
	return options

def roll_die(sides):
	return random.randint(1, sides)

def roll_multipledice(num, sides):
	raw_dice = []
	for _ in range(num): 
		raw_dice.append(roll_die(sides))
	return raw_dice 

def roll_multipledicemultipletimes(num, sides, again):
	master_rawdice = []
	again_dice = []
	still = True
	while still:
		if again_dice != []:
			num = len(again_dice)
		raw_dice=roll_multipledice(num, sides)
		master_rawdice.extend(raw_dice)
		again_dice=list(filter(lambda x: x >= again, raw_dice))
		if again_dice == []:
			still = False
	return master_rawdice
	
def score_dice(dicerolls, above):
	print (dicerolls)
	winners = []
	for dice in dicerolls:
		print (dice)
		if dice >= above:
			winners.append(dice)
	return winners		

if __name__ == "__main__":
	options = build_parser()
	print ('running with ' + str(options))
	
	if options.web == 0:
		t2 = roll_multipledicemultipletimes(options.num, options.sides, options.again)
		print ('Rolled ==> ' + str(t2))
		t2 = score_dice(t2, options.above)
		print ('Success Rolls => ' + str(t2))
	else: 
		print('running as webserver')
	
