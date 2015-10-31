#nWoD Dice roller#
#Version 1#
##########

import random
import optparse
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import time


#PARSE CLI or use Defaults
def build_parser():
	parser = optparse.OptionParser(usage='Roll Some Dice!')
	parser.add_option("-s", "--sides", dest="sides", help="Number of sides on the dice rolled - 6, 10, 20?", type=int, default=10)
	parser.add_option("-n","--num",dest="num", help="Number of dice to roll.", type=int, default=1)
	parser.add_option("-a","--again",dest="again", help="Reroll any dice equal to or above this number", type=int, default=10)
	parser.add_option("-+","--above",dest="above", help="Count all dice rolls equal to or above this number", type=int,default=8)
	parser.add_option("-w","--web",dest="web", help="setup rest server on given port", type=int, default=0)
	
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
	winners = []
	for dice in dicerolls:
		if dice >= above:
			winners.append(dice)
	return winners		

def parse_queryargs(path):
		options = {}
		query = (path).split("&")
		for arg in query:
			quarg=arg.split("=")
			if len(quarg) == 2:
				options[quarg[0]] = int(quarg[1])
		return options

class DiceHandler(BaseHTTPRequestHandler):
	
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/plain")
		s.end_headers()
	def do_GET(s):
		s.send_response(200)
		s.send_header("Content-type", "text/plain")
		s.end_headers()
		
		options = parse_queryargs((urlparse(s.path)[4]))
		raw_rolls = []
		winning_rolls = []
		
		if len(options) == 4:
			raw_rolls = roll_multipledicemultipletimes(int(options['num']), options['sides'], options['again'])
			winning_rolls = score_dice(raw_rolls, options['above'])
			s.wfile.write(bytes(str(raw_rolls)+"\n", "utf-8"))
			s.wfile.write(bytes(str(winning_rolls), "utf-8"))
		elif len(options) == 3:
			raw_rolls = roll_multipledicemultipletimes(int(options['num']), options['sides'], options['again'])
			s.wfile.write(bytes(str(raw_rolls)+"\n", "utf-8"))
		else: 
			s.wfile.write(bytes("missing arguments please provide num, sides, again, and above","utf-8"))

		
	

		
def run_webservice(port):
	#server_class = BaseHTTPServer.HTTPServer
	httpd = HTTPServer(("0.0.0.0", port), DiceHandler)
	print (time.asctime(), "Server Starts - %s:%s" % ("0.0.0.0", port))
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print (time.asctime(), "Server Stops - %s:%s" % ("0.0.0.0", port))

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
		run_webservice(options.web)
		
	
