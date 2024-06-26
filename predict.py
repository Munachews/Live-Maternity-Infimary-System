from joblib import dump, load
import pandas as pd 
import numpy as np
import os
from pathlib import Path

save_path = "saved_model/"
model_name = "model"

BASEDR = Path(__file__).resolve().parent.parent

pathy = os.path.join(BASEDR, 'home/')

#patient1 = [ 32, 120, 90, 7.5, 98]

#patient1 = np.array([patient1])

#GDRAT_abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), str(save_path + model_name + ".joblib"))

def prod(patient1):

	try:
		# Load Trained Model
		patient1 = np.array([patient1])
		clf = load(str(pathy + save_path + model_name + ".joblib"))
		result = clf.predict(patient1)
		print(result)

		return result

		
	except Exception as e:
		print(e)
		return e