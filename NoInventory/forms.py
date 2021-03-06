from django import forms
from django.contrib.auth.models import User
from NoInventory.models import *

from clasificacion import *

from bson import Binary, Code
from bson.json_util import dumps
from bson.json_util import loads
import json
import os
from NoInventory.views import *


from django.template import RequestContext
from django.forms import ClearableFileInput
from pymongo import MongoClient




manejadorClasificacion=ClasificacionDriver()


class ItemForm3(forms.Form):
    """Form for adding and editing backups."""

    def __init__(self, *args, **kwargs):
        organizacion = kwargs.pop('organizacion')
        super(ItemForm3, self).__init__(*args, **kwargs)
        self.fields['nombre_item'] = forms.CharField(required=True,max_length=150, label="Nombre")
        self.fields['descripcion_item']  = forms.CharField(widget = forms.Textarea, label="Detalles")
        lista_tag1=manejadorClasificacion.database.tag1.find({"organizacion":organizacion}).sort([("CLAVE1", 1)])
        lista_tag2=manejadorClasificacion.database.tag2.find({"organizacion":organizacion}).sort([("CLAVE2", 1)])
        lista_tag3=manejadorClasificacion.database.tag3.find({"organizacion":organizacion}).sort([("CLAVE3", 1)])
        #print "formulario"
        #print lista_tag2[0]["VALOR2"]
        self.fields['tag1'] = forms.ChoiceField(label='', choices=[(x["VALOR1"], x["VALOR1"]) for x in lista_tag1])
        self.fields['tag2'] = forms.ChoiceField(label='', choices=[(x["VALOR2"], x["VALOR2"]) for x in lista_tag2])
        self.fields['tag3'] = forms.ChoiceField(label='', choices=[(x["VALOR3"], x["VALOR3"]) for x in lista_tag3])
        self.fields['peso'] = forms.FloatField(required=False, label='Peso/Unidad',initial=0.0)
        self.fields['unidades']=forms.IntegerField(required=False,label='Unidades',initial=1)



class ItemFormAndroid(forms.Form):
    """Form for adding and editing items."""

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario')
        organizacion = kwargs.pop('organizacion')
        super(ItemFormAndroid, self).__init__(*args, **kwargs)
        self.fields['nombre_item'] = forms.CharField(required=True,max_length=150,label="Nombre")
        self.fields['descripcion_item']  = forms.CharField(widget = forms.Textarea, label="Detalles")
        lista_tag1=manejadorClasificacion.database.tag1.find({"organizacion":organizacion}).sort([("CLAVE1", 1)])
        lista_tag2=manejadorClasificacion.database.tag2.find({"organizacion":organizacion}).sort([("CLAVE2", 1)])
        lista_tag3=manejadorClasificacion.database.tag3.find({"organizacion":organizacion}).sort([("CLAVE3", 1)])
        #print "formulario"
        #print lista_tag2[0]["VALOR2"]
        self.fields['tag1'] = forms.ChoiceField(label='', choices=[(x["VALOR1"], x["VALOR1"]) for x in lista_tag1])
        self.fields['tag2'] = forms.ChoiceField(label='', choices=[(x["VALOR2"], x["VALOR2"]) for x in lista_tag2])
        self.fields['tag3'] = forms.ChoiceField(label='', choices=[(x["VALOR3"], x["VALOR3"]) for x in lista_tag3])
        self.fields['peso'] = forms.FloatField(required=False, label='Peso/Unidad',initial=0.0)
        self.fields['unidades']=forms.IntegerField(required=False,label='Unidades',initial=1)
        self.fields['user'] =forms.CharField(required=True,initial=usuario)
        self.fields['org'] = forms.CharField(required=True,initial=organizacion)

