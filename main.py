import tkinter as tk
from shapely.geometry import Polygon
from shapely.geometry import Point
import matplotlib.pyplot as plt


class PolygonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Polygon Intersection App")

        # Настройка переменных
        self.canvas = tk.Canvas(root, width=600, height=600, bg='white')
        self.canvas.pack()
        self.polygons = [[], []]  # Два списка для точек каждого полигона
        self.current_poly_index = 0  # Индекс текущего полигона
        self.intersection_poly = None  # Пересечение полигонов

        # Добавление кнопок для управления
        self.btn_switch = tk.Button(root, text="Switch Polygon", command=self.switch_polygon)
        self.btn_switch.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_calculate = tk.Button(root, text="Calculate Intersection", command=self.calculate_intersection)
        self.btn_calculate.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_clear = tk.Button(root, text="Clear", command=self.clear_canvas)
        self.btn_clear.pack(side=tk.LEFT, padx=5, pady=5)

        # Обработка кликов мыши
        self.canvas.bind("<Button-1>", self.add_point)

    def add_point(self, event):
        """Добавляет точку в текущий полигон по щелчку мыши."""
        x, y = event.x, event.y
        self.polygons[self.current_poly_index].append((x, y))
        self.draw_polygon()

    def switch_polygon(self):
        """Переключает текущий полигон для добавления точек."""
        if self.current_poly_index == 0:
            self.current_poly_index = 1
        else:
            self.current_poly_index = 0

    def calculate_intersection(self):
        """Вычисляет пересечение полигонов и отображает его."""
        if len(self.polygons[0]) < 3 or len(self.polygons[1]) < 3:
            print("Оба полигона должны содержать как минимум 3 вершины.")
            return

        poly1 = Polygon(self.polygons[0])
        poly2 = Polygon(self.polygons[1])
        intersection = poly1.intersection(poly2)

        if not intersection.is_empty:
            self.intersection_poly = intersection
            self.draw_intersection()
        else:
            print("Пересечение отсутствует.")

    def draw_polygon(self):
        """Рисует текущий полигон и точки на холсте."""
        self.canvas.delete("poly")

        # Рисуем первый полигон
        if self.polygons[0]:
            self.canvas.create_polygon(self.polygons[0], outline='blue', fill='', width=2, tags="poly")
            for x, y in self.polygons[0]:
                self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='blue', tags="poly")

        # Рисуем второй полигон
        if self.polygons[1]:
            self.canvas.create_polygon(self.polygons[1], outline='green', fill='', width=2, tags="poly")
            for x, y in self.polygons[1]:
                self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='green', tags="poly")

    def draw_intersection(self):
        """Рисует область пересечения полигонов."""
        if self.intersection_poly:
            self.canvas.delete("intersection")
            x, y = self.intersection_poly.exterior.xy
            points = list(zip(x, y))
            self.canvas.create_polygon(points, outline='red', fill='red', stipple="gray50", width=2,
                                       tags="intersection")

    def clear_canvas(self):
        """Очищает холст и сбрасывает все данные."""
        self.canvas.delete("all")
        self.polygons = [[], []]
        self.current_poly_index = 0
        self.intersection_poly = None


# Создаем окно приложения
root = tk.Tk()
app = PolygonApp(root)
root.mainloop()
