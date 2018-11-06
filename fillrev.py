import json
from psqldb import GetGameInfo

# names = []

# Creates and writes to master_deals json file
# with open("Names.json", "r") as rfile:
#     cot = json.load(rfile);
#     arrn = cot["Names"]
#     print(len(arrn))
#     rfile.close()
#
# for n in arrn[750:797]:
#     names.append(n)
#
# ob = YoutubeSearch()
#
# name_rev = []
#
# count = 750
# for i in names:
#     link = ob.search(i + " game review")
#     name_rev.append([i, link])
#     print("{} {} {}".format(count, i ,link))
#     count = count + 1
#
# # Creates and writes to master_deals json file
# with open("RevMap16.json", "w") as newfile:
#     json.dump({"Mapping": name_rev}, newfile)
#
# wholemap = []
#
# for i in range(1, 17):
#     # Creates and writes to master_deals json file
#     with open("RevMap{}.json".format(i), "r") as rfile:
#         cot = json.load(rfile);
#         arrn = cot["Mapping"]
#         rfile.close()
#
#     for map in arrn:
#         wholemap.append(map)
#
# # Creates and writes to master_deals json file
# with open("AllRev.json", "r") as newfile:
#     json.dump({"RevMap": wholemap}, newfile)


inst = GetGameInfo()

with open("AllRev.json", "r") as rfile:
    cot = json.load(rfile);
    arrn = cot["RevMap"]
    rfile.close()



for mapp in arrn:
    inst.dupe_remover(mapp[0], mapp[1])
