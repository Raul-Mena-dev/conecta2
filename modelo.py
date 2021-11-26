import pkg_resources
import numpy as np
import joblib



vectorizer = joblib.load(pkg_resources.resource_filename('modelo', 'app/model/vectorizer.joblib'))
model = joblib.load(pkg_resources.resource_filename('modelo', 'app/model/model.joblib'))


def _get_profane_prob(prob):
  return prob[1]

def prediccion(texts):
  return model.predict(vectorizer.transform(texts))

def prediccion_prob(texts):
  return np.apply_along_axis(_get_profane_prob, 1, model.predict_proba(vectorizer.transform(texts)))