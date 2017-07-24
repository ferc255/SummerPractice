import sys
import math


STRING = int(1e15)


def read(table, attributes):
    attributes[:] = input().split()
    input()
    for line in sys.stdin:
        table.append(line.replace(',', ' ').split());


def entropy(lot, total):
    result = 0
    for key in lot:
        fraction = lot[key] / total
        result += fraction * math.log(fraction, 2)
        
    return -result
        
        
def Info(table):
    lot = {}
    for row in table:
        if not(row[-1] in lot):
            lot[row[-1]] = 0
        lot[row[-1]] += 1

    return entropy(lot, len(table))


def calc_infos(lot, freq, total):
    result = 0
    aux = {}
    for key in freq:
        result += len(freq[key]) / total * entropy(lot[key], len(freq[key]))
        aux[key] = len(freq[key])

    return result, entropy(aux, total)


def get_dict_num(table, column, divider):
    lot = {}
    freq = {}
    for i, row in enumerate(table):
        relation = 'less' if float(row[column]) < float(divider) else 'greater'
        
        if not(relation in lot):
            lot[relation] = {}
        if not(row[-1] in lot[relation]):
               lot[relation][row[-1]] = 0
        lot[relation][row[-1]] += 1

        if not(relation in freq):
            freq[relation] = []
        freq[relation].append(i)

    return lot, freq
    

def get_dict_str(table, column):
    lot = {}
    freq = {}
    for i, row in enumerate(table):
        val = row[column]
        if not(val in lot):
            lot[val] = {}
        if not(row[-1] in lot[val]):
            lot[val][row[-1]] = 0
        lot[val][row[-1]] += 1

        if not(val in freq):
            freq[val] = []
        freq[val].append(i)

    return lot, freq


def Info_x(table, column, divider):
    if divider == STRING:
        lot, freq = get_dict_str(table, column)
    else:
        lot, freq = get_dict_num(table, column, divider)

    return calc_infos(lot, freq, len(table))


def calc_gain_ratio(table, column, divider, info):
    info_x, split_info = Info_x(table, column, divider)
    gain_ratio = info - info_x
    if split_info != 0:
        gain_ratio /= split_info
        #pass

    return gain_ratio
    

def update_best_ratio(table, column, info, best_ratio, best_column,
                      best_divider, divider):
    gain_ratio = calc_gain_ratio(table, column, divider, info)

    if gain_ratio > best_ratio:
        best_ratio = gain_ratio
        best_column = column
        best_divider = divider

    return best_ratio, best_column, best_divider

    
def get_best_division(level, column, gain_sum, best_column,
                      best_divider, divider):
    result_sum = 0
    for pair in level:
        info = Info(pair['table'])
        result_sum += calc_gain_ratio(pair['table'], column, divider, info)

    if result_sum > gain_sum:
        gain_sum = result_sum
        best_column = column
        best_divider = divider

    return gain_sum, best_column, best_divider


def C45_compress(level, attributes, tree, node):
    while len(level) > 0:
        gain_sum = -1
        best_column = -1
        best_divider = -1
        for column in range(len(attributes) - 1):
            if not level[0]['table'][0][column].isnumeric():
                gain_sum, best_column, best_divider = \
                    get_best_division(level, column, gain_sum,
                                    best_column, best_divider, STRING)
            else:
                for pair in level:
                    for row in pair['table']:
                        gain_sum, best_column, best_divider = \
                            get_best_division(level, column, gain_sum,
                                    best_column, best_divider, row[column])

        new_level = []
        for pair in level:
            if best_divider == STRING:
                node[pair['index']] = attributes[best_column]
                lot, freq = get_dict_str(pair['table'], best_column)        
            else:
                node[pair['index']] = attributes[best_column] + " " + \
                                   str(round(float(best_divider), 2))
                lot, freq = get_dict_num(pair['table'], best_column, best_divider)

            for key in freq:
                new_table = []
                for item in freq[key]:
                    new_table.append(pair['table'][item])

                node.append(None)
                tree.append([])
                tree[pair['index']].append((len(node) - 1, key))
                if Info(new_table) != 0:
                    new_level.append(\
                        {
                            'table': new_table,
                            'index': len(node) - 1,
                        });
                else:
                    node[-1] = new_table[0][-1]

        level = new_level


def print_results(node, tree):
    for i in range(len(node)):
        print(i, '=', node[i])
    print()

    for i in range(len(tree)):
        print(i, '|', tree[i])
    print()


def calc_used_attributes(node, attributes):
    result = set([])
    for item in node:
        if item.split()[0] in attributes:
            result.add(item)
    return len(result)
    
        
def main():
    table = []
    attributes = []
    read(table, attributes)
    #print(table, attributes, sep='\n\n')

    level = [{'table': table, 'index': 0,},]

    tree = [[],]
    node = [None,]
    C45_compress(level, attributes, tree, node)

    print_results(node, tree)
    print(calc_used_attributes(node, attributes))
    

if __name__ == "__main__":
    main()
