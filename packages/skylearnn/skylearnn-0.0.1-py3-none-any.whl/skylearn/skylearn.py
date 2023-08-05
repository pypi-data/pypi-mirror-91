# -*-coding:utf-8-*-
# Author: yunhao
# Github: https://github.com/yunhao233
# CreatDate: 2021/1/10 16:48
# Description:
def hello():
    print("hello")

def add():
    return "hello world!"

def eig():
    return """
    import numpy as np
try:
    n = [int(i) for i in input().split()]
    if len(n) != 25:
        print("输入有错！")
        exit(0)
    data = np.array(n).reshape(5, 5)
    w, v = np.linalg.eig(data)
    print(w, '\n', v)

except:
    print("输入有错！")
    """
def corr():
    return """
        import numpy as np

    s1 = [float(i) for i in input().split(' ')]
    s2 = [int(i) for i in input().split(' ')]
    n = np.array(s1).reshape(s2[0], s2[1])
    #求相关系数
    m = np.corrcoef(n)
    print(m)
    """

def linearRegression():
    return """
    import numpy as np
from sklearn import linear_model

x = np.array([float(i) for i in input().split()]).reshape(-1,1)
y = np.array([float(i) for i in input().split()]).reshape(-1,1)
z = np.array(int(input())).reshape(-1,1)

model = linear_model.LinearRegression()
model.fit(x,y)

predict = model.predict(z)

print("Predict 12 inch cost:${:.2f}".format(predict[0][0]))
    """

def fisher():
    return """
    from numpy import *
x = input().split(",")
y = input().split(",")
p1 = mat(vstack([x,y]),dtype=float)
x = input().split(",")
y = input().split(",")
p2 = mat(vstack([x,y]),dtype=float)

tt = input().split(",")
test = mat(vstack([tt[0],tt[1]]),dtype=float)

u1 = mean(p1,axis=1)
u2 = mean(p2,axis=1)

tp1 = p1 - u1
tp2 = p2 - u2

s = 0
for i in range(0,p1.shape[1]):
    s += dot(tp1[:,i],tp1[:,i].T)

for i in range(0,p2.shape[1]):
    s += dot(tp2[:,i],tp2[:,i].T)

W = dot(s.I,u2-u1).T

if abs(0.6 * dot(W,test-u1)) > abs(0.4 * dot(W,test-u2)):
    print("该点属于第二类")
else:
    print("该点属于第一类")
    """

def mainfunc():
    return """
    import numpy as np

a = input()
b = input()
bb = np.array([int(i) for i in b.split(',')])
num = np.array([float(i) for i in a.split(',')]).reshape(bb[0], bb[1])
x = (num - np.mean(num)) / np. std(num)
x1 = np.cov(x.T)
# 特征值和特征向量
w,v = np.linalg.eig(x1)
if w[0] > w[1]:
    index = 0
else:
    index = 1
print("第1主成分={:.5f}*(x1-{:.2f}){:+.5f}*(x2-{:.2f})".format(v[0][index],np.mean(num,axis=0)[0],v[1][index],np.mean(num,axis=0)[1]))
    """

def kmeans():
    return """
    import numpy as np
from sklearn.cluster import KMeans

a = input()
b = input()
c = input()

t1 = np.array([float(i) for i in a.split()])
t2,t3 = np.array([int(i) for i in b.split()])
t4 = int(c)

n = np.array(t1).reshape(t2,t3)

# 指定聚类数目
kmeans = KMeans(n_clusters=t4)
kmeans.fit(n)
m = kmeans.labels_[0]
print("A公司所在类的中心为：{:.2f},{:.2f}。".format(kmeans.cluster_centers_[m,0],kmeans.cluster_centers_[m,1]))
    """

def agglomerative():
    return """
    import numpy as np
from sklearn.cluster import AgglomerativeClustering

temp = np.array([float(i) for i in input().split()])
n_samplesj,n_features = np.array([int(i) for i in input().split()])
n_clusters = int(input())

X = np.array(temp).reshape(n_samplesj,n_features)

hc = AgglomerativeClustering(n_clusters=n_clusters,affinity="correlation",linkage="complete")
hc.fit(X.T)

hc1 = hc.labels_
if hc1[0] == hc1[2]:
    print("香气和酸质属于一类。")
else:
    print("香气和酸质不属于一类。")
    """

def pca():
    return """
    import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
a = input()
b = input()

bb = np.array([int(i) for i in b.split()])
num = np.array([int(i) for i in a.split()]).reshape(bb[0],-1)
x_cor = np.corrcoef(num.T)
w,v = np.linalg.eig(x_cor)
print("对面和汤打分的相关系数为{:.2f}。".format(x_cor[0][1]))

x = scale(num)
pca = PCA(n_components=2)
pca.fit(x)
print("第一主成的方差贡献率为{:.2%} ，第二主成分的方差贡献率为{:.2%}，前两个主成分的累计贡献率为{:.2%}。".format(pca.explained_variance_ratio_[0],pca.explained_variance_ratio_[1],
                                                                            (pca.explained_variance_ratio_[0]+pca.explained_variance_ratio_[1])))
    """
