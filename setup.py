import loginUnit.webUtility
import ticket.Ticket
import time
import copy

loginUnit = loginUnit.webUtility.webUtility()
myTicket = ticket.Ticket.Ticket(loginUnit)

response = loginUnit.decodeQR_img(loginUnit.getQRimg())

stateCode = loginUnit.QRquery(response)

loginUnit.check_login()

while(stateCode != '2'):
     stateCode = loginUnit.QRquery(response)
     print(stateCode)
     time.sleep(1)

stateCode = loginUnit.QRquery(response)

loginUnit.check_uamtk()
user = loginUnit.check_uamauthclient()

print("Hello! " + user + "，欢迎使用本系统\n\t by Gadia")

myTicket.getTrainList(loginUnit)



# 选择车次
for each in myTicket.trainInfo:
    TrainList = each.split('|')
    if (TrainList[11] == 'Y'):
        if TrainList[3] == 'G843':
            print("G843的str为" + TrainList[0])
            temp = copy.deepcopy(TrainList[0])
            myTicket.secretStr = temp
            #myTicket.secretStr(temp)

        print('车次为:' + TrainList[3] +
              '\t起始：:' + TrainList[6] +
              '\t到：' + TrainList[7] +
              '\t日期：' + TrainList[13] +
              '\t二等座数量：' + TrainList[30] +
              '\t一等座数量：' + TrainList[31])
    else:
        continue


print(loginUnit.checkUser())
print(myTicket.secretStr)