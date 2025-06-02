from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView, QDialog,
    QGroupBox, QFormLayout, QCheckBox, QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt
from db import Database


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.current_car_id = None
        self.setup_ui()
        self.load_filter_data()
        self.update_cars_table()

    def setup_ui(self):
        self.setWindowTitle("Used Cars Database")
        self.setGeometry(100, 100, 1200, 800)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.setup_view_tab()
        self.setup_add_car_tab()

    def setup_view_tab(self):
        self.view_tab = QWidget()
        layout = QVBoxLayout()

        filter_layout = QHBoxLayout()

        self.model_filter = QLineEdit()
        self.model_filter.setPlaceholderText("Модель")
        self.model_filter.textChanged.connect(self.update_cars_table)

        self.year_filter = QLineEdit()
        self.year_filter.setPlaceholderText("Год")
        self.year_filter.textChanged.connect(self.update_cars_table)

        self.price_min_filter = QLineEdit()
        self.price_min_filter.setPlaceholderText("Цена от")
        self.price_min_filter.textChanged.connect(self.update_cars_table)

        self.price_max_filter = QLineEdit()
        self.price_max_filter.setPlaceholderText("Цена до")
        self.price_max_filter.textChanged.connect(self.update_cars_table)

        self.fuel_type_filter = QComboBox()
        self.fuel_type_filter.addItem("Все типы топлива", "")
        self.fuel_type_filter.currentIndexChanged.connect(self.update_cars_table)

        self.transmission_filter = QComboBox()
        self.transmission_filter.addItem("Все КПП", "")
        self.transmission_filter.currentIndexChanged.connect(self.update_cars_table)

        filter_layout.addWidget(QLabel("Модель:"))
        filter_layout.addWidget(self.model_filter)
        filter_layout.addWidget(QLabel("Год:"))
        filter_layout.addWidget(self.year_filter)
        filter_layout.addWidget(QLabel("Цена от:"))
        filter_layout.addWidget(self.price_min_filter)
        filter_layout.addWidget(QLabel("Цена до:"))
        filter_layout.addWidget(self.price_max_filter)
        filter_layout.addWidget(QLabel("Топливо:"))
        filter_layout.addWidget(self.fuel_type_filter)
        filter_layout.addWidget(QLabel("КПП:"))
        filter_layout.addWidget(self.transmission_filter)

        layout.addLayout(filter_layout)

        self.cars_table = QTableWidget()
        self.cars_table.setColumnCount(8)
        self.cars_table.setHorizontalHeaderLabels(["Модель", "Год", "Цена", "Пробег",
                                                   "Объем двигателя", "Топливо", "КПП", "Владельцы"])
        self.cars_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.cars_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.cars_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.cars_table.setSortingEnabled(True)

        layout.addWidget(self.cars_table)

        control_layout = QHBoxLayout()

        self.view_details_btn = QPushButton("Просмотреть детали")
        self.view_details_btn.clicked.connect(self.show_car_details)

        self.edit_button = QPushButton("Редактировать")
        self.edit_button.clicked.connect(self.edit_selected_car)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_selected_car)

        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.clicked.connect(self.update_cars_table)

        control_layout.addWidget(self.view_details_btn)
        control_layout.addWidget(self.edit_button)
        control_layout.addWidget(self.delete_button)
        control_layout.addWidget(self.refresh_button)

        layout.addLayout(control_layout)

        self.view_tab.setLayout(layout)
        self.tabs.addTab(self.view_tab, "Просмотр автомобилей")

    def setup_add_car_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("Модель автомобиля")
        form_layout.addRow("Модель:", self.model_input)

        self.year_input = QSpinBox()
        self.year_input.setRange(1900, 2025)
        self.year_input.setValue(2020)
        form_layout.addRow("Год:", self.year_input)

        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 1000000)
        self.price_input.setPrefix("$ ")
        form_layout.addRow("Цена:", self.price_input)

        self.mileage_input = QSpinBox()
        self.mileage_input.setRange(0, 1000000)
        self.mileage_input.setSuffix(" км")
        form_layout.addRow("Пробег:", self.mileage_input)

        self.engine_input = QDoubleSpinBox()
        self.engine_input.setRange(0, 10)
        self.engine_input.setSuffix(" л")
        form_layout.addRow("Объем двигателя:", self.engine_input)

        self.fuel_type_input = QComboBox()
        form_layout.addRow("Топливо:", self.fuel_type_input)

        self.transmission_input = QComboBox()
        form_layout.addRow("КПП:", self.transmission_input)

        self.ownership_input = QSpinBox()
        self.ownership_input.setRange(1, 10)
        form_layout.addRow("Кол-во владельцев:", self.ownership_input)

        self.spare_key_input = QCheckBox()
        form_layout.addRow("Запасной ключ:", self.spare_key_input)

        self.imperfections_input = QSpinBox()
        self.imperfections_input.setRange(0, 10)
        form_layout.addRow("Кол-во дефектов:", self.imperfections_input)

        self.repainted_input = QSpinBox()
        self.repainted_input.setRange(0, 10)
        form_layout.addRow("Перекрашенные детали:", self.repainted_input)

        layout.addLayout(form_layout)

        add_button = QPushButton("Добавить автомобиль")
        add_button.clicked.connect(self.add_new_car)
        layout.addWidget(add_button, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Добавить автомобиль")

    def load_filter_data(self):
        models, fuel_types, transmissions = self.db.get_filter_data()

        for fuel in fuel_types:
            self.fuel_type_filter.addItem(fuel, fuel)
            self.fuel_type_input.addItem(fuel)

        for transmission in transmissions:
            self.transmission_filter.addItem(transmission, transmission)
            self.transmission_input.addItem(transmission)

    def update_cars_table(self):
        model = self.model_filter.text().strip()
        year = self.year_filter.text().strip()
        price_min = self.price_min_filter.text().strip()
        price_max = self.price_max_filter.text().strip()
        fuel_type = self.fuel_type_filter.currentData()
        transmission = self.transmission_filter.currentData()

        if not any([model, year, price_min, price_max, fuel_type, transmission]):
            cars = self.db.get_all_cars()
        else:
            cars = self.db.filter_cars(
                model=model,
                year=year,
                price_min=price_min,
                price_max=price_max,
                fuel_type=fuel_type,
                transmission=transmission
            )

        sort_column = self.cars_table.horizontalHeader().sortIndicatorSection()
        sort_order = self.cars_table.horizontalHeader().sortIndicatorOrder()

        self.cars_table.setRowCount(len(cars))
        for row_idx, car in enumerate(cars):
            car_id, model_name, year, price, mileage, engine_capacity, fuel_type, transmission, ownership, spare_key, imperfections, repainted_parts = car

            self.cars_table.setItem(row_idx, 0, self.create_table_item(model_name, car_id))
            self.cars_table.setItem(row_idx, 1, self.create_table_item(str(year), car_id))
            self.cars_table.setItem(row_idx, 2, self.create_table_item(f"${price:,.0f}", car_id))
            self.cars_table.setItem(row_idx, 3, self.create_table_item(f"{mileage:,} км", car_id))
            self.cars_table.setItem(row_idx, 4, self.create_table_item(f"{engine_capacity} л", car_id))
            self.cars_table.setItem(row_idx, 5, self.create_table_item(fuel_type, car_id))
            self.cars_table.setItem(row_idx, 6, self.create_table_item(transmission, car_id))
            self.cars_table.setItem(row_idx, 7, self.create_table_item(str(ownership), car_id))

        if sort_column >= 0:
            self.cars_table.sortByColumn(sort_column, sort_order)

    def create_table_item(self, text, car_id):
        item = QTableWidgetItem(text)
        item.setData(Qt.ItemDataRole.UserRole, car_id)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        return item

    def show_car_details(self):
        selected_row = self.cars_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите автомобиль из таблицы!")
            return

        car_id = self.cars_table.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)
        car_info = self.db.get_car_by_id(car_id)

        dialog = QDialog(self)
        dialog.setWindowTitle("Детали автомобиля")
        dialog.setMinimumSize(600, 400)

        layout = QVBoxLayout()

        info_group = QGroupBox("Информация об автомобиле")
        info_layout = QFormLayout()

        model_name, year, price, mileage, engine_capacity, fuel_type, transmission, ownership, spare_key, imperfections, repainted_parts = car_info

        info_layout.addRow("Модель:", QLabel(model_name))
        info_layout.addRow("Год:", QLabel(str(year)))
        info_layout.addRow("Цена:", QLabel(f"${price:,.0f}"))
        info_layout.addRow("Пробег:", QLabel(f"{mileage:,} км"))
        info_layout.addRow("Объем двигателя:", QLabel(f"{engine_capacity} л"))
        info_layout.addRow("Топливо:", QLabel(fuel_type))
        info_layout.addRow("КПП:", QLabel(transmission))
        info_layout.addRow("Кол-во владельцев:", QLabel(str(ownership)))
        info_layout.addRow("Запасной ключ:", QLabel("Да" if spare_key else "Нет"))
        info_layout.addRow("Кол-во дефектов:", QLabel(str(imperfections)))
        info_layout.addRow("Перекрашенные детали:", QLabel(str(repainted_parts)))

        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)

        dialog.setLayout(layout)
        dialog.exec()

    def edit_selected_car(self):
        selected_row = self.cars_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите автомобиль для редактирования!")
            return

        car_id = self.cars_table.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)
        car_info = self.db.get_car_by_id(car_id)

        dialog = QDialog(self)
        dialog.setWindowTitle("Редактирование автомобиля")
        dialog.setMinimumWidth(500)

        layout = QFormLayout()

        model_name, year, price, mileage, engine_capacity, fuel_type, transmission, ownership, spare_key, imperfections, repainted_parts = car_info

        model_edit = QLineEdit(model_name)
        year_edit = QSpinBox()
        year_edit.setRange(1900, 2025)
        year_edit.setValue(year)
        price_edit = QDoubleSpinBox()
        price_edit.setRange(0, 1000000)
        price_edit.setValue(price)
        mileage_edit = QSpinBox()
        mileage_edit.setRange(0, 1000000)
        mileage_edit.setValue(mileage)
        engine_edit = QDoubleSpinBox()
        engine_edit.setRange(0, 10)
        engine_edit.setValue(engine_capacity)
        fuel_combo = QComboBox()
        fuel_combo.addItems([f[0] for f in self.db.get_filter_data()[1]])
        fuel_combo.setCurrentText(fuel_type)
        transmission_combo = QComboBox()
        transmission_combo.addItems([t[0] for t in self.db.get_filter_data()[2]])
        transmission_combo.setCurrentText(transmission)
        ownership_edit = QSpinBox()
        ownership_edit.setRange(1, 10)
        ownership_edit.setValue(ownership)
        spare_key_check = QCheckBox()
        spare_key_check.setChecked(spare_key)
        imperfections_edit = QSpinBox()
        imperfections_edit.setRange(0, 10)
        imperfections_edit.setValue(imperfections)
        repainted_edit = QSpinBox()
        repainted_edit.setRange(0, 10)
        repainted_edit.setValue(repainted_parts)

        layout.addRow("Модель:", model_edit)
        layout.addRow("Год:", year_edit)
        layout.addRow("Цена:", price_edit)
        layout.addRow("Пробег:", mileage_edit)
        layout.addRow("Объем двигателя:", engine_edit)
        layout.addRow("Топливо:", fuel_combo)
        layout.addRow("КПП:", transmission_combo)
        layout.addRow("Кол-во владельцев:", ownership_edit)
        layout.addRow("Запасной ключ:", spare_key_check)
        layout.addRow("Кол-во дефектов:", imperfections_edit)
        layout.addRow("Перекрашенные детали:", repainted_edit)

        button_box = QHBoxLayout()
        save_button = QPushButton("Сохранить")
        cancel_button = QPushButton("Отмена")

        save_button.clicked.connect(lambda: self.save_car_changes(
            dialog, car_id,
            model_edit.text(),
            year_edit.value(),
            price_edit.value(),
            mileage_edit.value(),
            engine_edit.value(),
            fuel_combo.currentText(),
            transmission_combo.currentText(),
            ownership_edit.value(),
            spare_key_check.isChecked(),
            imperfections_edit.value(),
            repainted_edit.value()
        ))
        cancel_button.clicked.connect(dialog.reject)

        button_box.addWidget(save_button)
        button_box.addWidget(cancel_button)
        layout.addRow(button_box)

        dialog.setLayout(layout)
        dialog.exec()

    def save_car_changes(self, dialog, car_id, model_name, year, price, mileage,
                         engine_capacity, fuel_type, transmission, ownership,
                         spare_key, imperfections, repainted_parts):
        if not model_name:
            QMessageBox.warning(self, "Ошибка", "Название модели не может быть пустым!")
            return

        try:
            self.db.update_car(
                car_id, model_name, year, price, mileage, engine_capacity,
                fuel_type, transmission, ownership, spare_key,
                imperfections, repainted_parts
            )
            QMessageBox.information(self, "Успех", "Изменения сохранены!")
            dialog.accept()
            self.update_cars_table()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении: {str(e)}")

    def delete_selected_car(self):
        selected_row = self.cars_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите автомобиль для удаления!")
            return

        car_id = self.cars_table.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)
        car_name = self.cars_table.item(selected_row, 0).text()

        reply = QMessageBox.question(
            self, 'Подтверждение',
            f'Вы уверены, что хотите удалить автомобиль "{car_name}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_car(car_id)
                QMessageBox.information(self, "Успех", "Автомобиль удален!")
                self.update_cars_table()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении: {str(e)}")

    def add_new_car(self):
        model_name = self.model_input.text().strip()
        year = self.year_input.value()
        price = self.price_input.value()
        mileage = self.mileage_input.value()
        engine_capacity = self.engine_input.value()
        fuel_type = self.fuel_type_input.currentText()
        transmission = self.transmission_input.currentText()
        ownership = self.ownership_input.value()
        spare_key = self.spare_key_input.isChecked()
        imperfections = self.imperfections_input.value()
        repainted_parts = self.repainted_input.value()

        if not model_name:
            QMessageBox.warning(self, "Ошибка", "Введите модель автомобиля!")
            return

        try:
            car_id = self.db.add_car(
                model_name, year, price, mileage, engine_capacity,
                fuel_type, transmission, ownership, spare_key,
                imperfections, repainted_parts
            )
            QMessageBox.information(self, "Успех", f"Автомобиль добавлен с ID: {car_id}")

            self.model_input.clear()
            self.year_input.setValue(2020)
            self.price_input.setValue(0)
            self.mileage_input.setValue(0)
            self.engine_input.setValue(0)
            self.update_cars_table()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить автомобиль: {str(e)}")