import odoorpc


#def open_connection_odoogap(user, password, server, db, port):
#    # odoo_instance = odoorpc.ODOO(server, protocol='jsonrpc+ssl', port=int(port))
#    odoo_instance = odoorpc.ODOO(server, protocol='jsonrpc', port=int(port))
#   odoo_instance.login(db, user, password)     
#    return odoo_instance

# def get_token(user, password, server, db, port):
#    con = open_connection_odoogap(user, password, server, db, port)
#    if con:
#       return conn.execute('mtd.operations', 'get_token')

# def refresh_token(user, password, server, db, port, mtd_sandbox):
#    con = open_connection_odoogap(user, password, server, db, port)
#    if con:
#        return conn.execute('mtd.operations', 'refresh_token', mtd_sandbox)