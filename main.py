import sys
import httpx
import timeit
from ui import Widgets
from typing import Never
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from credential.API import API_KEY


class Weather(Widgets):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.Window)

        # Setting window icon and default size
        self.setWindowTitle("Open Qt6 Weather")
        self.setWindowIcon(QPixmap(u":/all_icons/penguin.png"))
        self.setMinimumSize(1, 1)
        self.location_name_line_edit.setMaxLength(45)
        self.location_name_line_edit.setCursor(QPixmap("icons/others/search.png"))
        self.location_name_line_edit.editingFinished.connect(self.api_value)
        self.search_location_button.clicked.connect(self.api_value)
        self.stack.setCurrentIndex(1)

    def api_value(self) -> Never:
        """
        :Retrieves requested JSON API data and parses it
        :No return value
        """

        # To clear self.h_forecast_layout from QWidgets

        city = self.location_name_line_edit.text()

        # Requesting weatherapi

        r = httpx.get(
            f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&aqi=yes&alerts=yes"
        )

        value: dict = r.json()  # Translating JSON to Python Dictionary

        key = 0

        # Error handling
        if r.headers["Cache-Control"] == "public, max-age=5" and value["error"]["message"] == "Parameter q is missing.":
            self.full_location_name.setText("Parameter missing ...")
            self.full_location_name.setStyleSheet("""
            border-top-right-radius: 20px;
            border-top-left-radius: 20px;
            background-color: black;
            border: 2px solid pink;
            """)

        elif r.headers["Cache-Control"] == "public, max-age=5":
            self.full_location_name.setText(f"{value["error"]["message"]}")
            self.full_location_name.setStyleSheet("""
            background: qradialgradient(
            cx: 0.9, cy: -0.4, fx: 0.5, fy: -0.7,
            radius: 1.35, stop: 0 #DB3445, stop: 1 #F71735
            );
            border: 2px solid red;
            border-top-right-radius: 20px;
            border-top-left-radius: 20px;
            """)

        elif r.headers["Cache-Control"] != "public, max-age=5":
            self.full_location_name.setText(f"{value["location"]["name"]}, "
                                            f"{value["location"]["country"]}"
                                            f"\nHave been found.")
            self.full_location_name.setStyleSheet("""
                background: qradialgradient(
                cx: 0.1, cy: -0.2, fx: 0.8, fy: -0.8,
                radius: 1.35, stop: 0 #6a3093, stop: 1 #a044ff
                );
                border-width: 19px;
                border: 2px solid green;
                border-top-right-radius: 20px;
                border-top-left-radius: 20px;
            """)

            icon_path = f"icons/{value["current"]["condition"]["icon"][21::]}"
            self.weather_icon.setPixmap(QPixmap(icon_path))

        try:
            """
            The reason we are using try-except keywords is 
            that we might get KeyError when requesting json value.
            So we need to handle errors in order to not let 
            our program crash.
            """
            for i in range(24):  # Length of forecast hour is same as len(value["forecast"]["forecastday"][0]["hour"])
                ico_path = f":/all_icons/icons/{str(value["forecast"]["forecastday"][0]["hour"][i]["condition"]["icon"][21::])}"
                forecast_feels_like_temperature = QLabel(
                    f"Feels like {str(value["forecast"]["forecastday"][0]["hour"][i]["temp_c"])}°C"
                )
                forcast_time = QLabel(str(value["forecast"]["forecastday"][0]["hour"][i]["time"][11::]))
                forecast_condition_icon = QLabel();
                forecast_condition_icon.setPixmap(QPixmap(ico_path))
                forecast_condition = QLabel(str(value["forecast"]["forecastday"][0]["hour"][i]['condition']['text']))
                forecast_temperature = QLabel(str(value["forecast"]["forecastday"][0]["hour"][i]["temp_c"]))

                forecast_feels_like_temperature.setContentsMargins(0, 0, 0, 0)
                forcast_time.setContentsMargins(0, 0, 0, 0)
                forecast_condition_icon.setContentsMargins(0, 0, 0, 0)
                forecast_condition.setContentsMargins(0, 0, 0, 0)
                forecast_temperature.setContentsMargins(0, 0, 0, 0)

                forecast_feels_like_temperature.setMargin(-9)
                forcast_time.setMargin(-12)
                forecast_condition_icon.setMargin(-9)
                forecast_condition.setMargin(-9)
                forecast_temperature.setMargin(-9)

                forecast_feels_like_temperature.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                forcast_time.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                forecast_condition_icon.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                forecast_condition.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                forecast_temperature.setAlignment(Qt.AlignmentFlag.AlignHCenter)

                h_forecast_child_widget = QWidget()
                h_forecast_child_widget.setMinimumSize(110, 95)
                h_forecast_child_layout = QGridLayout(h_forecast_child_widget)

                h_forecast_child_layout.addWidget(
                    forecast_feels_like_temperature,
                    0, 0
                )
                h_forecast_child_layout.addWidget(
                    forcast_time,
                    1, 0
                )
                h_forecast_child_layout.addWidget(
                    forecast_condition_icon,
                    2, 0
                )
                h_forecast_child_layout.addWidget(
                    forecast_condition,
                    3, 0
                )

                h_forecast_child_layout.setContentsMargins(0, 0, 0, 0)
                h_forecast_child_layout.setVerticalSpacing(0)
                # self.h_forecast_layout.removeWidget(h_forecast_child_widget)
                self.h_forecast_layout.addWidget(h_forecast_child_widget)
                h_forecast_child_widget.setStyleSheet("""
                   QWidget{
                       background-color: rgba(111, 111, 111, 8);
                       border: 1px solid rgba(255, 255, 255, 0.3);
                       border-radius: 15px;
                       outline-bottom-right-radius: 15px;
                       padding: 10px;
                   }
                   QLabel{
                       background-color: transparent;
                       border: transparent;
                   }
                """)

            # Temperature labels
            self.main_temp_c.setText(f"{str(value["current"]["temp_c"])}°C")
            self.main_temp_f.setText(f"{str(value["current"]["temp_f"])}°F")
            self.feels_like_c.setText(f"Feels like: {str(value["current"]["feelslike_c"])}°C")
            self.feels_like_f.setText(f"Feels like: {str(value["current"]["feelslike_f"])}°F")

            # Wind labels
            self.wind_kmh.setText(f"Current wind: {str(value["current"]["wind_kph"])}km/h")
            self.wind_mph.setText(f"Current wind: {str(value["current"]["wind_mph"])}mp/h")
            self.wind_degree.setText(f"Wind degree: {str(value["current"]["wind_degree"])}")
            self.wind_direction.setText(f"Wind direction: {str(value["current"]["wind_dir"])}")

            # Air Pressure labels
            self.pressure_mb.setText(f"Pressure: {str(value["current"]["pressure_mb"])} mb")
            self.pressure_in.setText(f"Pressure: {str(value["current"]["pressure_in"])} in")

            # Precipitation labels
            self.precipitation_mm.setText(f"Precipitation: {str(value["current"]["precip_mm"])} mm")
            self.precipitation_in.setText(f"Precipitation: {str(value["current"]["precip_in"])} in")

            # Humidity and Cloud labels
            self.humidity.setText(f"Humidity: {str(value["current"]["humidity"])}")
            self.cloud.setText(f"{str(value["current"]["cloud"])}% of Clouds ")

            # UV and Air quality labels
            self.uv.setText(f"UV: {str(value["current"]["uv"])}")
            self.co.setText(f"Carbon Monoxide/CO: {str(value["current"]["air_quality"]["co"])}")
            self.no2.setText(f"Nitrous Dioxide/NO2: {str(value["current"]["air_quality"]["no2"])}")
            self.o3.setText(f"Ozone/O3: {str(value["current"]["air_quality"]["o3"])}")
            self.so2.setText(f"Sulfur Dioxide/SO2: {str(value["current"]["air_quality"]["so2"])}")
            self.pm2_5.setText(f"PM2.5: {str(value["current"]["air_quality"]["pm2_5"])}")
            self.pm10.setText(f"PM10: {str(value["current"]["air_quality"]["pm10"])}")
            self.us_epa_index.setText(f"Air Quality: {str(value["current"]["air_quality"]["us-epa-index"])}US EPA")
            self.gb_defra_index.setText(f"Air Quality: {str(value["current"]["air_quality"]["gb-defra-index"])}GB DEFRA")

            # Visibility labels
            self.visibility_km.setText(f"Visibility: {str(value["current"]["vis_km"])} km")
            self.visibility_miles.setText(f"Visibility: {str(value["current"]["vis_miles"])} miles")

            # Weather condition label
            self.weather_condition.setText(f"Current weather: {value["current"]["condition"]["text"]}")

            # Date and time labels
            self.last_updated.setText(f"Last updated: {value["location"]["localtime"]}")

            # Location labels
            self.location_name.setText(f"{value["location"]["name"]}")
            self.location_region.setText(f"{value["location"]["region"]}")
            self.location_country.setText(f"{value["location"]["country"]}")

            # Weather condition label
            self.weather_condition.setText(str(value["current"]["condition"]["text"]))
            self.weather_condition.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        except KeyError:

            print("KeyError occurred!")
            self.main_temp_c.clear()
            self.main_temp_f.clear()
            self.feels_like_c.clear()
            self.feels_like_f.clear()
            self.wind_kmh.clear()
            self.wind_mph.clear()
            self.visibility_km.clear()
            self.visibility_miles.clear()
            self.visibility_km.clear()
            self.visibility_miles.clear()
            self.weather_condition.clear()
            self.last_updated.clear()
            self.location_name.clear()
            self.location_region.clear()
            self.location_country.clear()

    @staticmethod
    def credits() -> Never:
        """
    Acknowledgments:
        Flaticon icons used in this project:   https://www.flaticon.com/free-icon
        Streamline icons used in this project: www.streamlinehq.com/icons/core-line-free
        Weatherapi icons used in this project: www.weatherapi.com/docs/#weather-icons
        Special thanks to the authors of       www.pythonguis.com
        API powered by                         weatherapi.com

        Icon resource links:
            https://www.flaticon.com/free-icon/cloud_7646616?term=cloud&page=1&position=10&origin=style&related_id=7646616
            https://www.flaticon.com/free-icon/search_9784071?term=search&page=2&position=73&origin=search&related_id=9784071
            https://www.flaticon.com/free-icon/close_2961937?k=1718212905004
            https://www.flaticon.com/free-icon/maximize_4947644?term=maximize&related_id=4947644
            https://www.flaticon.com/free-icon/minimize_4947691?related_id=4947691
            https://www.streamlinehq.com/icons/core-line-free
            https://www.weatherapi.com/docs/#weather-icons

        Credits:
            www.flaticon.com
            www.streamlinehq.com
            www.weatherapi.com
            www.pythonguis.com
            www.stackoverflow.com
            forum.qt.io
            """


def execute() -> Never:
    application = QApplication(sys.argv)
    instance = Weather()
    instance.show()
    sys.exit(application.exec())


if __name__ == "__main__":
    execute()
