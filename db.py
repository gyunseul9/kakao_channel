import pymysql

class DBConnection:
    def __init__(self,host,user,password,database,charset,port):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=database,
            charset=charset,
            port=port,
            cursorclass=pymysql.cursors.DictCursor)   

    def exec_select(self,kind):
        with self.connection.cursor() as cursor:
            query = Query().get_select(kind)
            cursor.execute(query)
            data = cursor.fetchall()

        return data               

    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()

class Query:
    
    def get_select(self,kind):
            
        if kind == 1:
            table = 'rnd'
            condition = ''
            sort = 'order by num desc limit 15'
        elif kind == 2:
            table = 'news'
            condition = ''
            sort = 'order by num desc limit 15'
        elif kind == 3:
            table = 'mk'
            condition = ''
            sort = 'order by num desc limit 15'
        elif kind == 4:
            table = 'bloter'
            condition = ''
            sort = 'order by num desc limit 15' 
        elif kind == 5:
            table = 'trend'
            condition = ''
            sort = 'order by num desc limit 15'   
        elif kind == 6:
            table = 'reader'
            condition = ''
            sort = 'order by num desc limit 15'
        elif kind == 7:
            table = 'aladin'
            condition = ''
            sort = 'order by now() desc limit 25'
        elif kind == 8:
            table = 'mt'
            condition = ''
            sort = 'order by num desc limit 15'
        elif kind == 9:
            table = 'coronastatus'
            condition = ''
            sort = 'order by num desc limit 15'  
        elif kind == 10:
            table = 'invest'
            condition = ''
            sort = 'order by num desc limit 5'  
        elif kind == 11:
            table = 'startup'
            condition = ''
            sort = 'order by num desc limit 5'  
        elif kind == 12:
            table = 'investor'
            condition = ''
            sort = 'order by num desc limit 5'
        elif kind == 13:
            table = 'fund'
            condition = ''
            sort = 'order by num desc limit 5'
        elif kind == 14:
            table = 'caveup'
            condition = ''
            sort = 'order by num desc limit 6'                                                                                              
        else:
            table = 'sendrnd'
            condition = ''
            sort = 'order by num desc limit 15'         

        if kind == 3:
            query = 'select posted, replace(headline, \'\r\', \'. \') as headline, src, link from {} {} {}'.format(table,condition,sort)
        else:
            query = 'select * from {} {} {}'.format(table,condition,sort)

        return query
              