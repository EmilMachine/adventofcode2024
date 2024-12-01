from collections import Counter

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

l2count = Counter(l2)

answer = 0
for i in l1:
    answer += i * l2count[i]

print(answer)
