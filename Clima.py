import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
import requests
import warnings

def getLoc():

    try:

        #Define la URL de la API de IP Geolocation
        url = "https://ipinfo.io/json"

        #Realiza la solicitud GET a la API
        response = requests.get(url)

        #Verifica si la solicitud fue exitosa (código de estado HTTP 200)
        if response.status_code == 200:

            #Convierte la respuesta JSON a un diccionario de Python
            data = response.json()

            #Accede a los datos de ubicación, como la latitud y longitud
            ubicacion = data["loc"].split(",")
            latitud = ubicacion[0]
            longitud = ubicacion[1]

            return latitud,longitud,data['city']
    
        else:
    
            messagebox.showerror(message="Error al obtener la ubicación.",title="Error")
            ventana.quit()

    except requests.exceptions.RequestException as e:
    
        messagebox.showerror(message=f"Error al realizar la solicitud HTTP: {e}",title="Error")
        ventana.quit()

def getWeather(latitud,longitud):

    #Define la URL de la API y tu clave de API
    url = "https://api.openweathermap.org/data/2.5/weather"
    apiKey = "tu_clave_de_api_aqui"  #Reemplaza "tu_clave_de_api_aqui" con tu clave de API

    latitud,longitud,ciudad = getLoc()

    #Define los parámetros de la solicitud, como la ubicación y el formato de respuesta
    params = {
        
        "lat": latitud,
        "lon": longitud,
        "appid": apiKey,
        "units": "metric",  #Puedes cambiar a "imperial" para Fahrenheit
        "lang": "es"  #Configura el idioma de la respuesta
    }

    try:

        #Realiza la solicitud GET a la API
        response = requests.get(url, params=params)
        response.raise_for_status()  #Verifica si hay errores en la respuesta HTTP

        #Convierte la respuesta JSON a un diccionario de Python
        data = response.json()

        #Accede a los datos relevantes, como la temperatura actual y la descripción del clima
        temperatura = data["main"]["temp"]
        temperaturaMinima = data["main"]["temp_min"]
        temperaturaMaxima = data["main"]["temp_max"]
        descripcionClima = data["weather"][0]["description"]
        humedad = data["main"]["humidity"]

        #Regresa la información del clima
           
        return temperatura,temperaturaMinima,temperaturaMaxima,humedad,descripcionClima.title()

    except requests.exceptions.RequestException as e:

        messagebox.showerror(message=f"Error al realizar la solicitud HTTP: {e}",title="Error")
        ventana.quit()

    except KeyError as e:

        messagebox.showerror(message=f"Error al procesar la respuesta JSON: {e}",title="Error")
        ventana.quit()

#Debido a palabras en la descripción del clima se puede poner una imagen que corresponda a la descripción
def typeWeather(description,noche):
    
    if 'sol' in description:

        clima = 'Sunny'

    elif 'despejado' in description:

        clima = 'Clear'         

    elif 'muy' in description and 'nub' in description:

        clima = 'Cloud'

    elif 'nebl' in description or 'nieb' in description:

        clima = 'Foggy'

    elif 'lluv' in description:

        clima = 'Rain'

    elif 'torm' in description:

        clima = 'Storm'

    elif 'nieve' in description:

        clima = 'Snow'

    else:

        clima = 'Clouds'

    if noche:
        
        clima += '2.png'

    else:

        clima += '.png'

    return clima

def actualizarHora():

    #Obtener la hora actual
    horaActual = datetime.now().strftime("%H:%M:%S")
    #Actualizar el texto del Label con la hora actual
    labelHora.config(text=f"Hora: {horaActual}")
    #Llamar a la función actualizarHora() nuevamente después de 1 segundo
    ventana.after(1000, actualizarHora)

#Crea una instancia de la ventana
ventana = tk.Tk()

ventana.title('Clima')
ventana.configure(background='#DDD') 
ventana.geometry('700x300')
warnings.filterwarnings("ignore", category=DeprecationWarning) #PIL muestra una advertencia de alteración de imagen en la interfaz, pero no afecta nada
noche = False

if int(datetime.now().strftime("%H")) >= 6 and int(datetime.now().strftime("%H")) < 12:

    saludo = 'Buenos Días'

elif int(datetime.now().strftime("%H")) >= 12 and int(datetime.now().strftime("%H")) < 19:

    saludo = 'Buenas Tardes'

else:

    saludo = 'Buenas Noches'
    noche = True

latitud,longitud,ciudad = getLoc()
tempC,temperaturaMinima,temperaturaMaxima,humedad,descripcion = getWeather(latitud,longitud)

l = tk.Label(ventana,text=saludo,fg='#000',bg='#DDD',font=('Garamond bold', 15, 'bold italic'))
l.place(x=10,y=30)
l = tk.Label(ventana,text=f"Ciudad: {ciudad}",fg='#000',bg='#DDD',font=('Garamond bold', 15, 'bold italic'))
l.place(x=10,y=60)
labelHora = tk.Label(ventana,text="Hora:",fg='#000',bg='#DDD',font=('Garamond bold', 15, 'bold italic'))
labelHora.place(x=10,y=90)
l = tk.Label(ventana,text=f"Temperatura: {tempC} °C | {(round(float(tempC)*(9/5) + 32,2))} °F",fg='#000',bg='#DDD',font=('Garamond bold', 15, 'bold italic'))
l.place(x=10,y=120)

if tempC != temperaturaMinima or tempC != temperaturaMaxima:

    l = tk.Label(ventana,text=f"Temperatura Mínima: {temperaturaMinima} °C | {(round(float(temperaturaMinima)*(9/5) + 32,2))} °F",fg='#000',bg='#DDD',font=('Garamond bold', 15, 'bold italic'))
    l.place(x=10,y=150)
    l = tk.Label(ventana,text=f"Temperatura Máxima: {temperaturaMaxima} °C | {(round(float(temperaturaMaxima)*(9/5) + 32,2))} °F",fg='#000',bg='#DDD',font=('Garamond bold', 15, 'bold italic'))
    l.place(x=10,y=180)
    l = tk.Label(ventana,text=f"Humedad: {humedad}%",fg='#000',bg='#DDD',font=('Garamond bold', 15, 'bold italic'))
    l.place(x=10,y=210)
    l = tk.Label(ventana,text=f"Descripción: {descripcion}.",fg='#000',bg='#DDD',font=('Garamond bold', 15, 'bold italic'))
    l.place(x=10,y=240)

else:

    l = tk.Label(ventana,text=f"Humedad: {humedad}%",fg='#000',bg='#DDD',font=('Garamond bold', 15, 'bold italic'))
    l.place(x=10,y=150)
    l = tk.Label(ventana,text=f"Clima: {descripcion}.",fg='#000',bg='#DDD',font=('Garamond bold', 15, 'bold italic'))
    l.place(x=10,y=180)


img = typeWeather(descripcion.lower(),noche)
actualizarHora()

#Carga la imagen y ajusta su tamaño
imagen = Image.open('images/'+img)
ancho = 200  #Modifica el ancho deseado
alto = 200  #Modifica el alto deseado
imagenRedimensionada = imagen.resize((ancho, alto), Image.ANTIALIAS)
imagenTk = ImageTk.PhotoImage(imagenRedimensionada)

#Crea un widget Label para mostrar la imagen
labelImagen = tk.Label(ventana, image=imagenTk)
labelImagen.place(x=400,y=30)

#Ejecuta el bucle principal de la ventana
ventana.mainloop()
