import dns.name
import dns.message
import dns.query
import time
import datetime
def getNameServer(additionals):
    for i in additionals:
        additional = str(i).split(" ")
        if additional[-2] == "A":
            return additional[-1]

def dnsIPLookup(domain):
    dnsName = dns.name.from_text(domain)
    query = dns.message.make_query(dnsName, dns.rdatatype.A)
    rootServer = '198.41.0.4'
    while True:
        response = dns.query.udp(query, rootServer)
        if response.rcode() == 3:
            return 'Invalid Domain'
        elif not len(response.answer) == 0:
            return response.answer, response.question
        elif not len(response.additional) == 0:
            rootServer = getNameServer(response.additional)
            continue
        else:
            return dnsIPLookup(str(response.authority[0]).split("\n")[0].split(" ")[-1][:-1])

def mydig(domainname):
    starttime = time.time()
    results = dnsIPLookup(domainname)
    endtime = time.time()
    question = str(results[1][0])
    answer = str(results[0][0]).split("\n")
    print("QUESTION SECTION:")
    print(question)
    print()
    print("ANSWER SECTION:")
    for i in answer:
        print(i)
        temp = i
        while temp.split(" ")[-2] == "CNAME":
            newname = temp.split(" ")[-1]
            r = dnsIPLookup(newname)[0][0]
            temp = str(r)
            print(temp)
    print()
    print("Query time:", round((endtime - starttime) * 1000, 3), "ms")
    date = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    print("WHEN:", date)