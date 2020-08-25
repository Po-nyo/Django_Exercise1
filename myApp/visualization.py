import pandas as pd
import folium
import plotly.offline as plot
import plotly.express as px


class VisualizationFolium:

    def __init__(self):
        self.df = pd.read_csv('./data/older_population.csv')
        self.df2 = pd.read_csv('./data/전국푸드트럭허가구역.csv')
        self.geo_data = './data/seoul-dong.geojson'

    def get_figure(self, area):
        center = [37.541, 126.986]

        m = folium.Map(location=center, zoom_start=10)

        if area is None or area == '동':
            folium.Choropleth(
                geo_data=self.geo_data,
                data=self.df,
                columns=('동', '인구'),
                key_on='feature.properties.동',
                fill_color='BuPu',
                legend_name='노령 인구수',
            ).add_to(m)
        else:
            df_adm = self.df.groupby(['구'])['인구'].sum().to_frame().reset_index()

            folium.Choropleth(
                geo_data=self.geo_data,
                data=df_adm,
                columns=('구', '인구'),
                key_on='feature.properties.구',
                fill_color='BuPu',
                legend_name='노령 인구수',
            ).add_to(m)

        figure = folium.Figure()
        m.add_to(figure)
        figure.render()

        return figure

    def get_foodtruck_figure(self):
        center = [36.701553, 127.941129]

        m = folium.Map(location=center, zoom_start=7)

        for i in self.df2.index[:]:
            current_loc = self.df2.loc[i, ['위도', '경도']].dropna()
            if current_loc.size != 0:
                folium.Circle(
                    location=(current_loc['위도'], current_loc['경도']),
                    tooltip=self.df2.loc[i, '시군구명'],
                    radius=200
                ).add_to(m)

        figure = folium.Figure()
        m.add_to(figure)
        figure.render()

        return figure


class VisualizationPlotly:

    def __init__(self):
        self.data = pd.Series(range(10))
        self.gapminder = px.data.gapminder()
        self.iris = px.data.iris()

    def get_gapminder_figure(self):
        figure = px.area(
            self.gapminder,
            x='year',
            y='pop',
            color='continent',
            line_group='country'
        )

        fig_div = plot.offline.plot(figure, output_type='div')

        return fig_div

    def get_iris_figure(self):
        figure = px.scatter(
            self.iris,
            x='petal_width',
            y='petal_length',
            color='species',
            size='sepal_length',
            hover_data=['sepal_width']
        )

        fig_div = plot.offline.plot(figure, output_type='div')

        return fig_div
