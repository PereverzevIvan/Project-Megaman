self.anim_count = 0
        self.rect = self.image.get_rect(x=x, y=y)
        self.return_to_enemy = False
        self.damage = dam
        self.x1, self.y1 = x1, y1
        self.distance = dis
        self.current_distance = 0
        ROLLING_CUTTER_S.play(-1)

    def animation(self):
        if self.anim_count > 27:
            self.anim_count = 0
        frame = self.anim_count // 7
        self.image = ROLLING_CUTTER_IMAGE[frame]

    def update(self):
        self.animation()
        if not self.return_to_enemy:
            if self.rect.x < self.x1:
                self.rect.x += 8
            elif self.rect.x > self.x1:
                self.rect.x -= 8
            if self.rect.y < self.y1:
                self.rect.y += 8
            elif self.rect.y > self.y1:
                self.rect.y -= 8
            if abs(self.rect.x - self.x1) <= 10:
                self.rect.x = self.x1
            if abs(self.rect.y - self.y1) <= 10:
                self.rect.y = self.y1
            self.current_distance += 3
            print(self.distance, self.current_distance)
            if (self.current_distance >= self.distance) or\
                    (self.rect.x == self.x1 and self.rect.y == self.y1):
                self.return_to_enemy = True
        else:
            x = [i.rect.x for i in BOSSES][0]
            y = [i.rect.y for i in BOSSES][0]
            if [i.hp for i in BOSSES][0] == 0:
                ROLLING_CUTTER_S.stop()
                self.kill()
            if self.rect.x < x:
                self.rect.x += 5
            elif self.rect.x > x:
                self.rect.x -= 5
            if self.rect.y < y:
                self.rect.y += 5
            elif self.rect.y > y:
                self.rect.y -= 5
        self.anim_count += 1