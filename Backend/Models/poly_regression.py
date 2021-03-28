from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn import datasets, linear_model
import operator
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


def PlotGraphs(X, Y, Z):
    plt.scatter(X, Y)
    sort_axis = operator.itemgetter(0)
    sorted_zip = sorted(zip(X, Z), key=sort_axis)
    x, y_poly_pred = zip(*sorted_zip)
    plt.plot(x, y_poly_pred, color="m")
    plt.show()


def CustomPolynomialModelPredict(X, Y, degree):
    poly_features = PolynomialFeatures(degree=degree)
    X_poly = poly_features.fit_transform(X)
    model = LinearRegression()
    model.fit(X_poly, Y)
    Y_poly_predict = model.predict(X_poly)

    rmse = np.sqrt(mean_squared_error(Y, Y_poly_predict))
    r2 = r2_score(Y, Y_poly_predict)

    return model, Y_poly_predict, rmse, r2_score
