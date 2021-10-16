# ex: FNFJSONFIX.py "thunderstorm-hard.json"

# MADED BY RALTYRO
#
# if you delete this i will #### you and ####
# no regrets

import sys
import os
import json

FNF_EXT = ".json"
linethingylol = "---------------------------------------------------------"

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
def decode(file,strict,keys,noDup,reArrange,isLISSupport,isCBPMSupport,engineType,engineVers):
	file = json.loads(open(file).read().strip())
	file = file if isinstance(file["song"],str) else file["song"]
	
	chart = {}
	sections = []
	changeBPMS = []
	changeLIS = []
	notes = []
	notesMHS = []
	
	for i in file:
		if file[i] == None:
			del file[i]
		else:
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
		time = 0
		lastBPM = chart["bpm"]
		lastLIS = file["notes"][0]["lengthInSteps"] if isLISSupport and isinstance(file["notes"][0],list) and "lengthInSteps" in file["notes"][0]["lengthInSteps"] and isinstance(file["notes"][0]["lengthInSteps"],int) else 16
		stepCrochet = (((60 / float(lastBPM)) * 1000) / 4)
		for v in file["notes"]:
			section = {
				"mustHitSection":v["mustHitSection"] if isinstance(v["mustHitSection"],bool) else True,
				"lengthInSteps":v["lengthInSteps"] if isinstance(v["lengthInSteps"],int) else 16
			} if strict else v.copy()
			if not isLISSupport and "lengthInStep" in section: section["lengthInSteps"] = 16
			if not isCBPMSupport:
				if "bpm" in section: del section["bpm"]
				if "changeBPM" in section: del section["changeBPM"]
			
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
			
			stepCrochet = (((60 / float(lastBPM)) * 1000) / 4)
			if "startTime" in v and "endTime" in v:
				section["startTime"] = int(time)
				time += stepCrochet * lastLIS
				section["endTime"] = int(time)
			
		notes.sort(key=lambda v: v[0])
	
	notesPOS1 = {}
	notesPOS2 = {}
	
	i = 0
	for v in notes:
		section = -1
		time = -67
		stepCrochet = (((60 / float(changeBPMS[0])) * 1000) / 4)
		while clamp(v[0],0,9999999999) > time:
			section += 1
			stepCrochet = (((60 / float(changeBPMS[-1] if section >= len(changeBPMS) else changeBPMS[section])) * 1000) / 4)
			time += stepCrochet * (changeLIS[-1] if section >= len(changeLIS) else int(changeLIS[section]))
		
		if section > len(sections)-1:
			while len(sections)-1 < section:
				sections.append(sections[-1].copy())
		
		if (reArrange): v[0] = int((v[0]/(stepCrochet/4))*(stepCrochet / 4))
		
		if sections[section]["mustHitSection"] != notesMHS[i]:
			v[1] = v[1]-keys if v[1] > keys-1 else v[1]+keys
		
		plr = True if v[1] >= keys-1 else False
		# im lazy
		if plr:
			if not(str(v[0]) in notesPOS1): notesPOS1[str(v[0])] = []
			if listFind(notesPOS1[str(v[0])],v[1]) == -1 or not noDup:
				sections[section]["sectionNotes"].append(v)
				notesPOS1[str(v[0])].append(v[1])
		else:
			if not(str(v[0]) in notesPOS2): notesPOS2[str(v[0])] = []
			if listFind(notesPOS2[str(v[0])],v[1]) == -1 or not noDup:
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
	
	if engineType == 1 and engineVers == 1:
		if "eventObjects" in file:
			chart["eventObjects"] = []
			for v in file["eventObjects"]:
				event = v.copy()
				if event["type"] == "BPM Change" or event["type"] == "Scroll Speed Change":
					event["value"] = capnumber(event["value"],3)
				
				event["position"] = round(event["position"])
				
				chart["eventObjects"].append(event)
				
	
	return chart

