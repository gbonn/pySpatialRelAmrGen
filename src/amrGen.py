import csv
import re
import time

def FormatOutput(up_down,
                 color,
                 x_value,
                 y_value,
                 z_value,
                 full_sentence,
                 instance_id,
                 workset_id,
                 output_file):
    
    output_here_doc = """\
# ::id col_{workset_string}.{instance_string} ::date {date_time_string}
# ::snt <Architect> {full_string}
# ::save-date {date_string}::user jbonn ::file col_{workset_string}_{instance_string}.txt
(p / {up_down_string}
      :ARG0 (b / builder)
      :ARG1 (b2 / block 
            {arg_1_string})
      :ARG2 (s / space
            :location (c / cartesian-coordinate-entity :x {x_string} :y {y_string} :z {z_string})))
"""\
    
    up_down_mapping = {'picks up': 'pick-up-04',
                       'puts down': 'put-down-17'}
    
    color_mapping = {'red': ':ARG1-of (r / red-02)',
                     'orange': ':ARG1-of (o / orange)',
                     'yellow': ':ARG1-of (y / yellow-02)',
                     'green': ':ARG1-of (g / green-02)',
                     'blue': ':mod (b3 / blue)',
                     'purple': ':ARG1-of (p2 / purple-02)'}
    
    format_dict = {'up_down_string': up_down_mapping[up_down],
                   'arg_1_string': color_mapping[color],
                   'x_string': x_value,
                   'y_string': y_value,
                   'z_string': z_value,
                   'full_string': full_sentence,
                   'instance_string': instance_id,
                   'workset_string': workset_id,
                   'date_time_string': time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime()),
                   'date_string': time.strftime('%a %b %d, %Y', time.gmtime())}
    
    output_file.write(output_here_doc.format(**format_dict))
    output_file.write("\n")

builder_string_regex = '.*Builder (.*) a (\w+) block .*X:(-?\d+) Y:(-?\d+) Z:(-?\d+)'

output_file = open("../output/spacialRelAmrGen.txt", 'w')

with open('../input/action_sentences.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        searchResults = re.search(builder_string_regex, row[2])
        
        if (searchResults):
            FormatOutput(searchResults.groups()[0],
                         searchResults.groups()[1],
                         searchResults.groups()[2],
                         searchResults.groups()[3],
                         searchResults.groups()[4],
                         row[2],
                         row[1],
                         row[0],
                         output_file)

output_file.close()

print("Done.")