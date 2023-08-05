import re
import numpy as np

class Subnet:
    bitVs = np.array([128,64,32,16,8,4,2,1])
    subnet_info = {}
    def __init__(self,address,data,static=False):
        self.address = address
        self.static = static
        self.data = data
        self.subnetIt()

    def subnetIt(self):
        ip = list(map(int,re.findall(r"(\d+)",self.address)))
        maskBits = ip[-1]
        for nid,nno in self.data.items():
            tdata = {}
            if self.static:
                netbits = self.bitsRequired(len(self.data))
            else:
                hostbits = self.bitsRequired(nno+2)
                netbits =(32-hostbits)-maskBits
            tdata["mask"] = self.getMask(maskBits+netbits)
            tdata["network"] = self.getNetwork(ip,tdata["mask"],maskBits,netbits)
            tdata["broadcast"] = self.getBroadcast(tdata["network"],tdata["mask"])
            self.subnet_info[nid] = tdata

    def getNetwork(self,ip,mask,maskbits,netbits):
        prevnetwork = None
        if len(self.subnet_info.keys()) > 0:
            if self.static:
                prevnetwork = ''.join(list(map(self.convertToBinary,self.subnet_info[list(self.subnet_info.keys())[-1]]["network"])))
                startnetbit = maskbits+1
                endnetbit = maskbits+netbits-1
                ttbinary = "0"*32
                ttbinary = ttbinary[:endnetbit]+"1"+ttbinary[endnetbit+1:]
                network = self.addBinaries(prevnetwork,ttbinary)
                network = list(map(self.convertToDecimal,re.findall("(\d{8})",network)))
            else:
                prevbroadcast = ''.join(list(map(self.convertToBinary,self.subnet_info[list(self.subnet_info.keys())[-1]]["broadcast"])))
                ttbinary = "0"*31
                ttbinary +="1"
                network = self.addBinaries(prevbroadcast,ttbinary)
                network = list(map(self.convertToDecimal,re.findall("(\d{8})",network)))
        else:
            network = [mask[k] & ip[k] for k,v in enumerate(mask)]
        return network

    def getBroadcast(self,network,mask):
        rmask = list(map(lambda x: ~x & 255, mask))
        broadcast = [network[k]|rmask[k] for k,v in enumerate(rmask)]
        return broadcast

    def bitsRequired(self,no):
        return int(np.ceil(np.log2(no)))

    def getMask(self,bits):
        netm = ''
        hostm = ''
        for ind in range(bits,0,-1): netm += '1'
        for ind in range(32-bits,0,-1): hostm += '0'
        mask = netm+hostm
        mask = [ent for ent in re.findall('\d{8}',mask)]
        for k,m in enumerate(mask): mask[k] = np.sum(list(map(int,re.findall('\d',m)))*self.bitVs)
        return mask

    def summary(self):
        for k,info in self.subnet_info.items():
            print("""
                Network No # {}
                Network: {}
                Broadcast: {}
                Mask: {}
            """.format(k,info["network"],info["broadcast"],info["mask"]))

    def addBinaries(self,first,second):
        size = len(first) if len(first) > len(second) else len(second)
        first,second = first[::-1],second[::-1]
        rslt = "0"
        carry = "0"
        for i in range(size):
            if first[i] == "0" and second[i] == "0":
                if carry == "0":
                    rslt = rslt[:i]+"0"+rslt[i+1:]
                else:
                    rslt = rslt[:i]+"1"+rslt[i+1:]
                    carry = "0"
            elif (first[i] == "0" and second[i] == "1") or (first[i] == "1" and second[i] == "0"):
                if carry == "0":
                    rslt = rslt[:i]+"1"+rslt[i+1:]
                else:
                    rslt = rslt[:i]+"0"+rslt[i+1:]
                    carry="1"
            elif (first[i] == "1" and second[i] == "1"):
                if carry == "0":
                    rslt = rslt[:i]+"0"+rslt[i+1:]
                    carry = "1"
                else:
                    rslt = rslt[:i]+"1"+rslt[i+1:]
                    carry[i] = "1"
        return rslt[::-1]

    def convertToBinary(self,num):
        tbin = ''
        tnum = 0
        for shortcut in self.bitVs:
            if (tnum < num) and (not tnum+shortcut > num):
                tnum += shortcut
                tbin += "1"
            else:
                tbin += "0"
        return tbin

    def convertToDecimal(self,binary):
        return int(binary,2)


if __name__ == "__main__":
    # address = input("Address:")
    # data = "{"+input("Enter Data:").replace(" ",",")+"}"

    address = "192.168.1.12/24"
    data = {1:3, 2:5, 6:2}
    
    # ip = IP(address,eval(data))
    ip = Subnet(address,data)
    ip.summary()