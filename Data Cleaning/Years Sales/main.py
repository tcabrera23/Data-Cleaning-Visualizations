#!/usr/bin/env python
# coding: utf-8

# In[23]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ### Cargar archivos

# In[24]:


sales_2012 = pd.read_csv(r"C:\Users\tcabreraro001\Downloads\Curso Python\Preparation Data\sales_2012.csv")
sales_2013 = pd.read_csv(r"C:\Users\tcabreraro001\Downloads\Curso Python\Preparation Data\sales_2013.csv")
sales_2014 = pd.read_csv(r"C:\Users\tcabreraro001\Downloads\Curso Python\Preparation Data\sales_2014.csv")
sales_2015 = pd.read_csv(r"C:\Users\tcabreraro001\Downloads\Curso Python\Preparation Data\sales_2015.csv")
customer_address = pd.read_csv(r"C:\Users\tcabreraro001\Downloads\Curso Python\Preparation Data\customer_addresses.csv")


# In[25]:


# Uno todas las fechas - Union
sales_total = pd.concat([sales_2012,sales_2013,sales_2014,sales_2015])
# Hago un merge para hacer un join 
sales_customer_details = sales_total.merge(customer_address,on="Customer ID", how="left")


# ## Check datatype column

# In[26]:


sales_customer_details["Revenue"].describe() # dtype: object

sales_customer_details["Revenue"] = sales_customer_details["Revenue"].str.strip("$").astype("float64")
sales_customer_details["Price"] = sales_customer_details["Price"].str.strip("$").astype("float64")
sales_customer_details["Transaction Date"]=pd.to_datetime(sales_customer_details["Transaction Date"])

sales_customer_details


# In[27]:


# Busco outliers
sales_customer_details[sales_customer_details["Transaction Date"]>"2015-12-31"]


# In[28]:


# Busco outliers
sales_customer_details[sales_customer_details["Transaction Date"]<"2012-01-01"]


# In[29]:


# Cambio de 2051 a 2015 ya que el usuario se debe haber equivocado en el momento de escribirlo
sales_customer_details.loc[4158,"Transaction Date"]='2015-11-01 00:00:00'


# In[30]:


# Seleccionando columnas
sales_customer_details[["Transaction ID","Price", "Revenue"]]


# ## Chequeo valores nulos

# In[31]:


# Utilizo el metodo isna() o isnull()
sales_customer_details.isna().sum() 


# In[32]:


# Limpio los valores nulos de Product
nulls = sales_customer_details[sales_customer_details['Product'].isna()]
no_nulls = sales_customer_details[~sales_customer_details['Product'].isna()]

nulls[["Price", "Quantity"]].mean()


# In[33]:


#sales_customer_details.groupby(sales_customer_details["Product"]).mean()
no_nulls.groupby(sales_customer_details["Product"]).mean()


# In[34]:


# Observamos que el promedio en Quantity del producto Lomina es bastante similar, asi que puede haber relacion alli


# In[35]:


# Agrego los valores que no tenian nombre de producto a "Lomina" y chequeo que no hay mas nulls (osea que ya se cargaron)

sales_customer_details["Product"].fillna("Lomina", inplace=True)
sales_customer_details.isna().sum()


# # Encontrar duplicados

# In[36]:


# Primero hago la busqueda general y hago un drop() luego hago busqueda por ID y veo si el usuario quizas se equivoco nomas


# # Categorical Value Errors

# In[37]:


# Puede ser que los usuarios nos ingresen valores categoricos con distintos nombres o etiquetas
sales_customer_details["Product"].value_counts()


# In[38]:


# Nuestro deber es fusionar estos datos
replacements = {
    "Lominade":"Lomina",
    "Tridestand":"Tridesta",
    "Samatan":"Samtan",
    "Wediicare":"Wedicare"
}
sales_customer_details = sales_customer_details.replace(replacements)
sales_customer_details["Product"].value_counts()


# In[39]:


# Como no puedo dropear donde "Product" == "ufbbq" entonces armo una lista con los valores que quiero ver y se la paso al DF
products=["Lomina","Samtan","Tridesta","Wedicare"]
sales_customer_details=sales_customer_details[sales_customer_details["Product"].isin(products)]
sales_customer_details["Product"].value_counts()


# In[40]:


plt.figure(figsize=(8, 8))
plt.scatter(sales_customer_details["Transaction Date"],sales_customer_details["Price"])

