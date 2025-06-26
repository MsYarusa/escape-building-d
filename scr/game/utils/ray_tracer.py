from typing import List, Tuple, Set


class RayTracer:
    """
    Оптимизированная система поля зрения (Field of View), использующая
    алгоритм Recursive Shadowcasting.

    Эта версия исправляет артефакты "протекания света" через стены.
    """
    _OCTANT_TRANSFORMS = [
        (1, 0, 0, 1), (0, 1, 1, 0), (0, -1, 1, 0), (-1, 0, 0, 1),
        (-1, 0, 0, -1), (0, -1, -1, 0), (0, 1, -1, 0), (1, 0, 0, -1)
    ]

    @staticmethod
    def get_visible_cells(player_pos: Tuple[int, int], radius: int,
                          level: List[str], shadow_coef: int) -> Set[Tuple[int, int]]:
        """
        Возвращает множество видимых клеток в заданном радиусе от игрока.
        """
        px, py = player_pos
        visible_cells = {(px, py)}
        radius_sq = radius * radius

        for transform in RayTracer._OCTANT_TRANSFORMS:
            RayTracer._scan_octant(
                player_pos, radius_sq, 1, 1.0, 0.0, transform,
                visible_cells, level, shadow_coef
            )

        return visible_cells

    @staticmethod
    def _is_wall(x: int, y: int, level: List[str], shadow_coef: int) -> bool:
        """Проверяет, является ли клетка на сетке теней стеной на карте уровня."""
        level_x = x // shadow_coef
        level_y = y // shadow_coef

        if not (0 <= level_y < len(level) and 0 <= level_x < len(level[0])):
            return True
        return level[level_y][level_x] == '#'

    @staticmethod
    def _scan_octant(player_pos: Tuple[int, int], radius_sq: int, depth: int,
                     start_slope: float, end_slope: float,
                     transform: Tuple[int, int, int, int],
                     visible_cells: Set[Tuple[int, int]],
                     level: List[str], shadow_coef: int):
        """
        Рекурсивно сканирует один октант. ИСПРАВЛЕННАЯ ВЕРСИЯ.
        """
        px, py = player_pos
        xx, xy, yx, yy = transform

        if start_slope < end_slope:
            return

        for i in range(depth, int(radius_sq ** 0.5) + 1):
            prev_is_wall = None

            # Определяем диапазон для сканирования на основе наклонов
            min_dy = round(i * end_slope)
            max_dy = round(i * start_slope)

            for j in range(max_dy, min_dy - 1, -1):
                # Трансформируем локальные координаты октанта в глобальные
                x = px + i * xx + j * xy
                y = py + i * yx + j * yy

                # Проверяем, что клетка в пределах круга
                if (x - px) ** 2 + (y - py) ** 2 > radius_sq:
                    continue

                # Добавляем видимую клетку
                visible_cells.add((x, y))

                is_wall = RayTracer._is_wall(x, y, level, shadow_coef)

                # Логика отбрасывания тени и рекурсии
                if prev_is_wall is not None:
                    # Если мы перешли из света в тень (нашли стену)
                    if is_wall and not prev_is_wall:
                        # Запускаем новый скан для области, которая теперь в тени
                        new_end_slope = (j + 0.5) / (i - 0.5)
                        RayTracer._scan_octant(
                            player_pos, radius_sq, i + 1, start_slope, new_end_slope,
                            transform, visible_cells, level, shadow_coef
                        )
                    # Если мы перешли из тени в свет (стена закончилась)
                    elif not is_wall and prev_is_wall:
                        # Обновляем start_slope для продолжения сканирования в текущей "светлой" области
                        start_slope = (j + 0.5) / (i + 0.5)

                prev_is_wall = is_wall

            # Если вся колонка была стеной, то дальше нет смысла сканировать в этом конусе
            if prev_is_wall:
                break

    # --- Старые методы, оставлены для обратной совместимости или других нужд ---
    @staticmethod
    def bresenham_line(start: Tuple[int, int], end: Tuple[int, int]):
        x0, y0 = start
        x1, y1 = end
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx, sy = 1 if x0 < x1 else -1, 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            yield (x0, y0)
            if x0 == x1 and y0 == y1: break
            e2 = 2 * err
            if e2 > -dy: err -= dy; x0 += sx
            if e2 < dx: err += dx; y0 += sy

    @staticmethod
    def check_line_of_sight(start: Tuple[int, int], end: Tuple[int, int],
                            level: List[str], shadow_coef: int) -> bool:
        for x, y in RayTracer.bresenham_line(start, end):
            if RayTracer._is_wall(x, y, level, shadow_coef):
                return False
        return True
