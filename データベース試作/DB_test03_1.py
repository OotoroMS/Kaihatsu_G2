#DB使い方検証場所01
import matplotlib.pyplot as plt
import DbCommunication as DMC #DB関係

db=DMC.DbCommunication()

#db.db_query_execution('testdb_02',"insert into DB_sizelog(datetime,sizelog)values(now(),4.14)")
#db.db_query_execution('testdb_02',"insert into DB_sizelog(datetime,sizelog)values(now(),9.14)")
#db.db_query_execution('testdb_02',"insert into DB_sizelog(datetime,sizelog)values(now(),10.14)")
db.db_query_execution('testdb_02',"insert into DB_sizelog(datetime,sizelog)values(now(),13.14)")
db.db_query_execution('testdb_02',"insert into DB_sizelog(datetime,sizelog)values(now(),14.14)")

#新しい10個(降順)を取り出して、寸法データのみlistに入れる
size_list=[]
result = db.table_data_get('testdb_02',"select * from DB_sizelog order by id desc limit 10")
for i in result:
    size_list.append(i[2])

size_show=list(reversed(size_list))#並び順を反対にしている
print(size_show)

plt.plot(size_show)
plt.show()

print("------------------------------------------------")
db.table_data_list_display('testdb_02','DB_sizelog')
