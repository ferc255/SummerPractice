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
        relation = 'less' if int(row[column]) < int(divider) else 'greater'
        
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


def update_best_ratio(table, column, info, best_ratio, best_column,
                      best_divider, divider):
    info_x, split_info = Info_x(table, column, divider)
    gain_ratio = info - info_x
    if split_info != 0:
        gain_ratio /= split_info
        #pass

    if gain_ratio > best_ratio:
        best_ratio = gain_ratio
        best_column = column
        best_divider = divider

    return best_ratio, best_column, best_divider

    
def C45(table, attributes, tree, node, idx):
    tree.append([])
    info = Info(table)
    if info == 0:
        node[idx] = table[0][-1]
        return

    best_ratio = -1
    best_column = -1
    best_divider = -1
    for column in range(len(attributes) - 1):
        if not(table[0][column].isnumeric()):
            best_ratio, best_column, best_divider = \
                update_best_ratio(table, column, info, best_ratio,
                                  best_column, best_divider, STRING)
        else:
            for row in table:
                best_ratio, best_column, best_divider = \
                    update_best_ratio(table, column, info, best_ratio,
                                      best_column, best_divider, row[column])

    if best_divider == STRING:
        node[idx] = attributes[best_column]
        lot, freq = get_dict_str(table, best_column)        
    else:
        node[idx] = attributes[best_column] + " " + str(best_divider)
        lot, freq = get_dict_num(table, best_column, best_divider)

    for key in freq:
        new_table = []
        for item in freq[key]:
            new_table.append(table[item])
            
        node.append(None)
        tree[idx].append((len(node) - 1, key))
        C45(new_table, attributes, tree, node, len(node) - 1)

        
def main():
    table = []
    attributes = []
    read(table, attributes)
    #print(table, attributes, sep='\n\n')

    tree = []
    node = [None,]
    C45(table, attributes, tree, node, 0)

    for i in range(len(node)):
        print(i, '=', node[i])
    print()

    for i in range(len(tree)):
        print(i, '|', tree[i])
    print()
    

if __name__ == "__main__":
    main()