class CatalogoFormAndroid(forms.Form):
    """Form for adding and editing backups."""

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario')
        organizacion = kwargs.pop('organizacion')
        super(CatalogoFormAndroid, self).__init__(*args, **kwargs)
        TIPO = (('Publico', 'Publico'),('Privado', 'Privado'),)
        self.fields['nombre_catalogo'] = forms.CharField(required=True,max_length=150, label="Nombre")
        self.fields['descripcion_catalogo']  = forms.CharField(widget = forms.Textarea, label="Detalles")
        self.fields['fecha_alerta_catalogo'] = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}),initial="",required=False, label="Fecha Alerta")
        self.fields['tag_catalogo'] = forms.CharField(widget = forms.Textarea, max_length=300,label="Alerta")
        self.fields['tipo_catalogo'] = forms.CharField(label="Tipo",max_length=150,widget=forms.Select(choices=TIPO))
        self.fields['user'] =forms.CharField(required=True,initial=usuario)
        self.fields['org'] = forms.CharField(required=True,initial=organizacion)



class CatalogoForm(forms.ModelForm):
    TIPO = (('Publico', 'Publico'),('Privado', 'Privado'),)
    nombre_catalogo = forms.CharField(max_length=150, label="Nombre")
    descripcion_catalogo  = forms.CharField(widget = forms.Textarea, max_length=600,label="Detalles")
    fecha_alerta_catalogo = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}),initial="",required=False, label="Fecha Alerta")
    tag_catalogo = forms.CharField(widget = forms.Textarea, max_length=300,help_text="Alerta a mostar",label="Alerta")
    tipo_catalogo = forms.CharField(max_length=150,widget=forms.Select(choices=TIPO),label="Tipo")

    class Meta:
        model = Catalogo
        fields = ('nombre_catalogo','descripcion_catalogo','tag_catalogo','tipo_catalogo')

class SelectItem(forms.Form):
    def __init__(self,*args,**kwargs):
        super(SelectItem, self).__init__(*args,**kwargs)
        lista_items=db.items.find()
        self.fields['items'] = forms.ChoiceField(label="items", choices=[(x["nombre_item"], x["nombre_item"]) for x in lista_items])

class DocumentForm(forms.Form):
    archivo = forms.FileField(label='Selecciona fichero csv',help_text='max. 42 megabytes')

class CustomClearableFileInput(ClearableFileInput):
    template_with_clear = '<br>  <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label> %(clear)s'

class FormEntrada(forms.Form):
    file_tag1 = forms.FileField(label='Selecciona un archivo para tag 1',required=False)
    file_tag2 = forms.FileField(label='Selecciona un archivo para tag 2',required=False)
    file_tag3 = forms.FileField(label='Selecciona un archivo para tag 3',required=False)

    #file_tag2 = forms.FileField(label='Selecciona un archivo para tag 2')
    #file_tag3 = forms.FileField(label='Selecciona un archivo para tag 3')

class BuzonForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BuzonForm, self).__init__(*args, **kwargs)
        perfiles=UserProfile.objects.filter()
        organizaciones=[]
        organizaciones.append("Administrador")
        for i in perfiles:
            if i.organizacion not in organizaciones:
                organizaciones.append(i.organizacion)

        self.fields["asunto"] = forms.CharField(label="Asunto",required=True,max_length=150)
        self.fields["origen"] = forms.EmailField(label="Tu correo")#forms.CharField(label="Tu correo",required=True,max_length=150)
        self.fields["destino"] = forms.ChoiceField(label="Destinatario", choices=[(x,x) for x in organizaciones])
        self.fields["correo"]  = forms.CharField(label="Correo",widget = forms.Textarea)




############### REGISTRO DE USUARIOS #################
class UserForm(forms.ModelForm):
    username = forms.CharField(label="Usuario",required=True,max_length=150)
    password = forms.CharField(widget=forms.PasswordInput(),label="Password")
    email = forms.EmailField(label="Correo")
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    organizacion = forms.CharField(label="",required=True,max_length=150)
    class Meta:
        model = UserProfile
        fields = ('organizacion',)
