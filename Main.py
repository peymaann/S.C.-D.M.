import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess
import sys


if len(sys.argv) > 1:
	n_col = int(sys.argv[1])
else :
	n_col = 1

if len(sys.argv) > 2:
	n_row = int(sys.argv[2])
else :
	n_row = 1 

if len(sys.argv) > 2:
	fingers = int(sys.argv[3])
else :
	fingers = 2 

if len(sys.argv) > 3:
	scale = int(sys.argv[4])
else :
	scale = 0 


N_X = n_col + fingers
N_Y = n_row
#fingers = 2
dead_row = np.linspace(1,N_X,fingers)

print("N_X is: " + str(n_col))
print("N_Y is: " + str(n_row))
print("Fingers : " + str(fingers))
os.system("rm output" + str(n_col) + "_" + str(n_row) + ".txt")
#---------------------------------------------------
#Sheet resistance
RTs = 10 # Corresponding to ITO
RBs = 0.25 # COrresponding to silver
RT = np.ones((N_X, N_Y)) * RTs 
RB = np.ones((N_X, N_Y)) * RBs 
R_END = 0.1 # final contact resistance
R1 = RTs *  (150E-6/10e-3/scale)
R3 = RBs *  (150E-6/10e-3/scale)
R2 = 0.5 * min([RTs,RBs]) * (1e-6/10e-3/scale)
RC = R1+R2+R3
print(f"Rc is : {RC}")
Ratio = (N_X*(1e-2/scale)-(fingers-2)*(150e-6+150e-6+100e-6))/N_X/(1e-2/scale)
print(f"Ratio is : {Ratio}")
#---------------------------------------------------
#Parameter from fitting 
if scale==1:
	Iph = 0.015765197486583272
	Rs = 1.0000073738046325e-06
	Rsh = 6480.111340092841
	Is1 = 1.6177782741066065e-07
	Is2 = 2.925123460664602e-24
	a1 = 2.9823939857304103
	a2 = 3.887137562577057
	print("using original values 1*1")
elif scale == 2 :
	Iph = 0.003954718061760653
	Rs = 1.4218252819315427e-06
	Rsh = 6628.942712897443
	Is1 = 1.734605660603478e-08
	Is2 = 2.3899679774587772e-23
	a1 = 2.777910782578937
	a2 = 3.5926661153326473
	print("using scaled 3 values 2*2")
elif scale == 3:
	Iph = 0.0017599179090575807
	Rs = 1e-06
	Rsh = 11621.440957251038
	Is1 = 5.487227512798278e-09
	Is2 = 1.5121440649883335e-25
	a1 = 2.703452898389991
	a2 = 2.2939997715582114
	print("using scaled 3 values 3*3")
elif scale == 4:
	Iph = 0.0009886834857480095
	Rs = 1.9546481806580838e-06
	Rsh = 26461.93599574155
	Is1 = 4.325638738349857e-09
	Is2 = 3.9070409555463645e-25
	a1 = 2.7773482460710883
	a2 = 2.9042594230891834
	print("using scaled 4 values 4*4")
elif scale == 5:
	Iph = 0.0006415059389331048
	Rs = 1e-06
	Rsh = 10265.819327319905
	Is1 = 4.334141673655807e-11
	Is2 = 1.2956406527450505e-26
	a1 = 2.0778658789409956
	a2 = 4.0
	print("using scaled 5 values 5*5")	
else:
	print("use resonalbe value for scale")
Iph *= Ratio
IS1 = Is1
IS2 = Is2
N1 = a1
N2 = a2
Rs = np.ones((N_X, N_Y)) * Rs 
I = np.ones((N_X, N_Y)) * Iph 
Rsh = np.ones((N_X, N_Y)) * Rsh
#---------------------------------------------------

acative_region = np.ones((N_X, N_Y))

for i in range(len(dead_row)):
	acative_region[(int(dead_row[i])-1),:]  = np.zeros(N_Y)


plt.figure()
plt.imshow(acative_region.T, cmap='viridis') 
plt.colorbar() 
plt.title('Active area map')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.savefig("active_region"+ str(n_col) + "_" + str(n_row) + "_" +str(fingers)+".png")


V_max = 3
V_steps = 0.025

S = 10000
#-------------------------------------------------------------------------------------
# Generating basic model for the solar cell

text = "* Test Simulation - operation point analysis \n"


# Generating forming the 2d map of the soalr cells

elem = 0;

