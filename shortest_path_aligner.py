import csv
import sys


def hamming_distance(seq1, seq2):
    if len(seq1) != len(seq2):
        return -1
    distance = 0

    for i in range(len(seq1)):
        if seq1[i] != seq2[i]:
            distance += 1
    return distance


def hex_to_bin(base_num):
    return bin(int(str(base_num), 16))[2:].zfill(8)


def align(m_actual, m_expected, miss_penalty):
    m = len(m_actual)
    n = len(m_expected)
    err_matrix = [[0] * (n + 1) for i in range(m + 1)]

    for i in range(m):
        err_matrix[i][0] = miss_penalty
    for i in range(n):
        err_matrix[0][i] = miss_penalty

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if m_actual[i - 1] == m_expected[j - 1]:
                err_matrix[i][j] = err_matrix[i - 1][j - 1]
            else:
                err_matrix[i][j] = min(
                    err_matrix[i - 1][j - 1] + hamming_distance(hex_to_bin(m_actual[i - 1]),
                                                                hex_to_bin(m_expected[j - 1])),
                    err_matrix[i][j - 1] + miss_penalty)
    i = m
    j = n
    aligned_actual = [0] * n
    aligned_pos = n - 1

    while i != 0 and j != 0:
        if m_actual[i - 1] == m_expected[i - 1]:
            aligned_actual[aligned_pos] = m_actual[i - 1]
            i -= 1
            j -= 1
            aligned_pos -= 1
        elif err_matrix[i - 1][j - 1] + hamming_distance(hex_to_bin(m_actual[i - 1]), hex_to_bin(m_expected[j - 1])) == \
                err_matrix[i][j]:
            aligned_actual[aligned_pos] = m_actual[i - 1]
            i -= 1
            j -= 1
            aligned_pos -= 1
        elif err_matrix[i][j - 1] + miss_penalty == err_matrix[i][j]:
            aligned_actual[aligned_pos] = "-"
            j -= 1
            aligned_pos -= 1

    while aligned_pos > 0:
        if i > 0:
            aligned_actual[aligned_pos] = m_actual[i - 1]
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
            total_err += hamming_distance(hex_to_bin(aligned_actual[r]), hex_to_bin(m_expected[r]))

    return [total_err, total_miss, aligned_actual]


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f'Invalid number of arguments, use: python3 shortest_path_aligner input_file output_file miss_penalty')
        exit()

    raw_data_path = sys.argv[1]
    output_file_path = sys.argv[2]
    p_miss = int(sys.argv[3])

    actual = []
    expected = []

    with open(raw_data_path) as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            actual.append(row[0])
            expected.append(row[1])

        del actual[0]
        del expected[0]

    actual.reverse()
    expected.reverse()
    [t_err, t_miss, aligned] = align(actual, expected, p_miss)
    aligned.reverse()
    expected.reverse()

    with open(output_file_path, mode='w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["actual", "expected"])
        for i in range(len(expected)):
            csv_writer.writerow([aligned[i], expected[i]])

    print(f'Total error {t_err}bits = {t_err / (512 * 8) * 100}%')
    print(f'Packets missed {t_miss} = {t_miss / 512 * 100}%')

