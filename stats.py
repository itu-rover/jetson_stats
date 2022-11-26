import errno
import sys
import os
import subprocess

class Power:
    def __init__(self):

        self.GPUinstant = 0
        self.GPUaverage = 0
        self.CPUinstant = 0
        self.CPUaverage = 0
        self.CVinstant = 0
        self.CVaverage = 0
        self.VDDRQinstant = 0
        self.VDDRQaverage = 0
        self.SYS5Vinstant = 0
        self.SYS5Vaverage = 0
        self.instantTotal = 0
        self.averageTotal = 0

class Current:
    def __init__(self):

        self.GPUinstant = 0
        self.GPUaverage = 0
        self.CPUinstant = 0
        self.CPUaverage = 0
        self.CVinstant = 0
        self.CVaverage = 0
        self.VDDRQinstant = 0
        self.VDDRQaverage = 0
        self.SYS5Vinstant = 0
        self.SYS5Vaverage = 0
        self.instantTotal = 0
        self.averageTotal = 0

class Temp:
    def __init__(self):

        self.CPU = 0
        self.GPU = 0
        self.board = 0

class Data:
    def __init__(self):
       
        self.voltage = 0
        self.power = Power()
        self.current = Current()
        self.temp = Temp()

    def getData(self):
       
        self.command = subprocess.Popen(['tegrastats'], stdout=subprocess.PIPE)
        self.line = (subprocess.check_output(('head', '-n', '1'), stdin=self.command.stdout)).decode().split(" ")[21:41]

        self.command2 = subprocess.Popen(['cat','/sys/bus/i2c/drivers/ina3221/1-0040/hwmon/hwmon3/in1_input'], stdout=subprocess.PIPE)
        self.voltage = float((self.command2.stdout.readline().decode()).strip()) / 1000

        self.calculate()

    def calculate(self):
        
        self.temp.CPU = (self.line[0].split("@"))[1].split("C")[0]
        self.temp.GPU = (self.line[4].split("@"))[1].split("C")[0]
        self.temp.board = (self.line[2].split("@"))[1].split("C")[0]

        self.power.GPUinstant = float(((self.line[9].split("/"))[0]).split("m")[0]) /1000
        self.power.GPUaverage = float(((self.line[9].split("/"))[1]).split("m")[0]) /1000

        self.power.CPUinstant = float(((self.line[11].split("/"))[0]).split("m")[0]) /1000
        self.power.CPUaverage = float(((self.line[11].split("/"))[1]).split("m")[0]) /1000

        self.power.CVinstant = float(((self.line[15].split("/"))[0]).split("m")[0]) /1000
        self.power.CVaverage = float(((self.line[15].split("/"))[1]).split("m")[0]) /1000

        self.power.VDDRQinstant = float(((self.line[17].split("/"))[0]).split("m")[0]) /1000
        self.power.VDDRQaverage = float(((self.line[17].split("/"))[1]).split("m")[0]) /1000

        self.power.SYS5Vinstant = float(((self.line[19].split("/"))[0]).split("m")[0]) /1000
        self.power.SYS5Vaverage = float(((self.line[19].split("/"))[1]).split("m")[0]) /1000

        self.power.instantTotal = self.power.CPUinstant + self.power.GPUinstant + self.power.CVinstant + self.power.VDDRQinstant + self.power.SYS5Vinstant
        self.power.averageTotal = self.power.CPUinstant + self.power.GPUinstant + self.power.CVinstant + self.power.VDDRQinstant + self.power.SYS5Vinstant

        self.current.CPUaverage = self.power.CPUaverage / self.voltage
        self.current.CPUinstant = self.power.CPUinstant / self.voltage

        self.current.GPUaverage = self.power.GPUaverage / self.voltage
        self.current.GPUinstant = self.power.GPUinstant / self.voltage

        self.current.CVaverage = self.power.CVaverage / self.voltage
        self.current.CVinstant = self.power.CVinstant / self.voltage

        self.current.VDDRQaverage = self.power.VDDRQaverage / self.voltage
        self.current.VDDRQinstant = self.power.VDDRQinstant / self.voltage

        self.current.SYS5Vaverage = self.power.SYS5Vaverage / self.voltage
        self.current.SYS5Vinstant = self.power.SYS5Vinstant / self.voltage

        self.current.instantTotal = self.current.CPUinstant + self.current.GPUinstant + self.current.CVinstant + self.current.VDDRQinstant + self.current.SYS5Vinstant
        self.current.averageTotal = self.current.CPUinstant + self.current.GPUinstant + self.current.CVinstant + self.current.VDDRQinstant + self.current.SYS5Vinstant

        self.printStatus()

    def printStatus(self):
        os.system("clear")
        print("----------Temps-----------")
        print("CPU Temperature: " + str(self.temp.CPU))
        print("GPU Temperature: " + str(self.temp.GPU))
        print("Board Temperature: " + str(self.temp.board))

        print("\n\n-----------Voltages-----------")
        print("Voltage: " + str(self.voltage))
        print("Instant Total Current: " + str(self.current.instantTotal))
        print("Instant Total Power: " + str(self.power.instantTotal))
        print("\n")


if __name__ == "__main__":

    if(os.getuid() == 0):
        while True:
            try:
                status = Data()
                status.getData()
            except KeyboardInterrupt:
                exit(0)
    else:
        print("Please run the program with sudo!!!")
        exit(1)