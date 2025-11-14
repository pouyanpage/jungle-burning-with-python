from vpython import cylinder, cone, sphere, vector, color
import random

class Tree:
    def __init__(self, burning=False, wetness=1.0, xpos=0, ypos=0):
        self.burning = burning
        self.wetness = wetness
        self.xpos = xpos
        self.ypos = ypos
        self.model_parts = []
        self.initial_colors = []
        self.probCatch = 0.5  # مقدار پایه → در زیر کلاس‌ها تنظیم می‌شود

    def changeBurning(self, burning=True):
        self.burning = burning
        for part, original_color in self.initial_colors:
            part.color = color.red if burning else original_color


class Oak(Tree):
    def __init__(self, burning=False, wetness=1.0, xpos=0, ypos=0):
        super().__init__(burning, wetness, xpos, ypos)
        self.probCatch = 0.45 / wetness

    def create_tree(self):
        # تنه تصادفی
        trunk_height = random.uniform(0.6, 1.0)
        trunk_radius = random.uniform(0.08, 0.12)

        trunk = cylinder(pos=vector(self.xpos, 0, self.ypos),
                         axis=vector(0, trunk_height, 0),
                         radius=trunk_radius, color=color.orange)
        trunk.tree_ref = self
        self.model_parts.append(trunk)
        self.initial_colors.append((trunk, trunk.color))

        # تاج کروی با تنوع
        canopy_radius = random.uniform(0.35, 0.55)
        canopy = sphere(pos=vector(self.xpos, trunk_height + canopy_radius * 0.4, self.ypos),
                        radius=canopy_radius, color=color.green)
        canopy.tree_ref = self
        self.model_parts.append(canopy)
        self.initial_colors.append((canopy, canopy.color))


class Pine(Tree):
    def __init__(self, burning=False, wetness=1.0, xpos=0, ypos=0):
        super().__init__(burning, wetness, xpos, ypos)
        self.probCatch = 0.95 / wetness

    def create_tree(self):
        # تنه تصادفی
        trunk_height = random.uniform(0.8, 1.4)
        trunk_radius = random.uniform(0.05, 0.09)

        trunk = cylinder(pos=vector(self.xpos, 0, self.ypos),
                         axis=vector(0, trunk_height, 0),
                         radius=trunk_radius, color=color.orange)
        trunk.tree_ref = self
        self.model_parts.append(trunk)
        self.initial_colors.append((trunk, trunk.color))

        # ۲ تا ۳ لایه مخروطی متنوع (شکل A)
        layers = random.randint(2, 4)
        for i in range(layers):
            height = random.uniform(0.25, 0.45) * (1 - i * 0.15)
            radius = random.uniform(0.25, 0.45) * (1 - i * 0.15)
            crown = cone(pos=vector(self.xpos, trunk_height + i * 0.25, self.ypos),
                         axis=vector(0, height, 0),
                         radius=radius, color=color.green)
            crown.tree_ref = self
            self.model_parts.append(crown)
            self.initial_colors.append((crown, crown.color))
