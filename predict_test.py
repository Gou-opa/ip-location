from math import radians, cos, sin, asin, sqrt,atan2,acos,pi
import sys
import numpy as np
import distance_change as dc
import random


def printline():
    print("*"*50)


def haversine(lon1, lat1, lon2, lat2):             #calculate the distance between two points
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r


def check(lon_1,lat_1,lon_2,lat_2,restriction):
    if haversine(lon_1,lat_1,lon_2,lat_2)<=restriction:
        return True
    else:
        return False


def router_distance(target,landmark):
    routers_of_target=target['routers']
    routers_of_landmark=landmark['routers']
    for i in range(len(routers_of_target)-1,-1,-1):
        router_of_target=routers_of_target[i]
        for j in range(len(routers_of_landmark)-1,-1,-1):
            router_of_landmark=routers_of_landmark[j]
            if router_of_target==router_of_landmark:
                return len(routers_of_target)+len(routers_of_landmark)-i-j
    return len(routers_of_target)+len(routers_of_landmark)


def estimate_error(target,landmarks,radius):
    distance=[]
    intersection_point=[]                  #get intersection point of different circles
    number_of_pair_not_crossed = 0
    for i in range(len(landmarks)):
        landmark=landmarks[i]
        distance.append(router_distance(target, landmark))
    for i in range(len(landmarks)):
        if i%100==0:
            print(" the {}th in {} landmarks ".format(i + 1, len(landmarks)))
        for j in range(i+1,len(landmarks)):
            try:
                point = dc.solve(landmarks[i]["location"]["longitude"], landmarks[i]["location"]["latitude"],
                                 distance[i] * radius, landmarks[j]["location"]["longitude"],
                                 landmarks[j]["location"]["latitude"], distance[j] * radius)
                for j in point:
                    intersection_point.append(j)
            except:
                number_of_pair_not_crossed +=1
                print("{} pairs of landmarks are unfitted for this target".format(number_of_pair_not_crossed))
    ###filter intersection points
    flag=np.ones(len(intersection_point))
    for i in range(len(intersection_point)):
        if i%100==0:
            print("checking the {}th point in {} points".format(i+1, len(intersection_point)))
        number=0.
        for j in range(len(landmarks)):
            if check(intersection_point[i][0],intersection_point[i][1],landmarks[j]["location"]["longitude"],landmarks[j]["location"]["latitude"],radius*distance[j]):
                continue
            else:
                number+=1.
                if number>len(landmarks)*0.2:
                    flag[i]=0
                    break
    ###return the result
    lon=0.
    lat=0.
    num=0.
    for i in range(len(intersection_point)):
        if i%100==0:
            print("calculating {} points in {} points".format(i+1, len(intersection_point)))
        if flag[i]:
            lon+=intersection_point[i][0]
            lat+=intersection_point[i][1]
            num+=1
    lon/=num
    lat/=num
    return haversine(lon,lat,target["location"]["longitude"],target["location"]["latitude"]), number_of_pair_not_crossed


def main():
    landmark_set = []
    target_set = []
    f1 = open("11000001ipscout_marker_landmarks.txt", 'r')
    f2 = open("11000001ipscout_marker_targets.txt", 'r')
    f3 = open("11000001ipscout_marker_test_error.txt", 'w')
    f4 = open("11000001ipscout_marker_test_number_unfited_pair.txt",'w')
    for line in f1:
        landmark_set.append(eval(line))
    for line in f2:
        target_set.append(eval(line))
    print("there are {} landmarks".format(len(landmark_set)))
    print("there are {} targets to predict".format(len(target_set)))
    error = []
    number = []
    radius = 10
    not_success_number = []
    for i in range(len(target_set)):
        printline()
        print(i+1)
        tmp,tmp2=estimate_error(target_set[i],landmark_set,radius)
        error.append(tmp)
        not_success_number.append(tmp2)
        print("success")
    f3.write(str(error))
    f4.write(str(not_success_number))
    f1.close()
    f2.close()
    f3.close()
    f4.close()


main()