from flask import Flask, render_template, request
import jsonify
import math
import requests
import io
import base64
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
prediction_text={}
app = Flask(__name__)
@app.route('/',methods=['GET'])
def Home():
    prediction_text={}

    return render_template('index.html',prediction_text={})
@app.route("/predict", methods=['POST'])
def predict():
    prediction_text={}

    if request.method == 'POST':
        mass=float(request.form['mass'])#getting mass from html frontend input
        m_unit=request.form['m_unit']#storing unit of mass
        if(m_unit=='g'):
            mass=mass/1000 #converting it to SI units
        elif(m_unit=='lb'):
            mass=mass/2.205
        k=float(request.form['k'])#getting stiffness coefficient from html frontend input
        k_unit=request.form['k_unit']
        if(k_unit=='N/mm'):
            k=k*1000#converting it to SI units
        if(k_unit=='lbf/in'):
            k=k*175.1268#converting it to SI units
        DR=float(request.form['DR'])
        free_forced=request.form['free/forced']
        if(free_forced=='forced'):
            omega=float(request.form['omega'])
        Wn=math.sqrt(k/mass) #calculating Cicular frequency
        Fn=(7/44)*Wn #calculating Natural frequency
        T=(1/Fn) #calculating Period of oscilattion
        Cc=2*mass*Wn #calculating Critical damping
        C=DR*Cc #calculating Damping factor
        Wd=Wn*(math.sqrt(1-(DR*DR))) #calculating Damped natural angular frequency
        Fd=Fn*(math.sqrt(1-(DR*DR))) #calculating Damped natural frequency
        if(DR==0):
            Q='infinity' #damping ratio 0 case 
        else:
            Q=1/(2*DR) #calculating Quality factor
        t = np.arange(0.1, 3, 0.01) #creationg a list of numbers 
        if(free_forced=='forced'):
            k=4*(DR)**2
            # Create figure 
            fig, ax = plt.subplots() 
            #q=(7/44)**2
            # log x and y axis 
            ax.loglog(t,np.sqrt((1+k*t*t)/((1-t*t)**2+(k*t*t))),linewidth=1, basex = 10) #simplified equation where TR is function of frequesncy ratio
            ax.grid(True,which="both")  
            plt.ylabel('Transmissiblity [TR]',fontsize=5)
            plt.xlabel('Frequency Ratio(Ω/fn)',fontsize=10)
            ax.set_title('Transmissiblity[y] vs Frequency Ratio Graph[x](log-log)') 
            pngImage = io.BytesIO()
            FigureCanvas(fig).print_png(pngImage)
            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        
        if(free_forced=='forced'):#calculating  Transmissibility for forced vibrations 
            p=omega/Fn
            q=4*(DR)**2
            TR=math.sqrt((1+q*p*p)/((1-p*p)*(1-p*p)+(q*p*p))) #Calculating Transmissiblity
        

        #storing the results in a dictionary     
        prediction_text = {"Wn":round(Wn,2),"Fn":round(Fn,2),"T":round(T,2),"Cc":round(Cc,2),"C":round(C,2),"Wd":round(Wd,2),"Fd":round(Fd,2),"Q":round(Q,2)}
        if(free_forced=='forced'):
            prediction_text["TR"]=round(TR,2)
            prediction_text["image"]=pngImageB64String
        else:
            prediction_text["TR"]='---'
        return render_template('index.html',prediction_text=prediction_text)
            
        
    else:
        return render_template('index.html',prediction_text={})

if __name__=="__main__":
    app.run(debug=True)

