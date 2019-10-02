import csv


def hamming_distance(seq1, seq2):
    if len(seq1) != len(seq2):
        return -1
    distance = 0

    for i in range(len(seq1)):
        if seq1[i] != seq2[i]:
            distance += 1
    return distance


def hex_to_bin(base_num):
    return bin(int(base_num, 16))[2:].zfill(8)


actual = []
expected = []
p_miss = 8

with open('/home/ubuntu/Documents/raw.csv') as csv_file:
    csv_reader = csv.reader(csv_file)

    for row in csv_reader:
        actual.append(row[0])
        expected.append(row[1])

    del actual[0]
    del expected[0]

print(actual)
print(expected)

m = len(actual)
n = len(expected)
err_matrix = [[0] * (n + 1) for i in range(n + 1)]

for i in range(n):
    err_matrix[0][i] = p_miss
    err_matrix[i][0] = p_miss

for i in range(1, m + 1):
    for j in range(1, n + 1):
        if actual[i - 1] == expected[j - 1]:
            err_matrix[i][j] = err_matrix[i - 1][j - 1]
        else:
            err_matrix[i][j] = min(
                err_matrix[i - 1][j - 1] + hamming_distance(hex_to_bin(actual[i - 1]), hex_to_bin(expected[j - 1])),
                err_matrix[i][j - 1] + p_miss)
i = m
j = n
aligned_actual = [0] * n
aligned_pos = n - 1

while i != 0 and j != 0:
    if actual[i - 1] == expected[i - 1]:
        aligned_actual[aligned_pos] = actual[i - 1]
        i -= 1
        j -= 1
        aligned_pos -= 1
    elif err_matrix[i - 1][j - 1] + hamming_distance(hex_to_bin(actual[i - 1]), hex_to_bin(expected[j - 1])) == \
            err_matrix[i][j]:
        aligned_actual[aligned_pos] = actual[i - 1]
        i -= 1
        j -= 1
        aligned_pos -= 1
    elif err_matrix[i][j - 1] + p_miss == err_matrix[i][j]:
        aligned_actual[aligned_pos] = "-"
        j -= 1
        aligned_pos -= 1

while aligned_pos > 0:
    if i > 0:
        aligned_actual[aligned_pos] = actual[i - 1]
        aligned_pos -= 1
        i -= 1
    else:
        aligned_actual[aligned_pos] = "-"
        aligned_pos -= 1

total_err = 0
total_miss = 0
for r in range(n):
    if aligned_actual[r] == "-":
        total_miss += 1
    else:
        total_err += hamming_distance(hex_to_bin(aligned_actual[r]), hex_to_bin(expected[r]))

print(f'Total error {total_err}bits = {total_err / (512 * 8) * 100}%')
print(f'Packets missed {total_miss} = {total_miss / 512 * 100}%')

# with open('/home/ubuntu/Documents/pos1_free_130_aligned.csv', mode='w') as csv_file:
#     csv_writer = csv.writer(csv_file)
#     csv_writer.writerow(["actual", "expected"])
#     for r in range(n):
#         csv_writer.writerow([aligned_actual[r], expected[r]])
