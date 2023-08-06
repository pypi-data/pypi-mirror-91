import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE



class Logistic_regression_plot():

    def __init__(self, model):
        self.model = model
        self.train_class0_color = "#800080"
        self.train_class1_color = "#FFA500"
        self.test_class0_color = "#00BFFF"
        self.test_class1_color = "#FF1493"
        self.title = "Logistic regression visulisation"
        self.background_color = (0, 0, 0)
        self.train_class0_label = "class0 train"
        self.train_class1_label = "class1 train"
        self.test_class0_label = "class0 test"
        self.test_class1_label = "class1 test"
        self.test_alpha = 0.6
        self.train_alpha = 0.9
        self.color_dict = {"Red": "#FF0000", "Orange": "#FFA500", "Yellow": "#FFFF00", "DeepPink": "#FF1493",
                           "LightPink": "#FFB6C1", "LightPink": "#FFB6C1"
            , "Pink": "#FFC0CB", "Lavender": "#E6E6FA", "Orchid": "#DA70D6", "Violet": "#EE82EE",
                           "DarkOrchid": "#9932CC", "DarkViolet": "#9400D3"
            , "BlueViolet": "#8A2BE2", "Purple": "#800080", "Purple": "#800080", "Indigo": "#4B0082",
                           "Salmon": "#FA8072", "Crimson": "#DC143C", "DarkRed": "#8B0000",
                           "DarkOrange": "#FF8C00", "Coral": "#FF7F50", "OrangeRed": "#FF4500", "Gold": "#FFD700",
                           "GreenYellow": "#ADFF2F", "Lime": "#00FF00", "PaleGreen": "#98FB98"
            , "SpringGreen": "#00FF7F", "Green": "#008000", "LightSeaGreen": "#20B2AA", "Cyan": "#00FFFF",
                           "Aquamarine": "#7FFFD4", "SkyBlue": "#87CEEB",
                           "DeepSkyBlue": "#00BFFF", "Blue": "#0000FF", "MediumBlue": "#0000CD", "Navy": "#000080",
                           "Black": "#000000", "Gray": "#808080"}



    def set_plot_properties(self, train_alpha = 0.9,test_alpha = 0.6,test_class1_label = "class1 test",test_class0_label = "class0 test",train_class1_label = "class1 train", train_class0_label = "class0 train", background_color = (0, 0, 0),title = "Logistic regression visulisation",train_class0_color = "#800080", train_class1_color = "#FFA500", test_class0_color = "#00BFFF", test_class1_color = "#FF1493"):
        self.train_class0_color = train_class0_color
        self.train_class1_color = train_class1_color
        self.test_class0_color = test_class0_color
        self.test_class1_color = test_class1_color
        self.title = title
        self.background_color = background_color
        self.train_class0_label = train_class0_label
        self.train_class1_label = train_class1_label
        self.test_class0_label = test_class0_label
        self.test_class1_label = test_class1_label
        self.test_alpha = test_alpha
        self.train_alpha = train_alpha




    def plot_3D_calculations(self, model1, x, y):
        tsne_data = model1.fit_transform(x)
        class1 = []
        class2 = []

        for i in range(len(y)):
            if y[i] == 0:
                class1.append(tsne_data[i])
            else:
                class2.append(tsne_data[i])

        class1 = np.array(class1).T
        class2 = np.array(class2).T
        return class1, class2



    def plot_3D_visuals(self, plot_train_data =True, plot_test_data = False, save_fig_path="dont"):
        model1 = TSNE(n_components=3)

        if plot_train_data:
             class1, class2 = self.plot_3D_calculations(model1, self.model.x, self.model.y)
        if plot_test_data:
             class3, class4 = self.plot_3D_calculations(model1, self.model.x_calculated, self.model.y_calculated)

        plt.style.use('dark_background')

        fig = plt.figure(figsize=(12, 12))
        ax = plt.axes(projection='3d')
        ax.text2D(0.30, 0.98, self.title, transform=ax.transAxes)

        ax.set_facecolor(self.background_color)
        if plot_train_data:
            ax.text2D(0.90, 0.98, self.train_class0_label, transform=ax.transAxes, color=self.train_class0_color)
            ax.text2D(0.90, 0.94, self.train_class1_label, transform=ax.transAxes, color=self.train_class1_color)
            ax.scatter3D(class1[0], class1[1], class1[2], color=self.train_class0_color, alpha=self.train_alpha, label = self.train_class0_label)
            ax.scatter3D(class2[0], class2[1], class2[2], color=self.train_class1_color, alpha=self.train_alpha, label= self.train_class1_label)
        if plot_test_data:
            ax.text2D(0.90, 0.90, self.test_class0_label, transform=ax.transAxes, color=self.test_class0_color)
            ax.text2D(0.90, 0.86, self.test_class1_label, transform=ax.transAxes, color=self.test_class1_color)
            ax.scatter3D(class3[0], class3[1], class3[2], color=self.test_class0_color, alpha=self.test_alpha, label=self.test_class0_label)
            ax.scatter3D(class4[0], class4[1], class4[2], color=self.test_class1_color, alpha=self.test_alpha, label=self.test_class1_label)
        if not(save_fig_path=="dont"):
            plt.savefig(save_fig_path)

        plt.show()




