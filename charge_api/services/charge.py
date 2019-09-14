from sqlalchemy import create_engine
list = []

def charge (card_number,transaction,merchant):
    db_connect = create_engine('sqlite:///charge.db')
    conn = db_connect.connect()
    global list 
    list.append(merchant)
    if list.count(merchant) > 10:
        return {"approved": "false", "deniedReasons": "Merchant is on blacklist"}
    else:           
        query = conn.execute("select card_status from charge where card_number = {0};" .format(card_number)).fetchall()
        system = query[0][0]
        if system == "false":
            return {"approved": "false", "deniedReasons": "Credit Card is blocked"}
        else:
            query = conn.execute("select card_limit from charge where card_number = {0};" .format(card_number)).fetchall()
            system = query[0][0]
            new_limit = system - transaction
            if new_limit < 0:
                return {"approved": "false", "deniedReasons": "Insufficient limit"}
            else:
                query2 = conn.execute("select last_transaction from charge where card_number = {0};" .format(card_number)).fetchall()
                system2 = query2[0][0]
                if system2 == "null":
                    limit = system * 0.9
                    if transaction > limit:
                        return {"approved": "false", "deniedReasons": "First transaction exceeded"} 
                    else:    
                        query3 = conn.execute("update charge set card_limit = {0} where card_number = {1}".format(new_limit,card_number))
                        return {"approved": "true", "new_limit": new_limit, "deniedReasons": "null"}
