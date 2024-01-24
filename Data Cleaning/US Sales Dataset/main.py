#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd


# # Abriendo el archivo excel que puede contener varias hojas

# In[10]:


sales_xls=pd.ExcelFile(r"Sales Data.xlsx")
sales_xls.sheet_names


# ### Convirtiendo a dataframe

# In[11]:


sales_dataset=sales_xls.parse('Sales Data') # Nombre de la sheet del excel
sales_dataset


# In[12]:


# Datatype de la tabla Sales
sales_dataset.info()


# ### Check Nulls

# In[13]:


# No tengo valores nulos
sales_dataset.isna().sum()


# ### Check Duplicates

# In[14]:


# No tengo valores duplicados
sales_dataset[sales_dataset.duplicated()].sum()


# ### Check Categorical Value Errors

# In[15]:


sales_dataset["Region"].value_counts()


# ### Modificando el datatype de las columnas

# In[16]:


sales_dataset["Revenue"] = sales_dataset["Revenue"].str.strip('$').astype("float64")
sales_dataset["Cost"] = sales_dataset["Cost"].str.strip('$').astype("float64")
#sales_dataset["Date"] = pd.to_datetime(sales_dataset["Date"]) en caso de querer realizar operaciones entre fechas

sales_dataset.info()


# In[17]:


# Agrego columna profit 
sales_dataset["Profit"] = sales_dataset["Revenue"] - sales_dataset["Cost"]
sales_dataset


# In[18]:


# Split Address
sales_dataset[["Street","Address_Edit"]] = sales_dataset["Address"].str.split(',', expand=True)
sales_dataset


# In[19]:


# Hago el split de derecha a izquierda para tratar mejor los espacios en blanco
sales_dataset[["City&State","Code"]] = sales_dataset["Address_Edit"].str.rsplit(' ', n=1, expand=True)
sales_dataset[["City","State"]] = sales_dataset["City&State"].str.rsplit(' ', n=1, expand=True)
sales_dataset


# In[20]:


# Borro las columnas que no necesito y edito el orden de las mismas
sales_dataset = sales_dataset.drop(columns=["Address", "Address_Edit", "City&State"])
new_order = ["Customer Name", "Users", "Revenue", "Cost", "Profit", "State", "City", "Street", "Code", "Date", "Region", "Sales person"]

sales_dataset = sales_dataset[new_order]
sales_dataset


# In[21]:


sales_dataset["Profit"].describe()


# In[22]:


# Distinct Count de mis columnas
sales_dataset.nunique()


# In[23]:


print(sales_dataset.groupby(sales_dataset["Region"]).sum())


# In[24]:


# Estados que tuvieron mayor profit
states_byProfit = sales_dataset[["State","Profit"]].groupby('State').sum()
top_states = states_byProfit.sort_values("Profit", ascending=False)
top_states.head()


# In[25]:


# Vendedores con mejor profit
sales_person_byProfit = sales_dataset[["Sales person","Profit"]].groupby('Sales person').sum()
top_sales_person = sales_person_byProfit.sort_values("Profit", ascending=False)
top_sales_person


# In[26]:


# Vendedores con mas cantidad de usuarios
sales_person_byUsers = sales_dataset[["Sales person","Users"]].groupby('Sales person').sum()
top_sales_person = sales_person_byUsers.sort_values("Users", ascending=False)
top_sales_person


# In[27]:


sales_dataset["Users"].describe()


# ### Guardando el dataframe en un archivo Excel

# In[28]:


sales_dataset.to_excel("Sales Dataset.xlsx", sheet_name="Sales", index=False)

