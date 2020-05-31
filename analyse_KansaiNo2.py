import numpy as np
import astropy.time as Time
import matplotlib.pyplot as plt
import re

iFileName = "g4.areaAvgTimeSeries.OMNO2d_003_ColumnAmountNO2CloudScreened.20100101-20200527.134E_34N_136E_35N.csv"

numHeadFilter = re.compile('^\d*')
lenNumHead = lambda x : numHeadFilter.match(x).span()[1]
numTailFilter = re.compile('[-+]?\d*.\d*[e]?[-+]?\d*$')
fillValue = -1
noValue = np.nan

lst = [{"Date":[],"DoY":[], "Value":[]}]
t_prev = 2.0 # any value greater than start_day
start_day = 0.5 # start day of the analysis year in the format of the fraction of year (0.0~1.0)

# Skip Headers
with open(iFileName, "r") as ifile:
	ll = ifile.readline()
	while(lenNumHead(ll) != 4):
		if ll[0:10] == "Fill Value":
			fillValue = float(ll.split(',')[-1])
			#fillValue = numTailFilter.search(ll).group(0)
			print("fillValue = {0}".format(fillValue))
		ll = ifile.readline()
	while ll:
		data = ll.split(',')
		if float(data[1]) != fillValue:
			date = Time.Time(data[0]+"T12:00:00",format="isot")
			tt = date.jyear % 1
			if t_prev < start_day and tt >= start_day:
				lst.append({"Date":[],"DoY":[], "Value":[]})
			lst[-1]["Date"].append(date)
			lst[-1]["DoY"].append(((tt + start_day)%1)+start_day)
			lst[-1]["Value"].append(float(data[1]))
			t_prev = tt
		ll = ifile.readline()


fontsize = 18

fig, ax = plt.subplots(figsize=(18,6),dpi=100)
lastId = len(lst)-1
for ii, dd in enumerate(lst):
	tt = dd["DoY"]
	vv = dd["Value"]
	if ii != lastId:
		cc = [1-ii/40.0,0.75-ii/40.0,0.75-ii/40.0]
		style = "-"
	else:
		cc = [0,0,0]
		style = "x-"
	img = ax.plot(tt,vv,style, color=cc, linewidth=2)
plt.yscale("log")
plt.ylim([1e15, 1e17])
plt.xlim([start_day, start_day+1])
ax.set_xticks(np.arange(start_day,start_day+1.1,0.1), minor=True)
plt.tick_params(labelsize=fontsize)
ax.grid(which="both", axis="both", color="grey", alpha=0.8,linestyle="--", linewidth=0.5)
plt.title("KeiHanShin Area-Averaged Daily Column Density of NO$_{2}$ (cm$^{-2}$)", fontsize=fontsize)
plt.xlabel("Year", fontsize=fontsize)
plt.ylabel("Column Density of NO$_{2}$ (cm$^{-2}$)", fontsize=fontsize)
plt.savefig("NO2_YearAnalysis.png")
plt.show()

pltDate = []
pltVal  = []

dt = 0.01 # about 3 days

for t0, vv in zip(lst[-1]["DoY"], lst[-1]["Value"]):
	sum_v = 0.0
	sum_v2 = 0.0
	cnt = 0
	for dd in lst[:-1]:
		for jj, tt in enumerate(dd["DoY"]):
			if min(abs(tt-t0), abs(tt-t0-1)%1, abs(tt-t0+1)%1) <= dt:
				sum_v = sum_v + dd["Value"][jj]
				sum_v2 = sum_v2 + dd["Value"][jj]**2
				cnt = cnt + 1
	mean = sum_v/cnt
	std = np.sqrt(sum_v2/cnt - mean**2)
	pltDate.append(t0)
	pltVal.append((vv-mean)/std)

fig, ax = plt.subplots(figsize=(18,6),dpi=100)
img = ax.plot(pltDate, pltVal, "x-", color="k", linewidth=2)
plt.tick_params(labelsize=fontsize)
plt.ylim([-5, 5])
plt.xlim([0.5,1.5])
ax.set_xticks(np.arange(start_day,start_day+1.1,0.1), minor=True)
ax.grid(which="both", axis="both", color="grey", alpha=0.8,linestyle="--", linewidth=0.5)
plt.title("KeiHanShin Area-Averaged Daily Normalized Column Density of NO$_{2}$", fontsize=fontsize)
plt.xlabel("Year since 2019 Jan. 01", fontsize=fontsize)
plt.ylabel("Normalized Logarithm of Column Density", fontsize=fontsize)
plt.savefig("NO2_2019Jul-2020Jun.png")
plt.show()

print("[Decl.] WHO, Emergency of Int. Concern  : 2020 Jan. 30 ({0:8.3f})".format(Time.Time("2020-01-30T12:00:00").jyear))
print("[Decl.] Cancelation of Class in Japan   : 2020 Feb. 27 ({0:8.3f})".format(Time.Time("2020-02-27T12:00:00").jyear))
print("[Decl.] State of Emergency at Osaka&Kobe: 2020 Apr.  7 ({0:8.3f})".format(Time.Time("2020-04-07T12:00:00").jyear))
print("[Decl.] State of Emergency at Kyoto     : 2020 Apr. 16 ({0:8.3f})".format(Time.Time("2020-04-16T12:00:00").jyear))
print("Golden Week (Japanese Holiday Week)     : 2020 May   1 ({0:8.3f})".format(Time.Time("2020-05-01T12:00:00").jyear))
print("[Lift ] State of Emergency at Kyoto     : 2020 May  14 ({0:8.3f})".format(Time.Time("2020-05-14T12:00:00").jyear))
print("[Lift ] State of Emergency at Osaka&Kobe: 2020 May  21 ({0:8.3f})".format(Time.Time("2020-05-21T12:00:00").jyear))

for tt, vv in zip(pltDate, pltVal):
	print("{0:8.3f} : {1:6.3f}".format(tt,vv))