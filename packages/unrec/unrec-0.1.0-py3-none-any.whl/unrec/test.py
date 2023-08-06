
import sys
from relpath import add_import_path
add_import_path("../")
import unrec

@unrec
def frac(n):
	if n == 0: return 1
	return n * frac(n-1)

@unrec
def fib(n):
	if n <= 1: return n
	return fib(n-1) + fib(n-2)

@unrec
def ack(m,n):
	if m == 0: return n+1
	if n == 0: return ack(m-1, 1)
	return ack(
		m-1,
		ack(m,n-1)
	)

# 非常に大きい数の階乗
print(frac(4000))
