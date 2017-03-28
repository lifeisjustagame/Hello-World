#coding:utf_8
import xdrlib, sys
import xlrd
import xlwt

chargeValue = 0.7

workbook = xlrd.open_workbook('/home/sunqi/pythonProject/mytest/Feidata_all.xlsx')
worksheet1 = workbook.sheets()[0]

workbookNew = xlwt.Workbook()
worksheet2 = workbookNew.add_sheet('Sets', cell_overwrite_ok=True)		##用于存放符合条件的各次实验的基因名称  
worksheet3 = workbookNew.add_sheet('Intersections', cell_overwrite_ok=True)	##用于存放实验数据两两对比后相同的基因名称
worksheet4 = workbookNew.add_sheet('SetNumbers', cell_overwrite_ok=True)	##用于存放实验数据两两对比的各自源基因数目以及相同的基因数目

intRowOri = worksheet1.nrows  	#源数据行数
intColOri = worksheet1.ncols	#源数据列数

arrTitle = []	#表头，格式为set1,set2....
arrSet = [[]  for i in range(intColOri - 2)] 	#数据源前两列为名称跟基础数据，-2为了保证与实验次数同步
arrInterSection = [[] for i in range((intColOri -2) * (intColOri - 3) / 2)] 	 #所有实验数据两两对比，需要存储的集合数为n*(n-1)/2
#arrLen = [] #数组长度

for intCol in range(2, intColOri):	#从第二列开始取值为第一次的实验数据，intCol值为实验次数
	worksheet2.write(0, intCol - 2, 'set' + str(intCol - 1)) 	#定位到第一行第一列开始写第一次实验数据
	
	arrTitle.append('set' + str(intCol - 1))	#表头集合，用于后面的两两对比用
	intSheet2Row = 1
		
	for intRow in range(1, intRowOri):	#遍历所有有效数据进行数据过滤写入到对应的符合条件的set集合里
		if float(worksheet1.cell(intRow, intCol).value) / float(worksheet1.cell(intRow, 1).value) < chargeValue:
			worksheet2.write(intSheet2Row, intCol - 2, worksheet1.cell(intRow, 0).value) 	#定位行列到对应的实验次数列
			arrSet[intCol - 2].append(worksheet1.cell(intRow, 0).value)			#初始化集合数组，为了下一步的两两对比用
			intSheet2Row = intSheet2Row + 1
	
k = 0 	#用于setCommon的计数器，setCommon为符合条件的实验数据集合两两对比后相同的基因数据

for i in range(intCol - 2):	# 两两对比算法，格式为set1_VS_set2,set1_vs_set3...set1_vs_setN, set2_vs_set3...set2_vs_setn,set3....
	#print('setTile_' + str(i) + setTitle[i])
	for j in range(i + 1, intCol - 1):
		worksheet3.write(0, k, arrTitle[i] + '_VS_' + arrTitle[j])
		worksheet4.write(0, k, arrTitle[i] + '_VS_' + arrTitle[j])
		#setCommon[k] = list(set(setValue[i]).intersection(set(setValue[j]))) 	#取两个数组相同值的算法1
		arrInterSection[k] = [val for val in arrSet[i] if val in arrSet[j]]  	#取两个数组相同值的算法2
		
		worksheet4.write(1, k, "%s %s %s" %(len(arrSet[i]), len(arrSet[j]), len(arrInterSection[k])))	#两两对比的数组按照下标取对应的数组长度
		k = k + 1
		print(arrTitle[i] + '_VS_' + arrTitle[j])

for m in range(k):	#把对应的两两相比的数组相同的值写入到对应的列中
	n = 1
	for x in arrInterSection[m]:
		worksheet3.write(n, m, x)
	#for x in range(len(arrInterSection[k])):
	#	worksheet3.write(m, n, arrInterSection[k][x])
		n = n + 1

workbookNew.save('/home/sunqi/pythonProject/mytest/FeidataNew.xls')

		
