
## Conexion a la base de datos

server = 'OE-5CD2266N-PLA'
database = 'tpcxbb_1gb'
username = 'sa'
password = 'P@ssword1'

# CONEXION CON LA BASE DE DATOS
connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};TrustServerCertificate=yes;UID={username};PWD={password}'
conn_str = pyodbc.connect(connectionString)

# QUERY DE LA CONSULTA
input_query = '''SELECT
ss_customer_sk AS Cliente,
ROUND(COALESCE(returns_count / NULLIF(1.0*orders_count, 0), 0), 7) AS ordenRatio,
ROUND(COALESCE(returns_items / NULLIF(1.0*orders_items, 0), 0), 7) AS itemsRatio,
ROUND(COALESCE(returns_money / NULLIF(1.0*orders_money, 0), 0), 7) AS totalRatio,
COALESCE(returns_count, 0) AS Frequencia
FROM
(
  SELECT
    ss_customer_sk,
    -- return order ratio
    COUNT(distinct(ss_ticket_number)) AS orders_count,
    -- return ss_item_sk ratio
    COUNT(ss_item_sk) AS orders_items,
    -- return monetary amount ratio
    SUM( ss_net_paid ) AS orders_money
  FROM store_sales s
  GROUP BY ss_customer_sk
) orders
LEFT OUTER JOIN
(
  SELECT
    sr_customer_sk,
    -- return order ratio
    count(distinct(sr_ticket_number)) as returns_count,
    -- return ss_item_sk ratio
    COUNT(sr_item_sk) as returns_items,
    -- return monetary amount ratio
    SUM( sr_return_amt ) AS returns_money
FROM store_returns
GROUP BY sr_customer_sk ) returned ON ss_customer_sk=sr_customer_sk'''

##################
customer_data = pd.read_sql(input_query, conn_str)
#############
# DATOS DE LA TABLA
#print("Data frame:", customer_data.head(n=5))
##########################
## numero de clusters usando el Elbow method

cdata = customer_data
# RANGO DE GRUPOS
K = range(1, 20)
KM = (sk_cluster.KMeans(n_clusters=k).fit(cdata) for k in K)

centroids = (k.cluster_centers_ for k in KM)
D_k = (sci_distance.cdist(cdata, cent, 'euclidean') for cent in centroids)
dist = (np.min(D, axis=1) for D in D_k)
avgWithinSS = [sum(d) / cdata.shape[0] for d in dist]

# GRAFICA EL METODO ELBOW
plt.plot(K, avgWithinSS, 'b*-')
plt.grid(True)
plt.xlabel('Numero de clusters')
plt.ylabel('Promedio entre-cluster suma de cuadrados')
plt.title('Elbow para KMeans clustering')

#plt.show()

## clustering usando Kmeans
n_clusters = 4

# Procesamiento de los clusters
means_cluster = sk_cluster.KMeans(n_clusters=n_clusters, random_state=111)

columns = ["ordenRatio", "itemsRatio", "totalRatio", "Frequencia"]

est = means_cluster.fit(customer_data[columns])
clusters = est.labels_

# Se agregan los valores de los Kmeans a la 
# data que ya teniamos 
customer_data['cluster'] = clusters



# Informacion de los Clusters
for c in range(n_clusters):
    # Informacion de cada Cluster
    cluster_members=customer_data[customer_data['cluster'] == c][:]
    print('Cluster{}(n={}):'.format(c, len(cluster_members)))
    print('-'* 17)

# Datos agrupados por cluster
print(customer_data.groupby(['cluster']).mean())


#centroides = means_cluster.cluster_centers_
#print(centroides)


# Las datos de las columnas
customer_data.columns

#print(customer_data)







