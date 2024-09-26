import DbCommunication as DMC #DB関係
db=DMC.DbCommunication()

result = db.table_data_get('testdb_02',"select * from DB_now")
for i in result:
    print(i)

print("%s" % (result[0][1]))#二次元　注意!
print(i[1])#配列にしたらOK