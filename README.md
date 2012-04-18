# PyLight - A Light Table backend for Python #

Warning:  Early alpha software ahead!

During my exploration of bringing the Meta II compiler to Python I was interrupted by the insanely cool Light Table demo video.  If you haven't seen it, go watch it now!

Since I was already digging thru the tokenizer and compiler for Python I decided to see if I could achieve the live tracing as seen in Light Table.

The fruits of my labor is PyLight.

PyLight runs python code and prints out the substitutions as shown in the Light Table video.

_Shut up, and show me_

Simple example:

    def ex1(x):
        y = x * x
        return y, ex2(y)

    def ex2(y):
        return y / 3

    ex1(20)

(Save to test.py)

To see the substitutions for this file run it with PyLight like so:

   python pylight.py test.py

You should see the following:

    def ex1(20):
        y = 20 * 20
        return 400, ex2(400)

    def ex2(400):
        return 400 / 3

More fun:

    def fac(n):
    	if n <= 1:
	    return 1
    	else:
	    return n * fac(n - 1)

    fac(5)

Output:

    def fac(5):
        if 5 <= 1:
            return 1
        else:
            return 5 * fac(5 - 1)

    def fac(4):
        if 4 <= 1:
            return 1
        else:
            return 4 * fac(4 - 1)

    def fac(3):
        if 3 <= 1:
            return 1
        else:
            return 3 * fac(3 - 1)

    def fac(2):
        if 2 <= 1:
            return 1
        else:
            return 2 * fac(2 - 1)

    def fac(1):
        if 1 <= 1:
            return 1
        else:
            return n * fac(n - 1)

## Known issues ##

    * Class handling is quite ugly
    * Functions with internal iteration currently only show the final result of the iteration.

## Next steps ##

    * Fix class handling
    * Show internal iteration properly for some value of properly
    * Chase down endless edge cases
    * Add support to pull out a call graph for a function

## Call for help ##

There are endless bugs to discover and fix.  If you are so inclined please roll up your sleeves and get to work.