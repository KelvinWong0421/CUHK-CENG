'''
Description of the Grading Scheme

1. Connectivity Check
1.1 This is the preliminary and mandatory check.
1.2 Full marks (30) are awarded only if the result completely passes this check.
1.3 If there is a violation, the score for this part is calculated as 15 x r, where r is the ratio of
    (no. of pins with valid connections) / (no. of pins in total)
1.4 The evaluation process halts here if the connectivity check fails. There will be no scores awarded for the subsequent checks.
1.5 This is compulsory for PG students (0 marks for passing this part).

2. Capacity Check
2.1 This check follows and is dependent on the successful completion of the Capacity Check.
2.2 A full score of 30 points is granted for a complete pass.
2.3 In case of a violation, the score is determined by 15 x r, where r is the ratio of 
    (no. of grid edges used without violation) / (no. of grid edges used in total).
2.4 For PG students, full score is 45 and partial score is 25 x r.

3. Load Check
3.1 This check follows and is dependent on the successful completion of the Capacity Check.
3.2 The grading scheme of load check is similar to capacity check, while r is the ratio of 
    (no. of taps without violation) / (no. of taps in total)

4. Final Scoring Notes
4.1 It is only after fully passing all three checks that the final cost is considered.
'''
# py eval.py --input test2.in --output test2.out --plot true
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='CENG 4120 Clock Tree Synthesis Evaluator')
parser.add_argument('--input', required=True)
parser.add_argument('--output', default='')
parser.add_argument('--plot', default='false')
args = parser.parse_args()

max_time = 0
max_load = 0
size = 0
capacity = 0
num_pins = 0
num_taps = 0

global_max = 0
global_min = 1e9

# for undergraduates:
score_weight = [30, 15, 30, 15]

#for graduates:
# score_weight = [0, 0, 45, 25]

pins = []
taps = []

# grader
print('Reading {}...'.format(args.input))
with open(args.input) as f:
    line = f.readline()
    while len(line) > 0:
        data = line.strip().split(' ')
        if data[0] == 'MAX_RUNTIME':
            max_time = int(data[1])
        elif data[0] == 'MAX_LOAD':
            max_load = int(data[1])
        elif data[0] == 'GRID_SIZE':
            size = int(data[1])
        elif data[0] == 'CAPACITY':
            capacity = int(data[1])
        elif data[0] == 'PINS':
            num_pins = int(data[1])
            for i in range(num_pins):
                data = f.readline().strip().split(' ')
                pins.append([int(data[2]), int(data[3])])
        elif data[0] == 'TAPS':
            num_taps = int(data[1])
            for i in range(num_taps):
                data = f.readline().strip().split(' ')
                taps.append([int(data[2]), int(data[3])])
        
        line = f.readline()

assigned = [False for i in range(num_pins)]
tap_pins = [[] for i in range(num_taps)]
tap_edges = [[] for i in range(num_taps)]
pin_delay = [0 for i in range(num_pins)]
valid_pins = [1 for i in range(num_pins)]
score = 0

