import wiringpi
from wiringpi import GPIO
import curses

wiringpi.wiringPiSetup()

wiringpi.pinMode(2, GPIO.OUTPUT)
wiringpi.pinMode(1, GPIO.OUTPUT)
wiringpi.pinMode(5, GPIO.OUTPUT)
wiringpi.pinMode(7, GPIO.OUTPUT)


screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

try:
	while True:
		char = screen.getch()
		if char == ord('q'): 
			break
		elif char == curses.KEY_UP:
			wiringpi.digitalWrite(1, GPIO.HIGH)
			wiringpi.digitalWrite(2, GPIO.LOW)
			wiringpi.digitalWrite(5, GPIO.HIGH)
			wiringpi.digitalWrite(7, GPIO.LOW)
		elif char == curses.KEY_DOWN:
			wiringpi.digitalWrite(1, GPIO.LOW)
			wiringpi.digitalWrite(2, GPIO.HIGH)
			wiringpi.digitalWrite(5, GPIO.LOW)
			wiringpi.digitalWrite(7, GPIO.HIGH)
		elif char == curses.KEY_RIGHT:
			wiringpi.digitalWrite(1, GPIO.LOW)
			wiringpi.digitalWrite(2, GPIO.HIGH)
			wiringpi.digitalWrite(5, GPIO.HIGH)
			wiringpi.digitalWrite(7, GPIO.LOW)
		elif char == curses.KEY_LEFT:
			wiringpi.digitalWrite(1, GPIO.HIGH)
			wiringpi.digitalWrite(2, GPIO.LOW)
			wiringpi.digitalWrite(5, GPIO.LOW)
			wiringpi.digitalWrite(7, GPIO.HIGH)
		elif char == ord('s'): 
			wiringpi.digitalWrite(1, GPIO.LOW)
			wiringpi.digitalWrite(2, GPIO.LOW)
			wiringpi.digitalWrite(5, GPIO.LOW)
			wiringpi.digitalWrite(7, GPIO.LOW)
finally:
	curses.nocbreak()
	screen.keypad(0)
	curses.echo()
	curses.endwin()
	
	wiringpi.cleanup()
	exit()
