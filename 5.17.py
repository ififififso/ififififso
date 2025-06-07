#监督学习 垃圾分类模型
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

x = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14], [15, 16], [17, 18], [19, 20]]
y = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
model = LogisticRegression()
model.fit(x_train, y_train)

from sklearn.metrics import classification_report
predictions = model.predict(x_test)
print(classification_report(y_test, predictions))


from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

data, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)
plt.scatter(data[:,0], data[:,1])
plt.show()


#非监督学习 聚类分析
from sklearn.cluster import KMeans

wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(data)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 11), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

kmeans = KMeans(n_clusters=4, init='k-means++', max_iter=300, n_init=10, random_state=0)
pred_y = kmeans.fit_predict(data)
plt.scatter(data[:,0], data[:,1])
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='red')
plt.show()