if args.output != '':
    print('Reading {}...'.format(args.output))
    with open(args.output) as f:
        line = f.readline()
        while len(line) > 0:
            data = line.strip().split(' ')
            if data[0] == 'TAP':
                tap = int(data[1])
            elif data[0] == 'PINS':
                num_tap_pins = int(data[1])
                for i in range(num_tap_pins):
                    data = f.readline().strip().split(' ')
                    assert(data[0]=='PIN')
                    tap_pins[tap].append(int(data[1]))
            elif data[0] == 'ROUTING':
                num_edges = int(data[1])
                for i in range(num_edges):
                    data = f.readline().strip().split(' ')
                    assert(data[0]=='EDGE')
                    tap_edges[tap].append([
                        (int(data[1]), int(data[2])),
                        (int(data[3]), int(data[4]))
                    ])
            else:
                print('Invalid Format')
                exit(0)
            line = f.readline()
    
    for t_pins in tap_pins:
        for pin in t_pins:
            if assigned[pin]:
                print('Error: pin {} is assigned to more than one tap.'.format(pin))
                valid_pins[pin] = 0
            assigned[pin] = True
    for i, a in enumerate(assigned):
        if not a:
            print('Error: pin {} is not assigned to any tap.'.format(i))
            valid_pins[pin] = 0
    
    length = 0
    tap_used = []
    tap_skew = []
    for t in range(num_taps):
        used = [[[0 for y in range(size)] for x in range(size)] for d in range(2)]
        for edge in tap_edges[t]:
            if edge[0][0] == edge[1][0]:
                x = edge[0][0]
                l = min(edge[0][1], edge[1][1])
                h = max(edge[0][1], edge[1][1])
                for y in range(l, h):
                    if used[1][x][y] == 0:
                        used[1][x][y] = 1
                        length += 1
            elif edge[0][1] == edge[1][1]:
                y = edge[0][1]
                l = min(edge[0][0], edge[1][0])
                h = max(edge[0][0], edge[1][0])
                for x in range(l, h):
                    if used[0][x][y] == 0:
                        used[0][x][y] = 1
                        length += 1
            else:
                print('Error: edge {} {} {} {} is neither horizontal or vertical.'
                      .format(edge[0][0], edge[0][1], edge[1][0], edge[1][1]))
                exit(0)
            
            if min(edge[0][0], edge[0][1], edge[1][0], edge[1][1]) < 0 or \
               max(edge[0][0], edge[0][1], edge[1][0], edge[1][1]) >= size:
                print('Error: edge {} {} {} {} is out of boundary.'
                      .format(edge[0][0], edge[0][1], edge[1][0], edge[1][1]))
                exit(0)
        tap = taps[t]
        arrival_time = [[1e9 for y in range(size)] for x in range(size)]
        
        to_update = [[tap, 0, used, arrival_time]]
        i = 0
        while i < len(to_update):
            cur = to_update[i][0]
            time = to_update[i][1]
            used = to_update[i][2]
            arrival_time = to_update[i][3]
            if time < arrival_time[cur[0]][cur[1]]:
                arrival_time[cur[0]][cur[1]] = time
                if cur[0] > 0 and used[0][cur[0] - 1][cur[1]]:
                    to_update.append([[cur[0] - 1, cur[1]], time+1, used, arrival_time])
                if cur[0] < size - 1 and used[0][cur[0]][cur[1]]:
                    to_update.append([[cur[0] + 1, cur[1]], time+1, used, arrival_time])
                if cur[1] > 0 and used[1][cur[0]][cur[1] - 1]:
                    to_update.append([[cur[0], cur[1] - 1], time+1, used, arrival_time])
                if cur[1] < size - 1 and used[1][cur[0]][cur[1]]:
                    to_update.append([[cur[0], cur[1] + 1], time+1, used, arrival_time])
            i += 1
            
        min_time = 1e9
        max_time = 0
        for p in tap_pins[t]:
            pin = pins[p]
            if arrival_time[pin[0]][pin[1]] == 1e9:
                print('Error: pin {} is not connected to tap {}'.format(p, t))
                valid_pins[p] = 0
                # exit(0)
            pin_delay[p] = arrival_time[pin[0]][pin[1]]
            min_time = min(min_time, arrival_time[pin[0]][pin[1]])
            max_time = max(max_time, arrival_time[pin[0]][pin[1]])
        global_max = max(global_max, max_time)
        global_min = min(global_min, min_time)

        tap_skew.append(max_time - min_time)
        tap_used.append(used)

    valid_pins_num = valid_pins.count(1)
    if valid_pins_num == num_pins:
        print('Passed: Connectivity Check. (%d)' % score_weight[0])
        score += score_weight[0]
    else:
        cur_score = valid_pins_num / num_pins * score_weight[1]
        print('Partially Passed: Connectivity Check. %d/%d, (%.2f)' % (valid_pins_num, num_pins, cur_score))
        score += cur_score
        exit(0)
    
    overall_used = [[[0 for y in range(size)] for x in range(size)] for d in range(2)]
    max_used = 0
    max_used_edge = []
    for t in range(num_taps):
        for d in range(2):
            for x in range(size):
                for y in range(size):
                    overall_used[d][x][y] += tap_used[t][d][x][y]


    used_edge_num = sum(value > 0 for layer in overall_used for row in layer for value in row)
    invalid_edge_num = sum(value > capacity for layer in overall_used for row in layer for value in row)

    if invalid_edge_num==0 :
        print('Passed: Capacity Check. (%d)' % score_weight[2])
        score += score_weight[2]
    else:
        cur_score = (used_edge_num - invalid_edge_num) / used_edge_num * score_weight[3]
        print('Partially Passed: Capacity Check. %d/%d, (%.2f)' % (used_edge_num - invalid_edge_num, used_edge_num, cur_score))
        score += cur_score

    
    valid_taps = 0
    for i in range(num_taps):
        if len(tap_pins[i]) <= max_load:
            valid_taps += 1
    
    if valid_taps == num_taps:
        print('Passed: Load Check. (%d)' % score_weight[2])
        score += score_weight[2]
    else:
        cur_score = valid_taps/num_taps*score_weight[3]
        print('Partially Passed: Load Check. %d/%d, (%.2f)' % (valid_taps, num_taps, cur_score))
        score += cur_score


    # uncomment the line below to print the delay of each pin
    # print(pin_delay)
    
    print('Score = {:.2f}/90'.format(score))
    print('(Remaining score will be determined later)')
    
    if score != 90:
        print('INVALID DESIGN!')
    print('Final cost = {}'.format((global_max-global_min)*num_taps + length))
    print('    Max delay = {}, min delay = {}'.format(global_max, global_min))
    print('    Total length = {}.'.format(length))

    
    
            
