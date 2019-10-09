import csv
import sys

import shortest_path_aligner as saligner

window_size = 2


def find_right_position(actual, expected, index, window_s):
    for i in range(index, len(expected) - window_size + 1):
        if expected[i:i + window_size] == actual[index:index + window_size]:
            return i

    return -1


def main():
    if len(sys.argv) != 3:
        print(f'Invalid number of arguments, use: python3 {sys.argv[0]} input output')
        return

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    actual = []
    expected = []

    with open(input_file_path) as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            actual.append(row[0])
            expected.append(row[1])

        del actual[0]
        del expected[0]

    prev_checkpoint = -1
    aligned = [0] * len(expected)
    total_miss = 0
    total_err = 0

    for i in range(len(actual) - window_size + 1):
        position = find_right_position(actual, expected, i, window_size)
        if position != i and position != -1:
            misses = position - i
            p_miss = 8.0
            [t_err, t_miss, sub_arr] = saligner.align(actual[prev_checkpoint + 1:i + window_size],
                                                      expected[prev_checkpoint + 1:position + window_size], p_miss)
            while t_miss != misses:
                print(f'expected misses: {misses} actual misses: {t_miss} penalty: {p_miss}')
                if t_miss > misses:
                    p_miss += 0.2
                else:
                    p_miss -= 0.2
                [t_err, t_miss, sub_arr] = saligner.align(actual[prev_checkpoint + 1:i + window_size],
                                                          expected[prev_checkpoint + 1:position + window_size], p_miss)

            aligned[prev_checkpoint + 1:position + window_size] = sub_arr
            total_err += t_err
            total_miss += t_miss
            prev_checkpoint = position + window_size
            if prev_checkpoint == len(expected):
                break

    print(f'Total error {total_err}bits = {total_err / (512 * 8) * 100}%')
    print(f'Packets missed {total_miss} = {total_miss / 512 * 100}%')
    with open(output_file_path, mode='w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["actual", "expected"])
        for i in range(len(expected)):
            csv_writer.writerow([aligned[i], expected[i]])


if __name__ == '__main__':
    saligner.hex_to_bin('0')
    main()
