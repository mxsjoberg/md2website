# Even Fibonacci numbers
#
# Each new term in the Fibonacci sequence is generated by 
# adding the previous two terms. By starting with 1 and 2, 
# the first 10 terms will be: 1, 2, 3, 5, 8, 13, 21, 34, 
# 55, 89, ...
#
# By considering the terms in the Fibonacci sequence whose 
# values do not exceed four million, find the sum of the 
# even-valued terms.
#
# https://projecteuler.net/problem=2

# test
seq = list()
for n in list(range(10)):
    if n == 0:
        seq.append(1)
    if n == 1:
        seq.append(2)
    if n > 1:
        seq.append(seq[n - 2] + seq[n - 1])

assert(seq == list([1, 2, 3, 5, 8, 13, 21, 34, 55, 89]))

# solution
seq = list()
result = list()
max_value = 4000000
n = 0
while True:
    if n == 0:
        seq.append(1)
    if n == 1:
        seq.append(2)
    if n > 1:
        seq.append(seq[n - 2] + seq[n - 1])

    # break condition
    if seq[n] > max_value:
        seq.pop(n)
        break

    # even
    if seq[n] % 2 == 0:
        result.append(seq[n])

    n += 1

print(sum(result))
# 4613732