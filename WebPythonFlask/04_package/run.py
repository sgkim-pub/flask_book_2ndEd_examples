from computer.system import system

computer = system()

for itemStatus in computer.report():
    print(itemStatus)
