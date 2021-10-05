class Configuration:

  def get_configuration(choose):

    if(choose == 'local'):
      connect_value = dict(host='localhost',
        user='USERNAME',
        password='PASSWORD',
        database='DBNAME',
        port=3306,
        charset='utf8')
      
    elif(choose == 'aws'):
      connect_value = dict(host='gyunseul9.xxxx.amazonaws.com',
        user='USERNAME',
        password='PASSWORD',
        database='DBNAME',
        port=3307,
        charset='utf8')

    else:
      print('Not Selected')
      connect_value = ''

    return connect_value
