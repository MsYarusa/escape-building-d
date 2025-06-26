from typing import List, Tuple, Set


class RayTracer:
    """
    Оптимизированная система поля зрения (Field of View), использующая
    алгоритм Recursive Shadowcasting для расчета видимых ячеек.
    """
    # Трансформации для 8 октантов для сканирования на 360 градусов
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
            return True  # Считаем границы карты стенами для корректного отсечения
        return level[level_y][level_x] == '#'

    @staticmethod
    def _scan_octant(player_pos: Tuple[int, int], radius_sq: int, depth: int,
                     start_slope: float, end_slope: float,
                     transform: Tuple[int, int, int, int],
                     visible_cells: Set[Tuple[int, int]],
                     level: List[str], shadow_coef: int):
        """Рекурсивно сканирует один октант для определения видимых ячеек."""
        px, py = player_pos
        xx, xy, yx, yy = transform

        if start_slope < end_slope:
            return

        for i in range(depth, int(radius_sq ** 0.5) + 1):
            prev_is_wall = None
            min_dy = round(i * end_slope)
            max_dy = round(i * start_slope)

            for j in range(max_dy, min_dy - 1, -1):
                x = px + i * xx + j * xy
                y = py + i * yx + j * yy

                if (x - px) ** 2 + (y - py) ** 2 > radius_sq:
                    continue

                visible_cells.add((x, y))
                is_wall = RayTracer._is_wall(x, y, level, shadow_coef)

                if prev_is_wall is not None:
                    if is_wall and not prev_is_wall:
                        new_end_slope = (j + 0.5) / (i - 0.5)
                        RayTracer._scan_octant(
                            player_pos, radius_sq, i + 1, start_slope, new_end_slope,
                            transform, visible_cells, level, shadow_coef
                        )
                    elif not is_wall and prev_is_wall:
                        start_slope = (j + 0.5) / (i + 0.5)

                prev_is_wall = is_wall

            if prev_is_wall:
                break
