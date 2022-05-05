import numpy
import time
import matplotlib.pyplot as plt


class LinkedList:
    def __init__(self, slots):
        self.hashList = [[] for _ in range(0, slots)]
        self.m = slots
        self.n = 0
        self.collisions = 0

    def insert(self, value):
        slot = value % self.m
        if len(self.hashList[slot]) != 0:
            self.collisions += 1
        self.hashList[slot].append(value)
        self.n += 1

    def search_or_delete(self, value, delete):  # if delete == True it will delete, otherwise it will search
        found = False
        slot = value % self.m
        for i in range(0, len(self.hashList[slot])):
            if self.hashList[slot][i] == value:
                found = True
                # print(("Found " if not delete else "Found and deleted ") + "value " + str(value)
                # + " in slot " + str(slot))
                if delete:
                    self.hashList[slot].pop(i)
                    self.n -= 1
                return
        # if not found:
        # print("Value " + str(value) + " not found")

    def print_data(self):
        # print(self.hashList)
        print("Values in list: " + str(self.n))
        print("Total collisions: " + str(self.collisions))
        print("Loading factor: " + str(self.loading_factor()))

    def loading_factor(self):
        return self.n / self.m


class OpenAddressList:
    def __init__(self, slots):
        self.hashList = [None for _ in range(0, slots)]
        self.m = slots
        self.n = 0
        self.collisions = 0

    def insert(self, value):
        slot = value % self.m
        count = 0
        while self.hashList[slot] is not None and self.hashList[slot] != "del":
            if count == self.m:
                print("Hash table full, value " + str(value) + " not inserted!")
                break
            slot += 1
            slot = slot % self.m
            self.collisions += 1
            count += 1
        if self.hashList[slot] is None or self.hashList[slot] == "del":
            self.hashList[slot] = value
            self.n += 1

    def search_or_delete(self, value, delete):
        slot = value % self.m
        count = 0
        while 1:
            if count == self.m:
                # print("Value " + str(value) + " not found")
                break
            if self.hashList[slot] == value:
                # print("Value " + str(value) + " found in slot " + str(slot))
                if delete:
                    self.hashList[slot] = "del"
                    print("Value " + str(value) + " deleted")
                    self.n -= 1
                break
            if self.hashList[slot] is None:
                # print("Value " + str(value) + " not found")
                break
            count += 1
            slot += 1
            slot = slot % self.m

    def print_data(self):
        # print(self.hashList)
        print("Values in list: " + str(self.values_in_list()))
        print("Total collisions: " + str(self.collisions))
        print("Loading factor: " + str(self.loading_factor()))

    def values_in_list(self):
        values = 0
        for i in range(0, len(self.hashList)):
            if self.hashList[i] != "del" and self.hashList[i] is not None:
                values += 1
        return values

    def loading_factor(self):
        return self.n / self.m


linkedListInsertTimes = []
linkedListSearchTimes = []
linkedListCollisions = []
openAddressListInsertTimes = []
openAddressListSearchTimes = []
openAddressListCollisions = []

listSize = 10000
nRuns = 4

for i in range(0, nRuns):
    currentLoadingFactor = 0
    valuesToInsertLength = 0
    count = 0
    print("LINKED RUN ", i + 1)
    while currentLoadingFactor != 100:
        hashLinked = LinkedList(listSize)
        valuesToInsertLength += (listSize * 10)

        valuesToInsert = numpy.random.randint(0, 1000000, valuesToInsertLength)
        startInsTime = time.time()
        for j in range(0, valuesToInsertLength):
            hashLinked.insert(valuesToInsert[j])
        endInsTime = time.time()
        currentLoadingFactor = hashLinked.loading_factor()
        executionInsTime = endInsTime - startInsTime

        valuesToSearch = numpy.random.randint(0, 1000000, listSize)
        startSrcTime = time.time()
        for k in range(0, len(valuesToSearch)):
            hashLinked.search_or_delete(valuesToSearch[k], False)
        endSrcTime = time.time()
        executionSrcTime = endSrcTime - startSrcTime

        if i == 0:
            linkedListInsertTimes.append(executionInsTime)
            linkedListSearchTimes.append(executionSrcTime)
            linkedListCollisions.append(hashLinked.collisions)
        else:
            linkedListInsertTimes[count] += executionInsTime
            linkedListSearchTimes[count] += executionSrcTime
            linkedListCollisions[count] += hashLinked.collisions
        count += 1
        # hashChained.print_data()

