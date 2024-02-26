import ujson as json

# this list will store all objects before writing into the output file.
json_list = list()

with open('../data/finance_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

    for x in data:
        # this is the new structure we want to use for OCI Generative AI Service
        new_object =  {
            "prompt": x['instruction'],
            "completion": x['output']
        }
        json_list.append(new_object)

print('Converting {} prompt-response pairs'.format(len(json_list)))
# for every element in json_list, write everything into a txt file line by line
with open('../data/output.jsonl', 'w') as output_file:
    for x in json_list:
        # avoid those elements with non-utf8 characters. e.g. 🐥
        # we have a huge dataset so these cases are not that important.
        try:
            output_file.write("{}\n".format(x))
        except Exception as e:
            #print(x)
            pass
            