# visualizer
if args.plot.lower() == 'true':
    plot_name = args.input.replace('.in', '.pdf')
    print('Plotting...')
    cmap = plt.get_cmap('nipy_spectral')
    offset_width = min((num_taps - 1) * 0.10, 1.0)
    min_offset = 0
    fig = plt.figure(figsize=(min(size/4, 25), min(size/4, 25)))
    for t in range(num_taps):
        color = cmap(t/num_taps)
        offset = min_offset + offset_width * (t / max(num_taps-1, 1))
        # plot edges
        if args.output != '':
            for edge in tap_edges[t]:
                plt.plot(
                    [edge[0][0] + offset, edge[1][0] + offset], 
                    [edge[0][1] + offset, edge[1][1] + offset],
                    color=color,
                )
        else:
            offset = 0
        # plot taps
        plt.scatter([taps[t][0] + offset], [taps[t][1] + offset], marker='o', 
                    s=50, color=color, linewidths=0, zorder=3)
        # plot pins
        xs = []
        ys = []
        s = []
        for p in tap_pins[t]:
            xs.append(pins[p][0] + offset)
            ys.append(pins[p][1] + offset)
            s.append(20)
        plt.scatter(xs, ys, marker='s', s=s, color=color, linewidths=0, zorder=3)
    # plot unassigned pins 
    xs = []
    ys = []
    s = []
    for i, pin in enumerate(pins):
        if assigned[i]:
            continue
        xs.append(pin[0] + 0.5)
        ys.append(pin[1] + 0.5)
        s.append(20)
    plt.scatter(xs, ys, marker='s', s=s, color='black', linewidths=0, zorder=3)
    # plot grids
    plt.xticks([x for x in range(size + 1)])
    plt.yticks([y for y in range(size + 1)])
    plt.gca().grid()
    # plt.legend()
    plt.savefig(plot_name)
    plt.show()
    
        
