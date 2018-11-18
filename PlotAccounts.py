# Import the Python extension module to enable access to Oracle Database
import cx_Oracle
# Import Pandas and other modules as required
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

#Connect to the underlying database to get the details
dsn_tns = cx_Oracle.makedsn(<<DB SERVER>>, <<PORT>>, <<SID>>)
conn = cx_Oracle.connect(user=<<USERNAME>>, password=<<PASSWORD>>, dsn=dsn_tns)

# Get the required accounts data from Oracle. The second argument defines what will be the size of the bubble
accounts = pd.read_sql_query("select STATE_NAME as STATE, count(*)/100 as COUNT  from ACCOUNTS where COUNTRY_CODE='US' and STATE_NAME is not null group by STATE_NAME", conn)

# Read the statewise coordinates from the CSV file
statecoordinates=pd.read_csv("state-coordinates.csv")

#Create the dataframes
df1=pd.DataFrame(accounts)
df2=pd.DataFrame(statecoordinates)

#  Do a join between the datasets and specify the join column
df3=pd.merge(df1,df2,left_on="STATE", right_on="State")


# Plot the graph
plt.figure(figsize=(18,10))
m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
        projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
m.drawcoastlines(color='#555566', linewidth=2)
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='white',lake_color='aqua')
m.drawcountries(zorder=2,color="black", linewidth=2)
m.drawstates(zorder=2,color="red", linewidth=1)


# Initialize the values
x=[]
y=[]
z=[]
for name, row in df3.iterrows():
    x.append(row["Longitude"])
    y.append(row["Latitude"])
    z.append(row["CNT"])
    

lons,lats = m(x,y)

# Plot the graph
m.scatter(lons,lats,z, c='blue',alpha=0.5, zorder=10)



