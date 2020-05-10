from flask import Flask,request,url_for,render_template,redirect,session,jsonify
from flask_wtf import FlaskForm
from wtforms import FileField
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import joblib
from PIL import Image
import io

def return_predictions(model,image):
	if image.mode != "RGB":
		image = image.convert("RGB")
	adding_dimensions=np.expand_dims(image,axis=0)
	prediction=model.predict(adding_dimensions)
	if prediction>0.5:
		return 'uninfected'
	else:
		return 'parasitized'
	return prediction



class Form(FlaskForm):
	image=FileField('Image')




app=Flask(__name__)
app.config["SECRET_KEY"]="This is Secret"


model=load_model('C:\\Users\\yousuf\\Downloads\\image.h5')


@app.route('/',methods=['POST','GET'])
def form():
	form=Form()
	if request.method=='POST':
		if request.files.get("image"):
			image1 = request.files["image"].read()
			image = Image.open(io.BytesIO(image1))
			image=image.resize((130,130))
			results=return_predictions(model,image)
			# print(image)
			return render_template('prediction.html',results=results)
	return render_template('home.html',form=form)


if __name__ == '__main__':
	app.run(debug=True)