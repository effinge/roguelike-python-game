from collections import deque
import random


class EnemyAI:
    @staticmethod
    def take_turn(enemy, state):
        if not enemy.is_alive():
            return ("dead",)

        player = state.player

        if EnemyAI.is_adjacent(enemy, player):
            damage = enemy.attack(player)
            return ("attack", damage)

        if EnemyAI.can_see_player(enemy, player, state):
            enemy.state = "chase"
            enemy.last_seen_player_pos = (player.x, player.y)

            moved = EnemyAI.move_to_target(enemy, state, player.x, player.y)
            if moved:
                return ("move", enemy.x, enemy.y, "chase")
            return ("blocked",)

        if enemy.state in ("chase", "search") and enemy.last_seen_player_pos is not None:
            enemy.state = "search"

            tx, ty = enemy.last_seen_player_pos
            moved = EnemyAI.move_to_target(enemy, state, tx, ty)

            if (enemy.x, enemy.y) == (tx, ty):
                enemy.last_seen_player_pos = None
                enemy.state = "idle"

            if moved:
                return ("move", enemy.x, enemy.y, "search")
            return ("blocked",)

        moved = EnemyAI.random_move(enemy, state)
        if moved:
            return ("move", enemy.x, enemy.y, "idle")

        return ("blocked",)

    @staticmethod
    def is_adjacent(enemy, player):
        dx = abs(enemy.x - player.x)
        dy = abs(enemy.y - player.y)
        return dx + dy == 1

    @staticmethod
    def can_see_player(enemy, player, state):
        dx = player.x - enemy.x
        dy = player.y - enemy.y
        radius = getattr(enemy, "vision_radius", 6)

        if dx * dx + dy * dy > radius * radius:
            return False

        return EnemyAI.has_line_of_sight(
            state.game_map,
            enemy.x,
            enemy.y,
            player.x,
            player.y
        )

    @staticmethod
    def has_line_of_sight(game_map, x0, y0, x1, y1):
        points = EnemyAI.get_line(x0, y0, x1, y1)

        # первую точку (сам враг) не проверяем, последнюю (игрок) тоже можно не блокировать
        for x, y in points[1:-1]:
            if game_map.tiles[x][y] == "#":
                return False

        return True

    @staticmethod
    def get_line(x0, y0, x1, y1):
        points = []

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1

        err = dx - dy

        x, y = x0, y0

        while True:
            points.append((x, y))
            if x == x1 and y == y1:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

        return points

    @staticmethod
    def move_to_target(enemy, state, target_x, target_y):
        blocked = set()

        for other in state.enemies:
            if other is enemy:
                continue
            if other.is_alive():
                blocked.add((other.x, other.y))

        next_step = EnemyAI.find_next_step(
            state.game_map,
            (enemy.x, enemy.y),
            (target_x, target_y),
            blocked
        )

        if next_step is None:
            return False

        enemy.x, enemy.y = next_step
        return True

    @staticmethod
    def find_next_step(game_map, start, goal, blocked_positions=None):
        if blocked_positions is None:
            blocked_positions = set()

        if start == goal:
            return start

        queue = deque([start])
        came_from = {start: None}
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            current = queue.popleft()

            if current == goal:
                break

            cx, cy = current

            for dx, dy in directions:
                nx = cx + dx
                ny = cy + dy
                nxt = (nx, ny)

                if nxt in came_from:
                    continue

                if not (0 <= nx < game_map.width and 0 <= ny < game_map.height):
                    continue

                if not game_map.is_walkable(nx, ny):
                    continue

                if nxt in blocked_positions and nxt != goal:
                    continue

                came_from[nxt] = current
                queue.append(nxt)

        if goal not in came_from:
            return None

        current = goal
        while came_from[current] is not None and came_from[current] != start:
            current = came_from[current]

        return current

    @staticmethod
    def random_move(enemy, state):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        if getattr(enemy, "ai_type", "default") == "goblin":
            random.shuffle(directions)
        else:
            # тролль менее хаотичен
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in directions:
            nx = enemy.x + dx
            ny = enemy.y + dy

            if not (0 <= nx < state.game_map.width and 0 <= ny < state.game_map.height):
                continue

            if not state.game_map.is_walkable(nx, ny):
                continue

            occupied = False
            for other in state.enemies:
                if other is enemy:
                    continue
                if other.is_alive() and other.x == nx and other.y == ny:
                    occupied = True
                    break

            if state.player.x == nx and state.player.y == ny:
                occupied = True

            if occupied:
                continue

            enemy.x = nx
            enemy.y = ny
            return True

        return False