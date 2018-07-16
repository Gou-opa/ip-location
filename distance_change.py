from math import radians, cos, sin, asin, sqrt,atan2,acos,pi
import numpy as np
import ast
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r * 1000
def read_file1(path):
    fin=open(path,"r")
    tmp=[]
    for line in fin:
        dict=ast.literal_eval(line)
        #print dict
        tmp.append(dict)
    return tmp
def toradians(dist):
	dist/=1.852
	return dist/60.0*pi/180.0
def getq(x1,x2):
	return x1[0]*x2[0]+x1[1]*x2[1]+x1[2]*x2[2]
def geta(r1,r2,q):
	return (cos(r1)-cos(r2)*q)/(1-q*q)
def getb(r1,r2,q):
	return (cos(r2)-cos(r1)*q)/(1-q*q)
def getn(x1,x2):
	return np.cross(x1,x2)
def getx0(a,b,x1,x2):
	return [a*x1[0]+b*x2[0],a*x1[1]+b*x2[1],a*x1[2]+b*x2[2]]
def gett(x0,n):
	return sqrt((1-getq(x0,x0))/getq(n,n))
def getsolution(x0,t,n):
	result=[]
	result.append(x0+t*n)
	result.append(x0-t*n)
	return result
def convert(x,y,z):
	lon=atan2(y,x)/pi*180.0
	lat=atan2(z,sqrt(x*x+y*y))/pi*180.0
	return [lon,lat]
def get_coordinate(lat,lon):
	lon,lat=map(radians,[lon,lat])
	x=cos(lon)*cos(lat)
	y=sin(lon)*cos(lat)
	z=sin(lat)
	return x,y,z
def solve(lon1,lat1,r1,lon2,lat2,r2):
	r1=toradians(r1)
	r2=toradians(r2)
	x1=get_coordinate(lat1,lon1)
	x2=get_coordinate(lat2,lon2)
	q=getq(x1,x2)
	a=geta(r1,r2,q)
	b=getb(r1,r2,q)
	n=getn(x1,x2)
	x0=getx0(a,b,x1,x2)
	if(1-getq(x0,x0)<0):
		return [[0,0],[0,0]]
	t=gett(x0,n)
	tmp=getsolution(x0,t,n)
	result=[]
	result.append(convert(tmp[0][0],tmp[0][1],tmp[0][2]))
	result.append(convert(tmp[1][0],tmp[1][1],tmp[1][2]))
	return result