for i_y in range(N_Y):
	i_finger = 0
	for i_x in range(N_X):
		text += "\n"
		elem += 1
		elem_node = ((elem-1)*5)+1
		if acative_region[i_x,i_y]:
			#print(f"entering active  region{i_x},{i_y}")
			text += "D1_" + str(elem) + " " + str(elem_node+S) + " mid" + str(elem_node) + " diode_model_1 \n"
			text += "D2_" + str(elem) + " " + str(elem_node+S) + " mid" + str(elem_node) + " diode_model_2 \n"
			text += "I_"  + str(elem) + " mid" + str(elem_node) + " "  + str(elem_node+S)  + " " + str(I[i_x,i_y]) +  "\n"
			text += "Rsh_" + str(elem) + " mid" + str(elem_node) + " " + str(elem_node+S) + " " + str(Rsh[i_x,i_y]) + "\n"
			text += "Rs_" + str(elem) + " " + str(elem_node) + " mid" + str(elem_node) + " " + str(Rs[i_x,i_y]) + "\n"
				

			
			if acative_region[i_x-1,i_y]:
				node1 = elem_node -2
				node2 = elem_node -2 + S
				text += "RTL" + str(elem) + " " + str(elem_node) + " " + str(node1)+ " " + str(RT[i_x,i_y]) + "\n"
				text += "RBL" + str(elem) + " " + str(elem_node+S) + " " + str(node2)+ " " + str(RB[i_x,i_y]) + "\n"
			#else:
				#node1 = elem_node + 1
				#node2 = elem_node + 1 +S
				#text += "RBL" + str(elem) + " " + str(elem_node+S) + " " + str(node2)+ " " + str(RB[i_x,i_y]) + "\n"

			
			if acative_region[i_x+1,i_y]:
				node1 = elem_node +3
				node2 = elem_node +3 + S
				text += "RTR" + str(elem) + " " + str(elem_node) + " " + str(node1)+ " " + str(RT[i_x,i_y]) + "\n"
				text += "RBR" + str(elem) + " " + str(elem_node+S) + " " + str(node2)+ " " + str(RB[i_x,i_y]) + "\n"
			#else:
				#node1 = elem_node + 3
				#node2 = elem_node + 3 +S
				#text += "RTR" + str(elem) + " " + str(elem_node) + " " + str(node1)+ " " + str(RT[i_x,i_y]) + "\n"
			if i_y < N_Y -1:
				node1 = elem_node + 4
				node2 = elem_node + 4 +S
				text += "RTT" + str(elem) + " " + str(elem_node) + " " + str(node1)+ " " + str(RT[i_x,i_y]) + "\n"
				text += "RBT" + str(elem) + " " + str(elem_node+S) + " " + str(node2)+ " " + str(RB[i_x,i_y]) + "\n"
				
			if i_y > 0:
				node1 = ((elem -1 - N_X) * 5) + 5
				node2 = ((elem -1 - N_X) * 5) + 5 +S
				text += "RTB" + str(elem) + " " + str(elem_node) + " " + str(node1)+ " " + str(RT[i_x,i_y]) + "\n"
				text += "RBB" + str(elem) + " " + str(elem_node+S) + " " + str(node2)+ " " + str(RB[i_x,i_y]) + "\n"
		else:
			if i_x == 0: # connection to one side of the main conacts
				node1 = "out"
				node2 = elem_node + 5 + S			
				text += "RL" + str(elem) + " " + str(elem_node) + " " + str(node1)+ " " + str(R_END) + "\n"
				text += "RR" + str(elem) + " " + str(elem_node) + " " + str(node2)+ " " + str(R_END) + "\n"
			elif i_x == N_X-1: # connection to other side of the main conacts
				node1 = elem_node-5
				node2 = "gnd"			
				text += "RL" + str(elem) + " " + str(elem_node) + " " + str(node1)+ " " + str(R_END) + "\n"
				text += "RR" + str(elem) + " " + str(elem_node) + " " + str(node2)+ " " + str(R_END) + "\n"	
			else:  # connection of the subcells
				node1 = elem_node-5
				node2 = elem_node+5+S			
				text += "RL" + str(elem) + " " + str(elem_node) + " " + str(node1)+ " " + str(RC) + "\n"
				text += "RR" + str(elem) + " " + str(elem_node) + " " + str(node2)+ " " + str(RC) + "\n"
				if i_y > 0: #bottom resistors
					node1 = elem_node + 2
					node2 = elem_node + 2 + S 
					text += "RTB" + str(elem) + " " + str(elem_node) + " " + str(node1)+ " " + str(RC) + "\n"
					text += "RBB" + str(elem) + " " + str(elem_node) + " " + str(node2)+ " " + str(RC) + "\n"
				if i_y < N_Y-1: #top resistors
					node1 = elem_node + 4
					node2 = elem_node + 4 + S 
					text += "RTT" + str(elem) + " " + str(elem_node) + " " + str(node1)+ " " + str(RC) + "\n"
					text += "RBT" + str(elem) + " " + str(elem_node) + " " + str(node2)+ " " + str(RC) + "\n"







#text += "X 1 out out out out 11 gnd gnd gnd gnd solarcell II=0.03 IS=1E-19 RB=0.1 RT=10 RSH=10k "
text += "\n"

text += "V0 out gnd 0 \n"
text += "\n"
text += ".model diode_model_1 D (IS={" + str(IS1)+"} N={"+str(N1)+"}) \n"
text += ".model diode_model_2 D (IS={" + str(IS2)+"} N={"+str(N2)+"}) \n"
text += "\n"


text += ".control \n"
text += "op \n"
text += "dc V0 0 " + str(V_max) + " " + str(V_steps) + "\n"
text += "print i(V0) \n"
text += "\n"
text += "wrdata temp/output" + str(n_col) + "_" + str(n_row) + "_" +str(fingers) + ".txt i(V0)"
elem = 0;
for i_y in range(N_Y):
	for i_x in range(N_X):
		elem += 1
		elem_node = ((elem -1) * 5) + 1
		text += " v(" + str(elem_node) + ")"

text += "\n \n"



text += ".endc \n"
text += ".end \n"


 
with open('circuit.cir', 'w') as file:
    file.write(text)











