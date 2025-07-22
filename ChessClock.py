import time

class ChessClock:
    def __init__(self, total_time):
        self.white_time = total_time
        self.black_time = total_time
        self.last_update_time = time.time()
        self.active_player = 'white'  # or 'black'
        self.state_stack = []  # store (white_time, black_time, active_player)

    def update(self):
        now = time.time()
        elapsed = now - self.last_update_time
        if self.active_player == 'white':
            self.white_time -= elapsed
        else:
            self.black_time -= elapsed
        self.last_update_time = now

    def switch_player(self):
        self.update()
        self.active_player = 'black' if self.active_player == 'white' else 'white'
        self.last_update_time = time.time()

    def get_time(self):
        self.update()
        return self.white_time, self.black_time

    def format_time(self, seconds):
        minutes = int(seconds) // 60
        seconds = int(seconds) % 60
        return f"{minutes:02}:{seconds:02}"

    def is_time_up(self):
        self.update()
        if self.white_time <= 0:
            return 'white'
        elif self.black_time <= 0:
            return 'black'
        return None

    def save_state(self):
        # Save clock state before a move
        self.state_stack.append((
            self.white_time, self.black_time, self.active_player, self.last_update_time
        ))

    def undo(self):
        # Restore last saved clock state
        if self.state_stack:
            self.white_time, self.black_time, self.active_player, self.last_update_time = self.state_stack.pop()
