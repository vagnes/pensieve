#!/usr/bin/python3

import argparse
import datetime
import sys
import sqlite3
import time

# CLI setup

parser = argparse.ArgumentParser(
        description="Pensieve CLI")
parser.add_argument(
	"-i", "--input", metavar="str", nargs="+", type=str,
	help="Input memory to pensieve.")
parser.add_argument(
	"-c", "--continous", action="store_true",
	help="Enable continous input mode.")
parser.add_argument(
	"-r", "--retrieve", action="store_true",
	help="Retrieve one random memory.")
parser.add_argument(
	"-n", "--number", metavar="int", type=int,
	help="Number of memories to retrieve.")
parser.add_argument(
	"--reset", action="store_true",
	help="Resets the database.")
args = parser.parse_args()

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args=parser.parse_args()

# SQLite setup

try:
	sMemory = " ".join(args.input)
except TypeError as e:
	pass

bCont_mode = args.continous
bRetrieve_memory = args.retrieve
bReset_database = args.reset
nNumber_memory = args.number

conn = sqlite3.connect('pensieve.db')
c = conn.cursor()

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS pensieve(datestamp TEXT, memory TEXT)')

def reset_table():
	reset = input("Are you sure you want to delete the database?(y/n)\n> ")
	if reset == "y":
		c.execute('DROP TABLE pensieve')
		c.execute('CREATE TABLE pensieve(datestamp TEXT, memory TEXT)')
		print("::database reset::")
	elif reset == "n":
		print("Nothing deleted.")
		quit()
	else:
		print("Not a valid option. Nothing deleted.")

def single_data_entry(sMemory):
	sUnix = time.time()
	sDate = str(datetime.datetime.fromtimestamp(sUnix).strftime('%Y-%m-%d %H:%M:%S'))
	c.execute("INSERT INTO pensieve (datestamp, memory) VALUES (?, ?)",
		(sDate, sMemory))
	print("::saved::")
	conn.commit()

def continous_data_entry():
	print("Press '/q' to abort insertion.")
	print("Press '/w' to save and end insertion.\n")
	bQuit_cont_data_entry = False
	while bQuit_cont_data_entry == False:
		sContMemory = input("Insert memory:\n> ")
		if sContMemory == "/q":
			print("Memory insertion aborted.")
			bQuit_cont_data_entry = True
		elif sContMemory == "/w":
			print("Memory insertion saved and ended.")
			bQuit_cont_data_entry = True
			print("::saved::")
			conn.commit()
		else:
			sUnix = time.time()
			sDate = str(datetime.datetime.fromtimestamp(sUnix).strftime('%Y-%m-%d %H:%M:%S'))
			c.execute("INSERT INTO pensieve (datestamp, memory) VALUES (?, ?)",
				(sDate, sContMemory))

def single_memory_retrieval():
	c.execute("SELECT * FROM pensieve ORDER BY RANDOM() LIMIT 1")
	for row in c.fetchall():
		print("D/T:	", row[0], "\nC:	", row[1])

def number_memory_retrieval(nNumber_memory):
	c.execute("SELECT * FROM pensieve ORDER BY RANDOM() LIMIT (?)", [nNumber_memory])
	for row in c.fetchall():
		print("D/T: ", row[0], "\nCon: ", row[1], "\n")

if __name__ == "__main__":
	create_table()
	if bCont_mode:
		continous_data_entry()
	elif bRetrieve_memory:
		single_memory_retrieval()
	elif nNumber_memory:
		number_memory_retrieval(nNumber_memory)
	elif bReset_database:
		reset_table()
	else:
		single_data_entry(sMemory)