# map_chart maker
# works with https://www.mapchart.net
# can pick ANY map that is at country 
# doesnt split uk, us or canada

# next plans: html page

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
print(counter)
# prints dict of countries

unique_array = []
for item in countries:
    if (item == "N/A") or (item == "DELETED") or (item == "AUTO_GEN") or (item == "TERMINATED"):
        continue
    
    if item not in unique_array:
        unique_array.append(item)

print(len(unique_array)) 

###########################

dict_of_stats = {"1": [[],'#084081'], "2 - 3": [[],'#00ff00'], "4 - 5": [[],'#d40000'], 
                 "6 - 10": [[],'#ffff00'], "11 - 25": [[],'#f781bf'], "26 - 100": [[],'#5b5bf6'], 
                 "101 - 250":[[],'#ff7f00'], "251 - 500": [[],'#724a19'], 
                 "501 - 1000": [[],'#c2a1e7'], "1000+": [[],'#9c2b70'] }

add_to_array = ''

for item in unique_array:
    
    x = counter[item]
    
    if x == 1:
        add_to_array = "1"
    elif x <= 3:
        add_to_array = "2 - 3"
    elif x <= 5:
        add_to_array = "4 - 5"
    elif x <= 10:
        add_to_array = "6 - 10"
    elif x <= 25:
        add_to_array = "11 - 25"
    elif x <= 100:
        add_to_array = "26 - 100"
    elif x <= 250:
        add_to_array = "101 - 250"
    elif x <= 500:
        add_to_array = "251 - 500"
    elif x <= 1000:
        add_to_array = "501 - 1000"
    else:
        add_to_array = "1000+"
    
    item = item.replace(' ', '_')
    dict_of_stats[add_to_array][0].append(item)

print(dict_of_stats)

###########################

add_to_file = ''
add_countries = ''
colour = '#000000' # hex code

with open(r"sub_map_2.txt", "w") as f:
    f.write('{"groups":{')
    
    for key in dict_of_stats.keys():
        if not dict_of_stats[key]:
            continue # if empty
        
        colour = dict_of_stats[key][1]
        add_to_file += '"' + colour + '":{"label":"'+ key + '","paths":['
        
        for c in dict_of_stats[key][0]:
            add_countries += '"' + c + '",'
        
        add_to_file += add_countries[:-1] + ']},'
        add_countries = ''
    
    
    #################################
    
    f.write(add_to_file[:-1])
    
    f.write('},"title":"","hidden":["USA_Alaska","USA_Wisconsin","USA_Montana","USA_Minnesota","USA_Washington"'
            + ',"USA_Idaho","USA_North_Dakota","USA_Michigan","USA_Maine","USA_Ohio","USA_New_Hampshire","USA_New_York",'
            + '"USA_Vermont","USA_Pennsylvania","USA_Arizona","USA_California","USA_New_Mexico","USA_Texas","USA_Louisiana",'
            + '"USA_Mississippi","USA_Alabama","USA_Florida","USA_Georgia","USA_South_Carolina","USA_North_Carolina",'
            + '"USA_Virginia","USA_Washington_DC","USA_Maryland","USA_Delaware","USA_New_Jersey","USA_Connecticut",'
            + '"USA_Rhode_Island","USA_Massachusetts","USA_Oregon","USA_Hawaii","USA_Utah","USA_Wyoming","USA_Nevada",'
            + '"USA_Colorado","USA_South_Dakota","USA_Nebraska","USA_Kansas","USA_Oklahoma","USA_Iowa","USA_Missouri",'
            + '"USA_Illinois","USA_Kentucky","USA_Arkansas","USA_Tennessee","USA_West_Virginia","USA_Indiana",'
            + '"Scotland","Wales","England","Northern_Ireland","Yukon_CA","Prince_Edward_Island_CA","New_Brunswick_CA",'
            + '"Ontario_CA","British_Columbia_CA","Alberta_CA","Saskatchewan_CA","Manitoba_CA","Quebec_CA","Nunavut_CA",'
            + '"Newfoundland_and_Labrador_CA","Northwest_Territories_CA","Nova_Scotia_CA"],"background":"#ffffff",'
            + '"borders":"#000","legendFont":"Century Gothic","legendFontColor":"#000","legendBorderColor":"#00000000",'
            + '"legendBgColor":"#00000000","legendWidth":150,"legendBoxShape":"square","areBordersShown":true,"defaultColor":"'
            + '#d1dbdd","labelsColor":"#6a0707","labelsFont":"Arial","strokeWidth":"medium","areLabelsShown":false,'
            + '"uncoloredScriptColor":"#ffff33","v6":true,"usaStatesShown":false,"canadaStatesShown":false,"splitUK":false,'
            + '"legendPosition":"bottom_left","legendSize":"medium","legendTranslateX":"0.00","legendStatus":"show",'
            + '"scalingPatterns":true,"legendRowsSameColor":true,"legendColumnCount":1}')
            
# checkpoints

# 1,    2 - 3, 4 - 5, 6 - 10, 11 - 25, 26 - 100, 101 - 250, 251 - 500, 501 - 1000, 1000+
# dark, green,  red   yellow   pink     light    orange      brown      lilac     purple
# blue                                   blue

# 14 colours (+ bg white)
# default gray (#d1dbdd)

########################

# dark blue #084081
# regular green #00ff00
# red #ff0000
# yellow #ffff00
# pink #f781bf
# light blue #abd9e9
# orange #ff7f00
# brown #724a19
# lilac #c2a1e7
# purple #9c2b70
# light green #c7e9b4
# regular blue #0000ff
# dark green #238b45
