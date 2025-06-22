from typing import List, Tuple, Iterator
import math


class RayTracer:
    """
    Оптимизированная система трассировки лучей для проверки видимости.
    
    Использует алгоритм Брезенхэма для эффективного построения линий
    и проверки пересечений со стенами.
    """
    
    @staticmethod
    def bresenham_line(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
        """
        Генерирует точки линии между двумя точками используя алгоритм Брезенхэма.
        
        Args:
            start: Начальная точка (x, y)
            end: Конечная точка (x, y)
            
        Yields:
            Точки линии (x, y)
        """
        x0, y0 = start
        x1, y1 = end
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        
        # Определяем направление движения
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        
        err = dx - dy
        
        while True:
            yield (x0, y0)
            
            if x0 == x1 and y0 == y1:
                break
                
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
    
    @staticmethod
    def check_line_of_sight(start: Tuple[int, int], end: Tuple[int, int], 
                           level: List[str], shadow_coef: int) -> bool:
        """
        Проверяет видимость между двумя точками через карту уровня.
        
        Args:
            start: Начальная точка в координатах сетки теней
            end: Конечная точка в координатах сетки теней
            level: Карта уровня
            shadow_coef: Коэффициент масштабирования теней
            
        Returns:
            True если точки видимы друг другу
        """
        for x, y in RayTracer.bresenham_line(start, end):
            # Конвертируем координаты сетки теней в координаты уровня
            level_x = x // shadow_coef
            level_y = y // shadow_coef
            
            # Проверяем границы уровня
            if (level_y < 0 or level_y >= len(level) or 
                level_x < 0 or level_x >= len(level[0])):
                continue
                
            # Проверяем, не является ли клетка стеной
            if level[level_y][level_x] == '#':
                return False
                
        return True
    
    @staticmethod
    def get_visible_cells(player_pos: Tuple[int, int], radius: int, 
                         level: List[str], shadow_coef: int) -> set:
        """
        Возвращает множество видимых клеток в заданном радиусе от игрока.
        
        Args:
            player_pos: Позиция игрока в координатах сетки теней
            radius: Радиус видимости
            level: Карта уровня
            shadow_coef: Коэффициент масштабирования теней
            
        Returns:
            Множество видимых клеток (x, y)
        """
        visible_cells = set()
        px, py = player_pos
        
        # Проверяем все клетки в радиусе
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                # Проверяем, что клетка в радиусе
                if dx * dx + dy * dy <= radius * radius:
                    cell_x = px + dx
                    cell_y = py + dy
                    
                    # Проверяем видимость
                    if RayTracer.check_line_of_sight(
                        (px, py), (cell_x, cell_y), level, shadow_coef
                    ):
                        visible_cells.add((cell_x, cell_y))
                        
        return visible_cells 