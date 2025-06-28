from collections import Counter
import csv

countries = []

with open(r'subs_out_test.csv', newline='', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)# skips header
    for row in reader:
        if row == []:
            break
        countries.append(row[3])

counter = Counter(countries)

toRemove = ["DELETED","N/A","TERMINATED","AUTO_GEN"]
for key in toRemove:
    counter.pop(key, None)

print(counter)

#######################################################

yapms_ids = {}

with open(r'sub_list_id_match.csv', newline='', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)# skips header
    for row in reader:
        if row == []:
            break
        yapms_ids[row[0]] = row[1]

##########################################################

with open(r"yapms_sub_map.json", "w") as f:
    f.write('{"map":{"country":"glb","type":"countries","year":"2020078","variant":"blank"},' +
            '"tossup":{"id":"","name":"Tossup","defaultCount":0,"margins":[{"color":"#cccccc"}]},'
            '"candidates":[{"id":"29bf84dd-2b0c-4d5d-83fe-f827df9060b8","name":"Democrat","defaultCount":0,'
            '"margins":[{"color":"#1C408C"},{"color":"#577CCC"},{"color":"#8AAFFF"},{"color":"#949BB3"}]},'
            '{"id":"5a5a5598-d34f-42ae-aaf5-48e36b197cf8","name":"Republican","defaultCount":0,'
            '"margins":[{"color":"#BF1D29"},{"color":"#FF5865"},{"color":"#FF8B98"},{"color":"#CF8980"}]}],"regions":[')
    
    # iterate through every key in yapms_ids
    # ID_HERE       from yapms_ids
    # NUM_CHANNELS  from counter
    #{"id":"ID_HERE","value":NUM_CHANNELS,"permaVal":NUM_CHANNELS,"locked":false,"permaLocked":false,
    #"disabled":false,"candidates":[{"id":"","count":NUM_CHANNELS,"margin":0}]},
    
    add_to_file = ''
    for country in yapms_ids.keys():
        disabled = 'false'
        try:
            num_channels = counter[country]
        except NameError:
            num_channels = 0
            disabled = 'true'
        
        if country == 'United States':
            try:
                num_channels += counter["Puerto Rico"]
            except NameError:
                pass
        
        if country == 'China':
            try:
                num_channels += counter["Taiwan"]
            except NameError:
                pass
            try:
                num_channels += counter["Hong Kong"]
            except NameError:
                pass
        
        if num_channels == 0:
            disabled = 'true'
        
        nc = str(num_channels)
        
        add_to_file += ('{"id":"' + str(yapms_ids[country]) + '","value":' + nc + 
                ',"permaVal":' + nc + ',"locked":' + disabled + ',"permaLocked":false,' +
                '"disabled":' + disabled + ',"candidates":[{"id":"","count":' + nc +',"margin":0}]},')
    
    f.write(add_to_file[:-1] + ']}')
