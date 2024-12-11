input = "input/dec1.txt"
l1 = []
l2 = []
with open(input) as f:
    a = f.read()

for line in a.split("\n"):
    if len(line) > 0:
        b = line.split("   ")
        l1.append(int(b[0]))
        l2.append(int(b[1]))

l1.sort()
l2.sort()

diff_sum = 0
for i, j in zip(l1, l2):
    diff_sum += abs(i - j)

print(diff_sum)
