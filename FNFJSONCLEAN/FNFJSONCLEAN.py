# ex: FNFJSONCLEAN.py "hard-2-break.json"
#  or just drop the json into this script

# MADED BY RALTYRO
#
# if you delete this i will #### you and ####
# no regrets

import sys
import os
import json

FNF_EXT = ".json"

# FUNCTIONS!!!

def clamp(n,smallest,largest):return max(smallest, min(n, largest))

def capnumber(number,cap):
	cap = clamp(cap,1,256)
	a = str(number).split(".")
	n = float(a[0] + "." + (a[1])[0:(cap if len(a[1])>=cap else len(a[1]))]) if len(a) > 1 else a[0]
	return n

def listFind(list,i): return next((x for x in list if x == i), -1)

# functions ends no fun here :pensive:

def usage():
	print("Usage: {} [chart_file]".format(sys.argv[0]))
	print("bruuh where the json dude")
	sys.exit(1)

excludeKey = ['sections']
def decode(file,strict,keys):
	file = json.loads(open(file).read())
	file = file if isinstance(file["song"],str) else file["song"]
	
	chart = {}
	sections = []
	changeBPMS = []
	changeLIS = []
	notes = []
	notesMHS = []
	
	for i in file:
		yes = True
		if strict:
			if isinstance(file[i],str):
				if file[i].strip() == '': yes = False
		
		if listFind(excludeKey,i) == -1 and not(isinstance(file[i],list)) and yes:chart[i] = file[i]
		
	if "bpm" in chart and (isinstance(chart["bpm"],float) or isinstance(chart["bpm"],int)): chart["bpm"] = capnumber(chart["bpm"],3)
	else: chart["bpm"] = 160
	
	if "speed" in chart and (isinstance(chart["speed"],float) or isinstance(chart["speed"],int)): chart["speed"] = capnumber(chart["speed"],2)
	else: chart["speed"] = 2
	
	if isinstance(file["notes"],list) and len(file["notes"]) > 0:
		lastBPM = chart["bpm"]
		lastLIS = file["notes"][0]["lengthInSteps"] if isinstance(file["notes"][0],list) and "lengthInSteps" in file["notes"][0]["lengthInSteps"] and isinstance(file["notes"][0]["lengthInSteps"],int) else 16
		for v in file["notes"]:
			section = {
				"mustHitSection":v["mustHitSection"] if isinstance(v["mustHitSection"],bool) else True,
				"lengthInSteps":v["lengthInSteps"] if isinstance(v["lengthInSteps"],int) else 16
			} if strict else v.copy()
			sections.append(section)
			
			if "changeBPM" in v and isinstance(v["changeBPM"],bool) and v["changeBPM"] and "bpm" in v and isinstance(v["bpm"],float):
				lastBPM = capnumber(v["bpm"],3)
				changeBPMS.append(lastBPM)
			else:
				changeBPMS.append(lastBPM)
			
			if "lengthInSteps" in v and isinstance(v["lengthInSteps"],int):
				lastLIS = int(v["lengthInSteps"])
				changeLIS.append(lastLIS)
			else:
				changeLIS.append(lastLIS)
			
			if isinstance(v["sectionNotes"],list):
				for v2 in v["sectionNotes"]:
					sectionNote = [v2[0],v2[1],v2[2]] if strict else v2.copy()
					sectionNote[0] = int(v2[0])
					sectionNote[1] = int(v2[1])
					sectionNote[2] = int(v2[2])
					
					notesMHS.append(v["mustHitSection"])
					notes.append(sectionNote)
			
			if "sectionNotes" in section:
				section["sectionNotes"].clear()
			else:
				section["sectionNotes"] = []
			
		notes.sort(key=lambda v: v[0])
	
	notesPOS1 = {}
	notesPOS2 = {}
	
	i = 0
	for v in notes:
		section = -1
		time = -1
		stepCrochet = (((60 / float(changeBPMS[0])) * 1000) / 4)
		while clamp(v[0],0,9999999999) > time:
			section += 1
			stepCrochet = (((60 / float(changeBPMS[-1] if section >= len(changeBPMS) else changeBPMS[section])) * 1000) / 4)
			time += stepCrochet * (changeLIS[-1] if section >= len(changeLIS) else int(changeLIS[section]))
		
		if section > len(sections)-1:
			while len(sections)-1 < section:
				sections.append(sections[-1].copy())
		
		v[0] = int((v[0]/(stepCrochet/6))*(stepCrochet / 6))
		
		if sections[section]["mustHitSection"] != notesMHS[i]:
			v[1] = v[1]-keys if v[1] >= keys-1 else v[1]+keys
		
		plr = True if v[1] >= keys-1 else False
		# im lazy
		if plr:
			if not(str(v[0]) in notesPOS1): notesPOS1[str(v[0])] = []
			if listFind(notesPOS1[str(v[0])],v[1]) == -1:
				sections[section]["sectionNotes"].append(v)
				notesPOS1[str(v[0])].append(v[1])
		else:
			if not(str(v[0]) in notesPOS2): notesPOS2[str(v[0])] = []
			if listFind(notesPOS2[str(v[0])],v[1]) == -1:
				sections[section]["sectionNotes"].append(v)
				notesPOS2[str(v[0])].append(v[1])
		
		i += 1
	
	loopwithoutnothing = 0
	lastLIS = sections[0]["lengthInSteps"] if "lengthInSteps" in sections[0] and isinstance(sections[0]["lengthInSteps"],int) else 16
	lastMHS = sections[0]["mustHitSection"] if "mustHitSection" in sections[0] and isinstance(sections[0]["mustHitSection"],bool) else True
	for v in sections:
		loopwithoutnothing += 1
		LIS = v["lengthInSteps"] if "lengthInSteps" in v and isinstance(v["lengthInSteps"],int) else 16
		MHS = v["mustHitSection"] if "mustHitSection" in v and isinstance(v["mustHitSection"],bool) else True
		if ("changeBPM" in v and isinstance(v["changeBPM"],bool) and v["changeBPM"]) or LIS != lastLIS or MHS != lastMHS or len(v["sectionNotes"]) > 0: loopwithoutnothing = 0
		lastLIS = LIS
		lastMHS = MHS
	
	loopwithoutnothing = clamp(loopwithoutnothing-1,0,99999999999)
	if loopwithoutnothing > 0:
		#section = len(sections)-loopwithoutnothing
		for i in range(loopwithoutnothing):
			sections.pop();
	
	chart["notes"] = sections
	
	return chart

