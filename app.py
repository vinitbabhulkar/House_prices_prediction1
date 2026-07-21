import os
import pickle
import numpy as np
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Construct absolute path to the model file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'linear_model.pkl')

# Load the trained scikit-learn linear regression model
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)
