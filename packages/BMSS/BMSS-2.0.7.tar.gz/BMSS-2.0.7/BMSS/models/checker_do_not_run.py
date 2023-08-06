import numpy as np
def model_TestModel_LogicGate_ORgate_DelayActivation_DelayActivation(y, t, params):
	Inde1 = y[0]
	Indi1 = y[1]
	Inde2 = y[2]
	Indi2 = y[3]
	mRNA1 = y[4]
	Pep1  = y[5]
	mRNA2 = y[6]
	Pep2  = y[7]
	mRNA3 = y[8]
	Pep3  = y[9]

	syn_mRNA1 = params[0]
	syn_mRNA2 = params[1]
	syn_mRNA3 = params[2]
	deg_mRNA  = params[3]
	syn_Pep   = params[4]
	deg_Pep   = params[5]
	Pepmax    = params[6]
	Km1       = params[7]
	Km2       = params[8]
	state1    = params[9]
	state2    = params[10]

	dInde1 = -(Inde1/(Inde1+Km1))*Inde1
	dIndi1 = (Inde1/(Inde1+Km1))*Inde1
	dInde2 = -(Inde2/(Inde2+Km2))*Inde2
	dIndi2 = (Inde2/(Inde2+Km2))*Inde2
	dmRNA1 = syn_mRNA1*(Indi1)*(state1) - (deg_mRNA *mRNA1)
	dPep1  = (syn_Pep*mRNA1) - (deg_Pep*Pep1)
	dmRNA2 = syn_mRNA2*(Indi2)*(state2) - (deg_mRNA *mRNA2)
	dPep2  = (syn_Pep*mRNA2) - (deg_Pep*Pep2)
	dmRNA3 = (syn_mRNA3*((Pep1+Pep2)/Pepmax))-(deg_mRNA *mRNA3)
	dPep3  = (syn_Pep*mRNA3)-(deg_Pep*Pep3)

	return np.array([dInde1, dIndi1, dInde2, dIndi2, dmRNA1, dPep1, dmRNA2, dPep2, dmRNA3, dPep3])

Inde1,Indi1,Inde2,Indi2,mRNA1,Pep1,mRNA2,Pep2,mRNA3,Pep3,syn_mRNA1,syn_mRNA2,syn_mRNA3,deg_mRNA,syn_Pep,deg_Pep,Pepmax,Km1,Km2,state1,state2= np.random.rand(21)*10

Inde1,Indi1,Inde2,Indi2,mRNA1,Pep1,mRNA2,Pep2,mRNA3,Pep3,syn_mRNA1,syn_mRNA2,syn_mRNA3,deg_mRNA,syn_Pep,deg_Pep,Pepmax,Km1,Km2,state1,state2= list(map(float, [Inde1,Indi1,Inde2,Indi2,mRNA1,Pep1,mRNA2,Pep2,mRNA3,Pep3,syn_mRNA1,syn_mRNA2,syn_mRNA3,deg_mRNA,syn_Pep,deg_Pep,Pepmax,Km1,Km2,state1,state2]))

y = [Inde1,Indi1,Inde2,Indi2,mRNA1,Pep1,mRNA2,Pep2,mRNA3,Pep3]

t = 0
dt = 1e-3

params = syn_mRNA1,syn_mRNA2,syn_mRNA3,deg_mRNA,syn_Pep,deg_Pep,Pepmax,Km1,Km2,state1,state2

y = y + dt*model_TestModel_LogicGate_ORgate_DelayActivation_DelayActivation(y, t, params)

y = y + dt*model_TestModel_LogicGate_ORgate_DelayActivation_DelayActivation(y, t, params)