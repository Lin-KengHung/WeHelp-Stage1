# -------------task1-------------

print("---task1---")
def find_and_print(messages, current_station):
    greenLine = {
        "Songshan": 1,
        "Nanjing Sanmin": 2,
        "Taipei Arena": 3,
        "Nanjing Fuxing": 4,
        "Songjiang Nanking": 5,
        "Zhongshan": 6,
        "Beimen": 7,
        "Ximen": 8,
        "Xiaonanmen": 9,
        "Chiang Kai-Shek Memorial Hall": 10,
        "Guting": 11,
        "Taipower Building": 12,
        "Gongguan": 13,
        "Wanlong": 14,
        "Jingmei": 15,
        "Dapinling": 16,
        "Qizhang": 17,
        "Xindian City Hall": 18,
        "Xindian": 19,
        "Xiaobitan": 18,
    }

    # 字串處裡
 
    min = 18
    nearest = ""

    for name in list(messages.keys()):
        for station in list(greenLine.keys()):
            if station in messages[name]:
                distance = abs(greenLine[station] - greenLine[current_station])
              
                if bool(current_station == "Xiaobitan") ^ bool(station == "Xiaobitan"):
                    if current_station == "Xindian City Hall" or current_station == "Xindian" or station == "Xindian City Hall" or station == "Xindian":
                        distance += 2

                if min > distance:
                    min = distance
                    nearest = name
                break

    # 計算距離
    print(nearest)


messages={
"Leslie":"I'm at home near Xiaobitan station.",
"Bob":"I'm at Ximen MRT station.",
"Mary":"I have a drink near Jingmei MRT station.",
"Copper":"I just saw a concert at Taipei Arena.",
"Vivian":"I'm at Xindian station waiting for you."
}
find_and_print(messages, "Wanlong") # print Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivian



# -------------task2-------------
# your code here, maybe
print("---task2---")
schedule = {
    "John" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
          21, 22, 23, 24],
    "Bob" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
          21, 22, 23, 24],
    "Jenny" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23, 24]

}
def book(consultants, hour, duration, criteria):
    match criteria:
        case "price":
           consultants.sort(key=lambda x: x["price"])
        case "rate":
            consultants.sort(key=lambda x: x["rate"], reverse=True)
    # print(consultants)
    #  booking = list(range(hour, duration))??

    for request in consultants:
        breakOuterLoop = False
        for time in range(len(schedule[request["name"]])):
            if schedule[request["name"]][time] == hour and schedule[request["name"]][time + duration] == hour + duration:
                print(request["name"])
                schedule[request["name"]] = schedule[request["name"]][:time:] + schedule[request["name"]][time+duration::]
                # print(schedule[request["name"]])
                print
                breakOuterLoop = True
                break
        if breakOuterLoop:
            break
    else:
        print("下次請早")    
# your code here
consultants = [
    {"name":"John", "rate":4.5, "price":1000},
    {"name":"Bob", "rate":3, "price":1200},
    {"name":"Jenny", "rate":3.8, "price":800}
]
book(consultants, 15, 1, "price") # Jenny
book(consultants, 11, 2, "price") # Jenny
book(consultants, 10, 2, "price") # John
book(consultants, 20, 2, "rate") # John
book(consultants, 11, 1, "rate") # Bob
book(consultants, 11, 2, "rate") # No Service
book(consultants, 14, 3, "price") # John



# -------------task3-------------
print("---task3---")
def func(*data):
   
    ##切中間名
    midName=[]
    for i in range(len(data)):
        mid = round(len(data[i])/2-0.1)
        midName.append(data[i][mid])

    ##數次數
    times = {}
    for word in midName:
        if (word in times):
            times[word] += 1
        else:
            times[word] = 1
    
    # prin只出現一次的
    for i in range(len(midName)):
        if times[midName[i]] == 1:
            print(data[i])
            break;
        elif i == len(midName) - 1:
            print("沒有")



func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安
# -------------task4-------------
print("---task4---")
def get_number(index):
    sum = 0;
    for i in range(1,index+1):
        n = -1 if i % 3 == 0 else  4 
        sum += n
    print(sum)

get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70


# -------------task5-------------
print("---task5---")
def find(spaces, stat, n):
# your code her
    car = -1
    min = max(spaces)
    for i in range(len(spaces)):
        if stat[i] == 1 and  min > spaces[i] - n >= 0:
            min = spaces[i] - n
            car = i
    print(car) 

find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2) # print 5
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4) # print -1
find([4, 6, 5, 8], [0, 1, 1, 1], 4) # print 2
