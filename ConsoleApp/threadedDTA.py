import sys
import requests
import json
import concurrent
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

headerInfo = {"Content-Type":"application/json", "X-Requested-With":"XMLHttpRequest"}
userDict = {}
userHeaders = {}

s = requests.Session()

def fileProcessor():

    with open(sys.argv[1]) as f: #Reading in the file
        lines = f.readlines() 

    lines_formatted = [] 

    for i in range(len(lines)): #String formatting and appending to larger list
        without_line_breaks = lines[i].replace("\n","")
        separate_by_comma = without_line_breaks.split(",")
        lines_formatted.append(separate_by_comma)
        lines_formatted[i][0] = lines_formatted[i][0].split(" ")

    for j in range(len(lines_formatted)):
        if lines_formatted[j][0][1] == "ADD":
            userDict[lines_formatted[j][1]] = []


    for key in userDict:
        for element in lines_formatted:
            
            # print(str(element[0]) + " " + str(element[1]) + " " + str(key))

            if (element[1]==key):

                userDict[key] += [element]

            # for item in element:
                
            #     if str(item) == key:
                    
            #         userDict[key] += [element]
                    
            #         break

    for key in userDict:
        print(str(userDict[key]) + "\n\n")

    return userDict

def requestManager(batch,username):

    print("ENTERING LOG IN PHASE FOR " + username)

    endpoint = "https://daytradingseng468.herokuapp.com/api/users/"
    payload = {"user": {"email":username + "@gmail.com", "username":username, "password":username}}

    r = s.post(url = endpoint, data = json.dumps(payload), headers = headerInfo)
    res = r.json()
    # print(r.text)

    if ("errors" in res):

        print("REGISTRATION FAIL TRYIN TO LOG IN")
        endpoint = "https://daytradingseng468.herokuapp.com/api/users/login/"
        payload = {"user": {"email":username + "@gmail.com", "password":username}}

        r = s.post(url = endpoint, data = json.dumps(payload), headers = headerInfo)
        # print(r.text)
        res = r.json()
        

        if ("errors" in res):
            print("ERROR UNABLE TO LOGIN OR REGISTER")
            #exit() 
        
        # print("LOG IN SUCCESSFUL FOR " + username)

    token = "hello"
    tempHeader = headerInfo
    tempHeader["Authorization"] = "Token " + token
    userHeaders[username] = tempHeader

    print("AUTHENTICATION SUCCESSFUL FOR " + username)
    count = 0
    for element in batch:
        # print(count)
        # print(element[0][1])
        if element[0][1] == "ADD":
            username = element[1]
            amount = element[2].strip(" ")
            endpoint = "https://daytradingseng468.herokuapp.com/api/add/"
            payload = {"user": {"username" : username, "amount" : amount}}
            
            r = s.post(url=endpoint, data=json.dumps(payload), headers=userHeaders[username])
            # print("ADD ->  Status Code = " + str(r.status_code) + "\n" + r.text)
            # if(r.status_code == 500):

            #     f = open("errors.txt","w",encoding="utf-8")
            #     f.write(r.text)

            print("ADD ->  " + r.text)

        if element[0][1] == "QUOTE":
            username = element[1]
            ticker = element[2].strip(" ")
            endpoint = "https://daytradingseng468.herokuapp.com/api/quote"
            parameters = {"username":username,"ticker": ticker}   

            r = s.get(url=endpoint, params=parameters, headers=userHeaders[username])
            print("QUOTE ->  " + r.text)
        if element[0][1] == "BUY":
            username = element[1]
            ticker = element[2]
            amount = element[3].strip(" ")

            endpoint = "https://daytradingseng468.herokuapp.com/api/buy"
            payload = {"user": {"username" : username, "ticker" : ticker, "amount" : amount}}
            r = s.post(url=endpoint, data=json.dumps(payload), headers=userHeaders[username])
            print("BUY ->  Status Code = " + str(r.status_code) + "\n" + r.text)
        if element[0][1] == "COMMIT_BUY":
            username = element[1].strip()
            endpoint = "https://daytradingseng468.herokuapp.com/api/commitbuy/"
            payload = {"user": {"username" : username}}
            r = s.post(url=endpoint, data=json.dumps(payload), headers=userHeaders[username])
            print("COMMIT_BUY ->  Status Code = " + str(r.status_code) + "\n" + r.text)     
        if element[0][1] == "CANCEL_BUY":
            username = element[1].strip()
            endpoint = "https://daytradingseng468.herokuapp.com/api/cancelbuy/"
            payload = {"user": {"username" : username}}
            r = s.post(url=endpoint, data=json.dumps(payload), headers=userHeaders[username])
            print("CANCEL_BUY ->  " + r.text)
        if element[0][1] == "SELL":
            username = element[1]
            ticker = element[2]
            amount = element[3].strip()
            endpoint = "https://daytradingseng468.herokuapp.com/api/sell/"
            payload = {"user": {"username" : username, "ticker" : ticker, "amount" : amount}}
            r = s.post(url=endpoint, data=json.dumps(payload), headers=userHeaders[username])

        if element[0][1] == "COMMIT_SELL":
            username = element[1].strip()
            endpoint = "https://daytradingseng468.herokuapp.com/api/commitsell/"
            payload = {"user": {"username" : username}} 
            r = s.post(url=endpoint, data=json.dumps(payload), headers=userHeaders[username])           

        if element[0][1] == "CANCEL_SELL":
            username = element[1].strip()
            endpoint = "https://daytradingseng468.herokuapp.com/api/cancelsell/"
            payload = {"user": {"username" : username}}
            r = s.post(url=endpoint, data=json.dumps(payload), headers=userHeaders[username])           

        if element[0][1] == "SET_BUY_AMOUNT":
            username = element[1]
            ticker = element[2]
            amount = element[3].strip()
            endpoint = "https://daytradingseng468.herokuapp.com/api/setbuyamount/"
            payload = {"user": {"username" : username, "ticker" : ticker, "amount" : amount}}
            r = s.post(url=endpoint, data=json.dumps(payload), headers=userHeaders[username])           

        if element[0][1] == "CANCEL_SET_BUY":
            username = element[1]
            ticker = element[2].strip()
            endpoint = "https://daytradingseng468.herokuapp.com/api/cancelsetbuy/"
            payload = {"user": {"username" : username, "ticker" : ticker}}
            r = s.post(url=endpoint, data=json.dumps(payload), headers=userHeaders[username])           

        if element[0][1] == "SET_BUY_TRIGGER":
            username = element[1]
            ticker = element[2]
            amount = element[3].strip()
            endpoint = "https://daytradingseng468.herokuapp.com/api/setbuytrigger/"
            payload = {"user": {"username" : username, "ticker" : ticker, "amount" : amount}}
            r = s.post(url=endpoint, data=json.dumps(payload), headers=userHeaders[username])           

        if element[0][1] == "SET_SELL_AMOUNT":
            username = element[1]
            ticker = element[2]
            amount = element[3].strip()
            endpoint = "https://daytradingseng468.herokuapp.com/api/setsellamount/"
            payload = {"user": {"username" : username, "ticker" : ticker, "amount" : amount}}
            r = s.post(url=endpoint, data=json.dumps(payload), headers=userHeaders[username])           

        if element[0][1] == "SET_SELL_TRIGGER":
            username = element[1]
            ticker = element[2]
            amount = element[3].strip()
            endpoint = "https://daytradingseng468.herokuapp.com/api/setselltrigger/"
            payload = {"user": {"username" : username, "ticker" : ticker, "amount" : amount}}
            r = s.post(url=endpoint, data=json.dumps(payload), headers=userHeaders[username])           
        
        if element[0][1] == "CANCEL_SET_SELL":
            username = element[1]
            ticker = element[2].strip()
            endpoint = "https://daytradingseng468.herokuapp.com/api/cancelsetsell/"
            payload = {"user": {"username" : username, "ticker" : ticker}}
            r = s.post(url=endpoint, data=json.dumps(payload), headers=userHeaders[username]) 

        if element[0][1] == "DISPLAY_SUMMARY":
            username = element[1].strip()
            endpoint = "https://daytradingseng468.herokuapp.com/api/displaysummary"
            parameters = {"username":username}        
            r = s.get(url = endpoint, params=parameters)
            print("DISPLAY SUMMARY")
        count += 1

def main():

    iterationDict = fileProcessor()

    # print(iterationDict)
    # threads = [Thread(target=requestManager, args=(iterationDict[key],key)) for key in iterationDict]

    # # for key in iterationDict:
    # #     print(str(iterationDict[key]) + "\n\n")
    

    # for thread in threads:
    #     thread.start()

    # for t in threads:
    #     t.join()

    endpoint = "https://daytradingseng468.herokuapp.com/api/dumplog"  
    print("DUMPLOG")

    

if __name__ == '__main__':
    main()
