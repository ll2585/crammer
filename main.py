import gui, sys

def main(args):
	if(len(args)>1):
		gui.main(args[1])
	else:
		gui.main("test2.csv")

if __name__ == "__main__":
	main(sys.argv)