for i in range(0, len(linkedListInsertTimes)):
    linkedListInsertTimes[i] = linkedListInsertTimes[i] / nRuns
    linkedListSearchTimes[i] = linkedListSearchTimes[i] / nRuns
    linkedListCollisions[i] = linkedListCollisions[i] / nRuns
print("LINKED LIST INSERTION TIMES: ", linkedListInsertTimes)
print("-------------------------------------------------------")
print("LINKED LIST SEARCH TIMES: ", linkedListSearchTimes)
print("-------------------------------------------------------")
print("LINKED LIST COLLISIONS: ", linkedListCollisions)

for i in range(0, nRuns):
    currentLoadingFactor = 0
    valuesToInsertLength = 0
    count = 0
    print("OPEN ADDRESS RUN ", i + 1)
    while currentLoadingFactor != 1:
        hashOpen = OpenAddressList(listSize)
        valuesToInsertLength += 1000

        valuesToInsert = numpy.random.randint(0, 1000000, valuesToInsertLength)
        startInsTime = time.time()
        for j in range(0, valuesToInsertLength):
            hashOpen.insert(valuesToInsert[j])
        endInsTime = time.time()
        currentLoadingFactor = hashOpen.loading_factor()
        executionInsTime = endInsTime - startInsTime

        valuesToSearch = numpy.random.randint(0, 1000000, listSize)
        startSrcTime = time.time()
        for k in range(0, len(valuesToSearch)):
            hashOpen.search_or_delete(valuesToSearch[k], False)
        endSrcTime = time.time()
        executionSrcTime = endSrcTime - startSrcTime

        if i == 0:
            openAddressListInsertTimes.append(executionInsTime)
            openAddressListSearchTimes.append(executionSrcTime)
            openAddressListCollisions.append(hashOpen.collisions)
        else:
            openAddressListInsertTimes[count] += executionInsTime
            openAddressListSearchTimes[count] += executionSrcTime
            openAddressListCollisions[count] += hashOpen.collisions
        count += 1

print("-------------------------------------------------------")
print("-------------------------------------------------------")
print("-------------------------------------------------------")
for i in range(0, len(openAddressListInsertTimes)):
    openAddressListInsertTimes[i] = openAddressListInsertTimes[i] / nRuns
    openAddressListSearchTimes[i] = openAddressListSearchTimes[i] / nRuns
    openAddressListCollisions[i] = openAddressListCollisions[i] / nRuns
print("OPEN ADDRESS LIST INSERTION TIMES: ", openAddressListInsertTimes)
print("-------------------------------------------------------")
print("OPEN ADDRESS LIST SEARCH TIMES: ", openAddressListSearchTimes)
print("-------------------------------------------------------")
print("OPEN ADDRESS LIST COLLISIONS: ", openAddressListCollisions)

plt.plot([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], linkedListInsertTimes, 'o-')
plt.plot([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], linkedListSearchTimes, 'o-')
plt.title("Inserimento e ricerca per hash con concatenazione")
plt.xlabel("Fattore di caricamento")
plt.ylabel("Tempo (s)")
plt.legend(["Inserimento", "Ricerca"])
plt.show()

plt.plot([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], linkedListCollisions, 'o-')
plt.title("Collisioni per hash con concatenazione")
plt.xlabel("Fattore di caricamento")
plt.ylabel("Collisioni")
plt.show()

plt.yscale("log")
plt.ylim(0.00001, 100)
plt.plot([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], openAddressListInsertTimes, 'o-')
plt.plot([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], openAddressListSearchTimes, 'o-')
plt.title("Inserimento e ricerca per hash con indirizzamento aperto")
plt.xlabel("Fattore di caricamento")
plt.ylabel("Tempo (s)")
plt.legend(["Inserimento", "Ricerca"])
plt.show()

plt.yscale("log")
plt.ylim(10, 1000000)
plt.plot([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], openAddressListCollisions, 'o-')
plt.title("Collisioni per hash con indirizzamento aperto")
plt.xlabel("Fattore di caricamento")
plt.ylabel("Collisioni")
plt.show()
