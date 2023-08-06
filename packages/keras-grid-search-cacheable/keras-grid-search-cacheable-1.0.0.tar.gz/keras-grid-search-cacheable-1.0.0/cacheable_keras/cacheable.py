# -*- coding: utf-8 -*-
"""
@author: Daniel Espinosa- Daespinosag

"""
import tensorflow as tf
import tempfile

class KerasCacheable():
    def get_params_cacheable(self):
        '''Esta funcion se usa para extraer los parametros cachables y configurar el guardado y la extracción.
            -> este metodo debe sobreescribirse si no se quieren tomar todas las propiedades como cachables
            -> Si sobre escribe este metodo asegurese de escribir correctamente los nombres de sus propiedades si ingresa algun nombre errado el proceso de ejecusión fallará
                return:
                    properties: Se retorna una lista con los nombres de las propiedades que son cacheables'''    
        
        return self.get_params().keys()

    def get_custom_objects():
        '''
        Esta funcion se usa para extraer las acciones custom que debe ejecutar el modelo.
            -> este metodo debe sobreescribirse se se quiere incluir una funcion custom para ejecutar el modelo (por ejemplo: una funcion de costo)
                return:
                    properties: Un diccionario con: {'nombre_de_la_funcion' : referencia a la funcion }
        '''
        return {}

    def __getstate__(self):
        '''
        Este metodo mágico se utiliza para extraer la información cacheada 
            return:
                es un diccionario {'propiedad' : valor_de_la_propiedad }    
        '''
        model_str = ""
        
        with tempfile.NamedTemporaryFile(suffix='.h5', delete=True) as fd:
            try:
                self.model.save(fd.name,save_format='h5')
                model_str = fd.read()
            except:
                model_str  = 'model no trained'
                self.A_out = 'model no trained'
                self.A_in  = 'model no trained'

        d = { 'model_str': model_str,'A_in': self.A_in,'A_out': self.A_out }

        for att in self.get_params_cacheable():
            d[att] = getattr(self,att)            
        
        return d

    def __setstate__(self, state):
        '''
        Este metodo mágico se utiliza para actualizar la información cacheada 
        '''
        for att in self.get_params_cacheable():
            setattr(self,att,state[att])

        with tempfile.NamedTemporaryFile(suffix='.h5', delete=True) as fd:
            try:
                fd.write(state['model_str'])
                fd.flush()
                self.model=tf.keras.models.load_model(fd.name,custom_objects=self.get_custom_objects())    
                self.A_in=state['A_in']
                self.A_out=state['A_out']
            except:
                self.mode=state['model_str']
         
                