def main():
	if len(sys.argv) < 2:
		usage()
	
	infile = sys.argv[1]
	infile_name, infile_ext = os.path.splitext(os.path.basename(infile))
	if infile_ext == FNF_EXT:
		
		engine_type = input(linethingylol + "\nWhich engine where this chart maded from? (IMPORTANT)\n Kade Engine/1\n FNF/2\n Others/3\n\n")
		engine_type = 1 if (engine_type.find("k") != -1 or engine_type.find("1") != -1) else 2 if (engine_type.find("fnf") != -1 or engine_type.find("2") != -1) else 3

		print("Selected Option : " + ("Kade Engine" if engine_type == 1 else "FNF" if engine_type == 2 else "Others"))

		# fuck you kade /j
		engine_vers = 0
		if engine_type == 1:
			engine_vers = input(linethingylol + "\nIs your Kade Engine Version is above 1.6? (IMPORTANT)\n Yes/1\n No/2\n\n")
			engine_vers = 0 if (engine_vers.find("No") != -1 or engine_vers.find("2") != -1) else 1

			print("Selected Option : " + ("Yes" if engine_vers else "No"))
		
		encode_type = input(linethingylol + "\nWhich json encode type would you like? (Default is Compact)\n Compact/1 (Recommended, Not Readable, Usually below 20kb file size)\n Clean/2 (Readable, Usually above 50kb file size)\n\n").lower()
		encode_type = 2 if (encode_type.find("clean") != -1 or encode_type.find("2") != -1) else 1
		
		print("Selected Option : " + ("Clean" if encode_type == 2 else "Compact"))
		
		strict = input(linethingylol + "\nDo you want the chart to be stricted? (No Custom Values, Default is Stricted)\n Yes/1\n No/2\n\n").lower()
		strict = False if (strict.find("No") != -1 or strict.find("2") != -1) else True
		
		print("Selected Option : " + ("Stricted" if strict else "Not Stricted"))
		
		noDup = input(linethingylol + "\nDo you want your charts to not have Duplicated Notes? (Default is Yes)\n Yes/1\n No/2\n\n").lower()
		noDup = False if (noDup.find("No") != -1 or noDup.find("2") != -1) else True
		
		print("Selected Option : " + ("Yes" if noDup else "No"))
			
		reArrange = input(linethingylol + "\nDo you want your charts to be Rearranged (by 4 stepCrochets)? (Default is Yes)\n Yes/1\n No/2\n\n").lower()
		reArrange = False if (reArrange.find("No") != -1 or reArrange.find("2") != -1) else True

		print("Selected Option : " + ("Yes" if reArrange else "No"))
		
		keys = input(linethingylol + "\nWhat's the Chart Keys? (Number here, Default is 4)\n\n")
		keys = 4 if keys.strip() == '' else int(keys)
		
		print("Selected Option : " + str(keys))
		
		isLISSupport = False
		isCBPMSupport = True

		if engine_type != 1: isCBPMSupport = False
		if engine_type == 1 and engine_vers == 0: isCBPMSupport = False

		if engine_type != 1:
			isLISSupport = input(linethingylol + "\nIs your chart have lengthInStep Support? (If you're using Kade Engine, pick no, otherwise yes, Default is Yes)\n Yes/1\n No/2\n\n")
			isLISSupport = False if (isLISSupport.find("No") != -1 or isLISSupport.find("2") != -1) else True

			print("Selected Option : " + ("Yes" if isLISSupport else "No"))
		if not isCBPMSupport:
			isCBPMSupport = input(linethingylol + "\nIs your chart have changeBPM Support? (Some of the engine doesn't support this, pick no if it doesnt support changeBPM, otherwise yes, Default is Yes)\n Yes/1\n No/2\n\n")
			isCBPMSupport = False if (isCBPMSupport.find("No") != -1 or isCBPMSupport.find("2") != -1) else True

			print("Selected Option : " + ("Yes" if isCBPMSupport else "No"))
		
		print(linethingylol)
		
		try:
			final = decode(infile,strict,keys,noDup,reArrange,isLISSupport,isCBPMSupport,engine_type,engine_vers)
			print(str(final) + "\n" + linethingylol)

			if not os.path.exists("_FNFJSONCLEAN-results"): os.mkdir("_FNFJSONCLEAN-results")

			outfile = open("_FNFJSONCLEAN-results/" + infile_name + FNF_EXT,'w')
			if encode_type == 1:
				outfile.write(json.dumps({"song":final},separators=(',', ':')))
			else:
				outfile.write(json.dumps({"song":final},separators=(',', ':'),sort_keys=True,indent=4).replace("    ","	"))
			outfile.close()
		except:
			print("Something went wrong while trying to clean '" + par + "/" + dir + "/" + file + "'")
			input("Plesae check the json if its a fnf song format, otherwise send the json to Raltyro!\n")
		else:
			input("Finished! Check the folder '" + "_FNFJSONCLEAN-results" + "'\nFeel free to exit this")
		print(linethingylol)
		
	else:
		usage()

if __name__ == "__main__":
	main()
