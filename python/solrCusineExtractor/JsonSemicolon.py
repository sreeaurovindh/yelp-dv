json_file_in = "D:\\Dropbox\\dv\\review_input\\food_reviews.json"
json_file_out = "D:\\Dropbox\\dv\\review_input\\food_reviews_out.json"

input_file = open(json_file_in, 'r')
out_file = open(json_file_out,'w')
out_file.write("[\n")
for line in input_file:
    line = line.rstrip() # here
    final= line+','+'\n'
    out_file.write(final)
out_file.write("]\n")
out_file.close()
input_file.close()
    
