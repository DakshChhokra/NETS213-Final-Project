import pandas as pd
import operator
import csv

hit2_output = pd.read_csv("../data/agg_hit2_input.csv")
key = pd.read_csv("../data/agg_key.csv")

print(hit2_output)
print(key)

answer_key = {}

for index, row in key.iterrows():
    answer_key[row["id"]] = (row["c1"], row["c2"], row["c3"])

#aggregate_output[id] = {percentage_correct:2/3, }
aggregate_labels = {}
for index, row in hit2_output.iterrows():
    id_num = row["id"]
    rc1, rc2, rc3 = answer_key[id_num]
    c1, c2, c3 = row["comprehension_1"], row["comprehension_2"], row["comprehension_3"]

    acc1 = 1 if rc1 == c1 else 0
    acc2 = 1 if rc2 == c2 else 0
    acc3 = 1 if rc3 == c3 else 0
    accuracy = (acc1 + acc2 + acc3)/3

    current_label = row["asshole_validator"]

    if id_num not in aggregate_labels:
        curr_dict = {"YTA": 0, "NTA": 0, "ES":0, "NA":0}
    else:
        curr_dict = aggregate_labels[id_num]
    
    curr_dict[current_label] += accuracy

    aggregate_labels[id_num] = curr_dict

print(aggregate_labels)

final_labels = {}

for key in aggregate_labels.keys():
    curr_dict = aggregate_labels[key]
    biggest_label = max(curr_dict.items(), key=operator.itemgetter(1))[0]
    confidence_num  = curr_dict[biggest_label]
    confidence_den = curr_dict["YTA"] + curr_dict["NTA"] + curr_dict["ES"] + curr_dict["NA"]
    confidence  = confidence_num / confidence_den
    
    final_labels[key] = {"label": biggest_label, "confidence": confidence}

print(final_labels)


with open('../data/agg_hit_2_output.csv','w+') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(["id", "label", "confidence"])
        for key in final_labels:
            csv_out.writerow((key, final_labels[key]["label"], final_labels[key]["confidence"]))
