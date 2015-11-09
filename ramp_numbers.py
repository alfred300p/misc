'''
Copyright (c) Paulo Pinto <paulo@cod.pt>
Sample solution of the challenge at: reddit.com/3o4tpz, comment cvudq0c

Ramp Numbers - A ramp number is a number whose digits from left to right
either only rise or stay the same. 1234 is a ramp number as is 1124.
1032 is not.
Given: A positive integer, n.
Output: The number of ramp numbers less than n.
Example input: 123
Example output: 65

This implementation assumes 0 is also a ramp number, since the description
doesn't imply this. So the actual result for 123 would be 66.

This is also quite fast!
between 0 and 100000000000000000000 (including) there are 10015005 ramp numbers
real    0m10.023s
user    0m0.031s
sys     0m0.062s
'''

def getramps(upto):
	count = 1 # include "0"
	uptodigits = list(map(int, str(upto))) # for easy comparison with `digits`
	maxlength = len(uptodigits)
	def check(sofar = [], lastdigit = 1):
		nonlocal count # I find nonlocal so non-pythonic :'(
		for d in range(lastdigit, 10):
			digits = sofar + [d]
			# no need to check if we're within the interval if we have less
			# digits than `upto`
			if len(digits) == maxlength:
				if digits <= uptodigits:
					count += 1
			else:
				count += 1

			if len(digits) < maxlength:
				check(digits, d)

	check()
	print('in the interval [0,%d] there are %d ramp numbers' % (upto, count))

# show off
import random
for i in range(10):
	getramps(random.randint(10, 10**10))