def main():
	if len(sys.argv) < 2:
		usage()
	
	infile = sys.argv[1]
	infile_name, infile_ext = os.path.splitext(os.path.basename(infile))
	if infile_ext == FNF_EXT:
		
		#chart_type = input("Which engine does this chart maded from? \n(auto, kade, psych, fnf)")
		
		encode_type = input("\nWhich json encode type would you like?\n Compact/1 (Recommended, Not Readable, Usually below 20kb file size)\n Clean/2 (Readable, Usually above 50kb file size)\n\n").lower()
		encode_type = 2 if (encode_type.find("clean") != -1 or encode_type.find("2") != -1) else 1
		
		print("Selected Option : " + ("Clean" if encode_type == 2 else "Compact"))
		
		strict = input("\nDo you want the chart to be stricted? (No Custom Values)\n Yes/1\n No/2\n\n")
		strict = False if (strict.find("No") != -1 or strict.find("2") != -1) else True
		
		print("Selected Option : " + ("Stricted" if strict else "Not Stricted"))
		
		keys = input("\nWhat's the Chart Keys?\n (Input Number Here)\n")
		keys = 4 if keys.strip() == '' else int(keys)
		
		print("Selected Option : " + str(keys))
		
		print("\n\n\n")
		
		final = decode(infile,strict,keys)
		print(final)
		
		if not os.path.exists("FNFJSONCLEAN-results"): os.mkdir("FNFJSONCLEAN-results")
		
		outfile = open("FNFJSONCLEAN-results/" + infile_name + ".json",'w')
		if encode_type == 1:
			outfile.write(json.dumps({"song":final},separators=(',', ':')))
		else:
			outfile.write(json.dumps({"song":final},separators=(',', ':'),sort_keys=True,indent=4).replace("    ","	"))
		outfile.close()
	else:
		usage()

if __name__ == "__main__":
	main()
