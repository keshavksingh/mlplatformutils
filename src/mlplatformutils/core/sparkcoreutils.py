import json

def read_from_adls_gen2(SOURCE_STORAGE_ACCOUNT_VALUE,\
                        AZURE_TENANT_ID,\
                        file_path,\
                        file_format,\
                        SOURCE_READ_SPN_VALUE,\
                        SOURCE_READ_SPNKEY_VALUE):
    from pyspark.sql.session import SparkSession
    spark = SparkSession.builder.appName("Read from ADLS Gen2").getOrCreate()
    spark.conf.set("fs.azure.account.auth.type."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", "OAuth")
    spark.conf.set("fs.azure.account.oauth.provider.type."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net",  "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
    spark.conf.set("fs.azure.account.oauth2.client.id."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", SOURCE_READ_SPN_VALUE)
    spark.conf.set("fs.azure.account.oauth2.client.secret."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", SOURCE_READ_SPNKEY_VALUE)
    spark.conf.set("fs.azure.account.oauth2.client.endpoint."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", "https://login.microsoftonline.com/"+AZURE_TENANT_ID+"/oauth2/token")

    df = spark.read.format(file_format).load(file_path)
    
    return df

def write_to_adls_gen2(SOURCE_STORAGE_ACCOUNT_VALUE,\
                       AZURE_TENANT_ID,\
                       file_path,\
                       file_format,\
                       repartition,\
                       partitionColumn,\
                       dynamicPartitionOverwriteMode,\
                       df,\
                       SOURCE_WRITE_SPN_VALUE,\
                       SOURCE_WRITE_SPNKEY_VALUE):
    from pyspark.sql.session import SparkSession             
    spark = SparkSession.builder.appName("Read from ADLS Gen2").getOrCreate()
    spark.conf.set("fs.azure.account.auth.type."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", "OAuth")
    spark.conf.set("fs.azure.account.oauth.provider.type."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net",  "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
    spark.conf.set("fs.azure.account.oauth2.client.id."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", SOURCE_WRITE_SPN_VALUE)
    spark.conf.set("fs.azure.account.oauth2.client.secret."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", SOURCE_WRITE_SPNKEY_VALUE)
    spark.conf.set("fs.azure.account.oauth2.client.endpoint."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", "https://login.microsoftonline.com/"+AZURE_TENANT_ID+"/oauth2/token")
    
    if dynamicPartitionOverwriteMode:
        spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
    
    if repartition is None:
        if partitionColumn:
            #partitionColumn accepted as list of columns
            df.write.format(file_format).partitionBy(partitionColumn).mode("overwrite").save(file_path)
        else: 
            df.write.format(file_format).mode('overwrite').save(file_path)
    else:
        if partitionColumn:
            df.repartition(repartition).write.format(file_format).partitionBy(partitionColumn).mode("overwrite").save(file_path)
        else:
            df.repartition(repartition).write.format(file_format).mode('overwrite').save(file_path)
    return

def read_from_kusto(kustoOptions):
    from pyspark.sql.session import SparkSession
    pyKusto = SparkSession.builder.appName("kustoPySpark").getOrCreate()
    kustoDf  = pyKusto.read. \
                format("com.microsoft.kusto.spark.datasource"). \
                option("kustoCluster", kustoOptions["kustoCluster"]). \
                option("kustoDatabase", kustoOptions["kustoDatabase"]). \
                option("kustoQuery", kustoOptions["kustoTable"]). \
                option("kustoAadAppId", kustoOptions["kustoAADClientID"]). \
                option("kustoAadAppSecret", kustoOptions["kustoClientAADClientPassword"]). \
                option("kustoAadAuthorityID", kustoOptions["kustoAADAuthorityID"]). \
                load()
                  
    return kustoDf

def read_from_azsql(SQL_SERVER_INSTANCE,access_token,Query):
    from pyspark.sql.session import SparkSession
    pySql = SparkSession.builder.appName("AzSQLPySpark").getOrCreate()
    df = pySql.read \
        .format("com.microsoft.sqlserver.jdbc.spark") \
        .option("url", SQL_SERVER_INSTANCE) \
        .option("query", Query) \
        .option("accessToken", access_token) \
        .option("encrypt", "true") \
        .option("hostNameInCertificate", "*.database.windows.net") \
        .load()
    
    return df