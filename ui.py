from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtCore import QEvent
from PySide6.QtGui import QIcon, QMovie, QAction, QPixmap
from PySide6.QtWidgets import (QWidget, QMainWindow, QStackedWidget, QLabel, QLineEdit, QPushButton,
                               QGridLayout, QHBoxLayout, QVBoxLayout,
                               QSizePolicy, QScrollArea, QButtonGroup, QStatusBar, QSystemTrayIcon, QMenu,
                               QStackedLayout, QToolButton, QSpacerItem)
from PySide6 import QtWidgets
from resources import *


class Widgets(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        central_widget.setObjectName("central_widget")
        self.setCentralWidget(central_widget)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowMaximizeButtonHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        # Tile bar container
        self.title_bar_header = QWidget()
        self.title_bar_header.setFixedHeight(45)
        self.title_bar_header.setObjectName("title_bar_header")

        # Tile bar, spacer, text & icon
        title_bar = QWidget()
        title_bar.setFixedWidth(170)

        title_bar_text = QLabel("Weather")
        title_bar_icon = QLabel()
        cloud_icon = QPixmap(u":/all_icons/penguin.png")
        cloud_icon = cloud_icon.scaled(64, 64)

        title_bar_icon.setPixmap(cloud_icon)

        # Navigation bar
        navigation_bar = QWidget()

        # Window management buttons
        window_management_buttons = QWidget()
        window_management_buttons.setFixedWidth(100)

        quit_button = QToolButton()
        max_min_button = QToolButton()
        hide_button = QToolButton()

        quit_button.setIcon(QPixmap(":/all_icons/icons/others/close.png"))
        max_min_button.setIcon(QPixmap(":/all_icons/icons/others/maximize.png"))
        hide_button.setIcon(QPixmap(":/all_icons/icons/others/hide.png"))

        quit_button.clicked.connect(self.window().close)
        max_min_button.clicked.connect(self.window().showMaximized)
        hide_button.clicked.connect(self.window().showMinimized)

        title_bar_spacer_1 = QSpacerItem(800 - title_bar.width(), 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        title_bar_spacer_2 = QSpacerItem(820 + window_management_buttons.width(), 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Layouts
        self.title_bar_header_layout = QGridLayout(self.title_bar_header)
        title_bar_layout = QGridLayout(title_bar)
        wmb_layout = QGridLayout(window_management_buttons)

        # Adding widgets to layouts
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.addWidget(title_bar_icon,
                                   0, 0)
        title_bar_layout.addWidget(title_bar_text,
                                   0, 1)

        wmb_layout.setContentsMargins(0, 0, 0, 0)
        wmb_layout.addWidget(hide_button,
                             0, 0)
        wmb_layout.addWidget(max_min_button,
                             0, 1)
        wmb_layout.addWidget(quit_button,
                             0, 3)

        self.title_bar_header_layout.setContentsMargins(0, 0, 0, 0)
        self.title_bar_header_layout.addWidget(title_bar,
                                               0, 0)
        self.title_bar_header_layout.addItem(title_bar_spacer_1,
                                               0, 1, )
        self.title_bar_header_layout.addWidget(navigation_bar,
                                               0, 2,
                                               alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.title_bar_header_layout.addItem(title_bar_spacer_2,
                                               0, 3,)
        self.title_bar_header_layout.addWidget(window_management_buttons,
                                               0, 4)

        # Creating page widgets
        self.forecast_page = QWidget()
        self.search_location_page = QWidget()
        self.about_page = QWidget()
        self.settings_page = QWidget()

        h_forecast_scroll_area = QScrollArea()
        h_forecast_scroll_area.setWidget(self.forecast_page)
        h_forecast_scroll_area.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        h_forecast_scroll_area.setWidgetResizable(True)

        # Creating stacked widget
        self.stack = QStackedWidget(self)

        # Adding page widgets to stacked widget
        self.stack.addWidget(h_forecast_scroll_area)     # Index: 0
        self.stack.addWidget(self.search_location_page)  # Index: 1
        self.stack.addWidget(self.about_page)            # Index: 2
        self.stack.addWidget(self.settings_page)         # Index: 3

        # Setting size policy
        self.stack.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Main weather information
        self.h_main_information = QWidget()
        self.h_main_information.setMinimumSize(400, 400)
        self.forecast_page.setContentsMargins(5, 5, 5, 5)

        # Forcast
        h_forecast_scroll_area = QScrollArea()
        self.h_forecast = QWidget()
        h_forecast_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        h_forecast_scroll_area.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        h_forecast_scroll_area.setWidgetResizable(True)
        h_forecast_scroll_area.setWidget(self.h_forecast)
        h_forecast_scroll_area.setMinimumHeight(250)
        self.setStyleSheet("""
            QLabel{
                    background-color: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 15px;
                    outline-bottom-right-radius: 15px;
                    padding: 15px;
                }
        """)

        # Precipitation & Humidity & Cloud labels
        self.h_phc = QWidget()
        self.h_phc.setBaseSize(650, 650)
        self.h_phc.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # UV & Air quality
        self.h_uv_air = QWidget()

        # Air pressure & Wind
        self.h_air_wind = QWidget()

        # Error/Full location name label
        self.full_location_name = QLabel(
            text="Pass US Zipcode, UK Postcode,"
            "\nCanada Postalcode, IP address,"
            "\nLatitude/Longitude (decimal degree)"
            " or city name."
        )

        # Date and time labels
        self.last_updated = QLabel()

        # Icon label
        self.weather_icon = QLabel()

        # Location labels
        self.location_region = QLabel()
        self.location_name = QLabel()
        self.location_country = QLabel()

        # Hour-by-Hour labels
        self.h_hour_forecast = QWidget()

        # Temperature labels
        self.main_temp_c = QLabel()
        self.main_temp_f = QLabel()
        self.feels_like_c = QLabel()
        self.feels_like_f = QLabel()

        # Precipitation labels
        self.precipitation_mm = QLabel()
        self.precipitation_in = QLabel()

        # Humidity and Cloud labels
        self.humidity = QLabel()
        self.cloud = QLabel()

        # UV and Air quality labels
        self.uv = QLabel()
        self.co = QLabel()
        self.no2 = QLabel()
        self.o3 = QLabel()
        self.so2 = QLabel()
        self.pm2_5 = QLabel()
        self.pm10 = QLabel()
        self.us_epa_index = QLabel()
        self.gb_defra_index = QLabel()

        # Air Pressure labels
        self.pressure_mb = QLabel()
        self.pressure_in = QLabel()

        # Wind labels
        self.wind_kmh = QLabel()
        self.wind_mph = QLabel()
        self.wind_degree = QLabel()
        self.wind_direction = QLabel()

        # Visibility labels
        self.visibility_km = QLabel()
        self.visibility_miles = QLabel()

        # Weather condition label
        self.weather_condition = QLabel()

        # Line Edits
        self.location_name_line_edit = QLineEdit()
        self.location_name_line_edit.setPlaceholderText("Search location:")

        forecast_icon = QIcon()

        # --- Search location page button
        self.search_location_button = QPushButton("Search location")
        self.search_location_button.setToolTip("If you want to search location,\n"
                                               "write city name and push this annoying BUTTON!")

        # --- Navigation bar buttons ---
        self.forecast_page_button = QPushButton(text="Forecast",
                                                icon=QtGui.QPixmap("icons/button-icons/forecast.png"))
        self.forecast_page_button.setCheckable(True)
        self.forecast_page_button.setAutoExclusive(True)

        self.search_location_page_button = QPushButton(text="Location",
                                                       icon=QtGui.QPixmap("icons/button-icons/location.png"))
        self.search_location_page_button.setCheckable(True)
        self.search_location_page_button.setAutoExclusive(True)

        self.about_page_button = QPushButton(text="Surprise",
                                             icon=QtGui.QPixmap("icons/button-icons/info.png"))
        self.about_page_button.setCheckable(True)
        self.about_page_button.setAutoExclusive(True)

        self.settings_page_button = QPushButton(text="Settings",
                                                icon=QtGui.QPixmap("icons/button-icons/settings.png"))
        self.settings_page_button.setCheckable(True)
        self.settings_page_button.setAutoExclusive(True)

        self.search_location_page_button.setChecked(True)

        # Thanks to: https://stackoverflow.com/a/61200491/21927402

        self.btn_group = QButtonGroup()
        self.btn_group.addButton(self.forecast_page_button)
        self.btn_group.addButton(self.search_location_page_button)
        self.btn_group.addButton(self.about_page_button)
        self.btn_group.addButton(self.settings_page_button)

        self.btn_group.setId(self.forecast_page_button, 0)
        self.btn_group.setId(self.search_location_page_button, 1)
        self.btn_group.setId(self.about_page_button, 2)
        self.btn_group.setId(self.settings_page_button, 3)

        self.btn_group.idClicked.connect(self.stack.setCurrentIndex)

        # Setting size and policy to the  buttons

        # --- Search location page buttons
        self.search_location_button.setFixedSize(120, 40)

        # --- Navigation bar buttons ---
        self.forecast_page_button.setFixedSize(90, 40)
        self.forecast_page_button.setSizeIncrement(1, 1)

        self.search_location_page_button.setFixedSize(90, 40)

        self.about_page_button.setFixedSize(90, 40)

        self.settings_page_button.setFixedSize(90, 40)

        # Setting size and policy to the line edits
        self.location_name_line_edit.setFixedSize(220, 40)
        self.location_name_line_edit.setAlignment(QtCore.Qt.AlignCenter)

        # Setting size and policy to the labels
        self.full_location_name.setFixedSize(340, 70)
        self.full_location_name.setAlignment(QtCore.Qt.AlignCenter)
        self.full_location_name.setContentsMargins(10, 8, 10, 8)

        self.main_temp_c.setAlignment(QtCore.Qt.AlignCenter)
        self.weather_icon.setAlignment(QtCore.Qt.AlignCenter)

        # Layout
        # --- Creating layouts for pages ---

        self.navigation_bar_layout = QGridLayout(navigation_bar)
        self.forecast_page_layout = QGridLayout(self.forecast_page)
        self.search_location_page_layout = QGridLayout(self.search_location_page)
        self.horizontal_box_layout = QHBoxLayout()

        # Horizontal box layout
        self.horizontal_box_layout.addWidget(self.location_name_line_edit)
        self.horizontal_box_layout.addWidget(self.search_location_button)

        self.horizontal_box_layout.setSpacing(0)

        # Forecast page widgets layout
        self.h_main_information_layout = QGridLayout(self.h_main_information)
        self.h_forecast_layout = QHBoxLayout(self.h_forecast)
        self.h_phc_layout = QGridLayout(self.h_phc)
        self.h_air_wind_layout = QGridLayout(self.h_air_wind)
        self.h_uv_air_layout = QGridLayout(self.h_uv_air)

        # --- Adding widgets to page layouts ---
        navigation_bar.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, True)
        navigation_bar.setFixedSize(365, 55)

        tray = QSystemTrayIcon()
        tray.showMessage("Title", "The message", QtGui.QPixmap("icons/button-icons/forecast.png"), 1400)
        tray.setIcon(QtGui.QPixmap("icons/button-icons/forecast.png"))
        tray.setVisible(True)

        # Create the menu
        menu = QMenu()
        action = QAction("A menu item")
        menu.addAction(action)

        # Add a Quit option to the menu.
        quit = QAction("Quit")
        quit.triggered.connect(lambda: print(0))
        menu.addAction(quit)

        # Add the menu to the tray
        tray.setContextMenu(menu)

        # Forecast page layout
        self.forecast_page_layout.addWidget(self.h_main_information,
                                            0, 0, 1, 0)
        self.forecast_page_layout.addWidget(h_forecast_scroll_area,  # h_forecast
                                            1, 0, 1, 0)
        self.forecast_page_layout.addWidget(self.h_phc,
                                            2, 0)
        self.forecast_page_layout.addWidget(self.h_air_wind,
                                            2, 1)
        self.forecast_page_layout.addWidget(self.h_uv_air,
                                            3, 0, 1, 0)
        self.forecast_page_layout.setContentsMargins(2, 2, 2, 2)

        # About page layout
        m = QMovie("giphy.gif")
        self.varo = QLabel()
        self.varo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.varo.setMovie(m)

        m.start()

        self.about_page_layout = QGridLayout(self.about_page)
        self.about_page_layout.addWidget(self.varo)

        # Location page layout

        spacer_1 = QSpacerItem(10, 1600, QSizePolicy.Minimum, QSizePolicy.Fixed)
        spacer_2 = QSpacerItem(10, 1600,  QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.search_location_page_layout.setSpacing(0)

        self.search_location_page_layout.addWidget(self.full_location_name,
                                                   1, 0, QtCore.Qt.AlignmentFlag.AlignAbsolute)
        self.search_location_page_layout.addLayout(self.horizontal_box_layout,
                                                   2, 0)
        self.search_location_page_layout.addItem(spacer_1,
                                                 0, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignAbsolute)
        self.search_location_page_layout.addItem(spacer_2,
                                                 3, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignAbsolute)

        # Navigation bar layout
        self.navigation_bar_layout.setSpacing(2)
        self.navigation_bar_layout.setContentsMargins(0, 0, 0, 5)
        self.navigation_bar_layout.addWidget(self.forecast_page_button,
                                             0, 2)
        self.navigation_bar_layout.addWidget(self.search_location_page_button,
                                             0, 1)
        self.navigation_bar_layout.addWidget(self.about_page_button,
                                             0, 3)
        self.navigation_bar_layout.addWidget(self.settings_page_button,
                                             0, 0)

        # --- Adding widgets to home page widget layouts ---

        # Home Main-information layout
        self.h_main_information_layout.setSpacing(0)
        hmi_spacer_1 = QSpacerItem(2, 40, QSizePolicy.Fixed)
        hmi_spacer_2 = QSpacerItem(2, 40, QSizePolicy.Fixed)
        self.h_main_information_layout.addItem(hmi_spacer_1,
                                               0, 0)
        self.h_main_information_layout.addWidget(self.main_temp_c,
                                                 1, 0, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.h_main_information_layout.addWidget(self.weather_icon,
                                                 2, 0, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        self.h_main_information_layout.addWidget(self.weather_condition,
                                                 3, 0)
        self.h_main_information_layout.addItem(hmi_spacer_2,
                                               4, 0)

        # Home Precipitation-Humidity-Cloud layout
        self.h_phc_layout.addWidget(self.visibility_km)

        # Home UV-Air layout
        self.h_uv_air_layout.addWidget(self.uv)
        self.h_uv_air_layout.addWidget(self.co)
        self.h_uv_air_layout.addWidget(self.no2)
        self.h_uv_air_layout.addWidget(self.o3)
        self.h_uv_air_layout.addWidget(self.so2)
        self.h_uv_air_layout.addWidget(self.pm2_5)
        self.h_uv_air_layout.addWidget(self.pm10)
        self.h_uv_air_layout.addWidget(self.us_epa_index)
        self.h_uv_air_layout.addWidget(self.gb_defra_index)

        # Main window/self layout management
        self.main_grid_layout = QGridLayout(central_widget)
        self.main_grid_layout.addWidget(self.title_bar_header,
                                        0, 0)

        self.main_grid_layout.addWidget(self.stack,
                                        1, 0,)

        self.main_grid_layout.setSpacing(0)
        self.main_grid_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.main_grid_layout)
    
        # Setting object name
        self.h_main_information.setObjectName("h_main_information")

        current_widget = self.stack.currentWidget()

        # Qt Style Sheet
        self.setStyleSheet("""background: black;
        """)

        self.h_main_information.setStyleSheet("""
        QWidget{
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            outline-bottom-right-radius: 15px;
            padding: 10px;
            }
        QLabel{
            background-color: transparent;
            border: transparent;
        }
        """)

        self.h_forecast.setStyleSheet("""
        QWidget{
            background-color: transparent
            border-radius: 17px;
            }
        QLabel{
            background-color: transparent;
            border: #598FF0;
        }
        """)

        #Source: https://doc.qt.io/qt-6/stylesheet-examples.html#customizing-qscrollbar
        h_forecast_scroll_area.setStyleSheet("""
        
        QScrollBar:horizontal {
            border: 2px solid grey;
            background: #32CC99;
            height: 15px;
            margin: 0px 20px 0 20px;
        }
        QScrollBar::handle:horizontal {
            background: white;
            min-width: 20px;
        }
        QScrollBar::add-line:horizontal {
            border: 2px solid grey;
            background: #32CC99;
            width: 20px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }

        QScrollBar::sub-line:horizontal {
            border: 2px solid grey;
            background: #32CC99;
            width: 20px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }    
        """)

        self.h_phc.setStyleSheet("""
        QWidget{
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            background-color: rgba(255, 255, 255, 0.1);
            outline-bottom-right-radius: 15px;
            padding: 15px;
            }
        QLabel{
            background-color: transparent;
            border: transparent;
        }
        """)

        self.h_uv_air.setStyleSheet("""
        QWidget{
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            background-color: rgba(255, 255, 255, 0.1);
            outline-bottom-right-radius: 15px;
            padding: 15px;
            }
        QLabel{
            background-color: transparent;
            border: transparent;
        }
        """)

        self.h_air_wind.setStyleSheet("""
        QWidget{
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            background-color: rgba(255, 255, 255, 0.1);
            outline-bottom-right-radius: 15px;
            padding: 15px;
            }
        QLabel{
            background-color: transparent;
            border: transparent;
        }
        """)

        self.forecast_page.setStyleSheet("""
        background: qradialgradient(
                cx: 0.3, cy: -0.4, fx: 0.5, fy: -0.4,
                radius: 1.35, stop: 0 #1976d2, stop: 1 #2196f3
                );
        """)

        """
        BTW, this QSS looks pretty sweet, i call it delightful sugar cotton:
            background: qradialgradient(
                cx: 0.1, cy: -0.5, fx: 0.5, fy: -0.9,
                radius: 1.95, stop: 0 #748582, stop: 1 #F65283
                )
        """

        self.main_temp_c.setStyleSheet("""
        QLabel{
            font-size: 40pt;
        }
        """)

        self.weather_condition.setStyleSheet("""
        QLabel{
            font-size: 40pt;
        }
        """)

        self.search_location_page.setStyleSheet("""
            background: black;
        """)

        self.search_location_page.setStyleSheet("""
        QPushButton{
            background-color: #569;
            
            border-bottom-right-radius: 20px;
        }
        QPushButton:hover{
            background-color: #579
        }
        QPushButton:pressed{
            background-color: #568
        }
        QLineEdit{
            border: 1.3px solid #d0e3ff;
            border-bottom-left-radius: 20px;
            color: white;
            background: black;
            selection-color: white;
            selection-background-color: blue;
            lineedit-password-character: 9659;
        }
        QLineEdit:focus {
            border: 1.7px solid white;
        }
        
        """)

        self.full_location_name.setStyleSheet("""
            background: #Fb8F69;
            border-top-right-radius: 20px;
            border-top-left-radius: 20px;
            spacing: 10;
        """)

        navigation_bar.setStyleSheet("""
        QWidget{
            background-color: rgba(31, 149, 239, 0.1);
        }
        QPushButton{
            
            background-color: black;
            color: white;
            border-width: 5px;
            border-radius: 2px;
        }
        QPushButton:pressed{
            
        }
        QPushButton:checked{
        border-bottom: 1.6px solid #F84F99;
        }
        QPushButton:hover{
           
        }
        
        """)
        self.current = QtCore.QPoint()
        self.pressed = False

        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    def clear_layout(self, layout) -> None:
        """
        Deletes the QWidgets from QLayout/QLayout inherited class
        :Source
        https://github.com/dglent/meteo-qt/blob/578088f110fe1495b629323adce291c7a22e9c34/meteo_qt/meteo_qt.py#L1534:
        :param layout:
        """

        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    def delete_widgets(self, layout) -> None:
        """
        Has same job as clear_layout function
        :source https://stackoverflow.com/a/70914343:
        :param layout:
        :return None:
        """
        while (child := layout.takeAt(0)) is not None:
            child.widget().deleteLater(); del child

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            window = self.window().windowHandle()
            window.startSystemMove()
            return super().mousePressEvent(event)
