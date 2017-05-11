import re
from array import *
f = open('./rbc_components_3.ttl','r');

main_device = "Streetlight"
in_main_device = False 
sub_class_list = []
rel_tmp_list = []
rel_tmp_sc_arr = []
val_tmp_sc_arr = []
for line in f:
  
  if re.search("^"+"rbccps:"+str(main_device), line):
     if re.search("owl:Class", line):
        in_main_device = True 
        break;
parsing_restriction_field = False
while in_main_device is True:
  for line in f:

    if re.search("^\s+\[", line):
       parsing_restriction_field = True
       rel_tmp = None

    if re.search("^\s+"+"owl:onProperty", line): #rel field. If the range for this is an owl:Class then we have to have 
       #parse that class to provide metadata values in val field. Else val field will
       #be empty (empty means to be filled at on-boarding time)
       rel_tmp = line.split()[1]
       rel_tmp_sc_arr.append(-1)      
       val_tmp_sc_arr.append(-1)      
  
    if (parsing_restriction_field is True) and (re.search("owl:onClass", line) or re.search("owl:onDataRange", line) or re.search("owl:hasValue", line)):
       if re.search("owl:onClass", line):
          sub_class_list.append(line.split()[1])
          #rel_tmp = rel_tmp + ":"+line.split()[1]
          rel_tmp = line.split()[1]
          rel_tmp_sc_arr.pop()
          rel_tmp_sc_arr.append(len(sub_class_list)-1)      

       if re.search("owl:hasValue", line):
          #print line.split()
          val_tmp = line.split()[1]
          val_tmp_sc_arr.pop()
          val_tmp_sc_arr.append(val_tmp)      

       rel_tmp_list.append(rel_tmp)
       
       parsing_restriction_field = False

    if re.search("\.$", line):
       in_main_device = False
       break;

  #split_line = line.split()
f.close()
rel_tmp_list_1 = rel_tmp_list
val_tmp_sc_arr_1 = val_tmp_sc_arr
print val_tmp_sc_arr

rel_tmp_list = []
rel_tmp_list_11 = []

val_tmp_list = []
val_tmp_list_11 = []

cntr = 0;
for subc in sub_class_list:
  rel_tmp_list = []
  rel_tmp_list_11 = []
  in_subc = False
  parsing_restriction_field = False
  f = open('./rbc_components_3.ttl','r');

  for line in f:
    if re.search("^"+str(subc), line):
       if re.search("owl:Class", line):
          in_subc = True 
          break;
  while in_subc is True:
      for line in f:
        if re.search("^\s+\[", line):
           parsing_restriction_field = True
           rel_tmp = None
    
        if re.search("^\s+"+"owl:onProperty", line):
           rel_tmp = line.split()[1]
           val_tmp = -1  

        if (parsing_restriction_field is True) and (re.search("owl:onClass", line) or re.search("owl:onDataRange", line) or re.search("owl:hasValue", line)):
           if re.search("owl:onClass", line):
              sub_class_list.append(line.split()[1])
              #rel_tmp = rel_tmp + ":"+line.split()[1]
              rel_tmp = line.split()[1]
           if re.search("owl:hasValue", line):
              val_tmp = line.split()[1]

           rel_tmp_list.append(rel_tmp)
           rel_tmp_list_11.append(val_tmp)
           parsing_restriction_field = False
        if re.search("\.$", line):
           in_subc = False
           break;

  f.close()
  val_tmp_list.append(rel_tmp_list)
  val_tmp_list_11.append(rel_tmp_list_11)
  cntr = cntr+1


#print val_tmp_list[0]
#print rel_tmp_list_1
#index = [i for i, s in enumerate(sub_class_list) if "caseTemperature" in s]
print val_tmp_list_11

f1 = open('sl_data_model.txt','w');
cntr = 0;

for rel in rel_tmp_list_1:
 
   f1.write("   {")
   f1.write("\n")
   f1.write("    \"rel\":"+"\""+rel_tmp_list_1[cntr]+"\""+",")
   f1.write("\n")
   if rel_tmp_sc_arr[cntr] < 0:
      if val_tmp_sc_arr_1[cntr] < 0:
        f1.write("    \"val\":")
      if val_tmp_sc_arr_1[cntr] >= 0:
        f1.write("    \"val\": "+str(val_tmp_sc_arr_1[cntr]))

      f1.write("\n")
   
   if rel_tmp_sc_arr[cntr] >= 0:
      #f1.write("  \"rel\":"+"\""+rel_tmp_list_1[cntr]+"\"")
      #f1.write("\n")
      #f1.write("\"val\":")
      f1.write("    \"val\":")
      f1.write(" [")
      f1.write("\n")
      cntr1 = 0;
      for field in val_tmp_list[rel_tmp_sc_arr[cntr]]:
          val_field = val_tmp_list_11[rel_tmp_sc_arr[cntr]][cntr1]
          f1.write("       {")
          f1.write("\n")
          if val_field < 0:
            f1.write("          "+"\"rel\":"+"\""+field+"\""+",")
            f1.write("\n")
            f1.write("          "+"\"val\":")
            #f1.write("        "+field+":")
          if val_field >= 0:
            f1.write("          "+"\"rel\":"+"\""+field+"\""+",")
            #f1.write("        "+field+": "+str(val_field))
            f1.write("\n")
            f1.write("          "+"\"val\": "+str(val_field))
          f1.write("\n")
          if cntr1 != len(val_tmp_list[rel_tmp_sc_arr[cntr]]) - 1:
            f1.write("       },")
          else :
            f1.write("       }")
          f1.write("\n")
          cntr1 = cntr1+1

      f1.write("      ]")
      f1.write("\n")

   if cntr != len(rel_tmp_list_1)-1:
     f1.write("   },")
   else :
     f1.write("   }")

   cntr = cntr + 1
   f1.write("\n")

f1.close()
