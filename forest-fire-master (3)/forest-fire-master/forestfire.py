from vpython import scene, rate, vector, color, box, cone, cylinder, sphere, local_light
import random

# ================== کلاس‌های درخت ==================
class Tree:
    def __init__(self, burning=False, wetness=1.0, xpos=0, ypos=0):
        self.burning = burning
        self.wetness = wetness
        self.xpos = xpos
        self.ypos = ypos
        self.model_parts = []

    def changeBurning(self, burning=True):
        self.burning = burning
        for part in self.model_parts:
            part.color = color.red if burning else part.initial_color

class Oak(Tree):
    def __init__(self, burning=False, wetness=1.0, xpos=0, ypos=0):
        super().__init__(burning, wetness, xpos, ypos)
        self.probCatch = 0.45 / wetness

    def create_tree(self):
        h_trunk = random.uniform(0.5, 0.8)
        trunk = cylinder(pos=vector(self.xpos, 0, self.ypos), axis=vector(0, h_trunk, 0),
                         radius=0.1, color=vector(0.55,0.27,0.07))
        trunk.initial_color = trunk.color
        self.model_parts.append(trunk)
        h_canopy = random.uniform(0.3, 0.5)
        canopy = sphere(pos=vector(self.xpos, h_trunk + h_canopy/2, self.ypos),
                        radius=h_canopy, color=vector(0,0.6,0))
        canopy.initial_color = canopy.color
        self.model_parts.append(canopy)

class Pine(Tree):
    def __init__(self, burning=False, wetness=1.0, xpos=0, ypos=0):
        super().__init__(burning, wetness, xpos, ypos)
        self.probCatch = 0.95 / wetness

    def create_tree(self):
        h_trunk = random.uniform(0.6, 1.0)
        trunk = cylinder(pos=vector(self.xpos, 0, self.ypos), axis=vector(0, h_trunk, 0),
                         radius=0.08, color=vector(0.55,0.27,0.07))
        trunk.initial_color = trunk.color
        self.model_parts.append(trunk)
        layers = random.randint(2,3)
        for i in range(layers):
            cone_height = 0.25 - i*0.05
            cone_radius = 0.3 - i*0.05
            crown = cone(pos=vector(self.xpos, h_trunk + i*0.1, self.ypos),
                         axis=vector(0, cone_height, 0),
                         radius=cone_radius, color=vector(0,0.6,0))
            crown.initial_color = crown.color
            self.model_parts.append(crown)

# ================== کلاس جنگل ==================
class Forest:
    def __init__(self):
        self.forestList = []

    def prompts(self):
        density = float(input('Tree density (0.1 - 1): '))
        percentPine = float(input('Percent pine (0 - 1): '))
        wetness = float(input('Wetness (1=dry, 3=wet): '))
        return density, percentPine, wetness

    def initialize_forest_list(self, density, percentPine, wetness):
        self.forestList = []
        for i in range(30):
            for j in range(30):
                if random.random() <= density:
                    if random.random() <= percentPine:
                        tree = Pine(False, wetness, j, i)
                    else:
                        tree = Oak(False, wetness, j, i)
                    tree.create_tree()
                    self.forestList.append(tree)
                else:
                    self.forestList.append(None)

    def check_for_fire(self):
        burning_now = [obj for obj in self.forestList if obj and obj.burning]
        new_burning = []
        for obj in self.forestList:
            if obj and not obj.burning:
                for other in burning_now:
                    if abs(obj.xpos - other.xpos) <= 1 and abs(obj.ypos - other.ypos) <= 1:
                        if random.random() < obj.probCatch:
                            new_burning.append(obj)
                            break
        for obj in new_burning:
            obj.changeBurning(True)

# ================== تابع اصلی ==================
def main():
    f = Forest()
    density, percentPine, wetness = f.prompts()
    f.initialize_forest_list(density, percentPine, wetness)

    scene.title = "Forest Fire Simulation"
    scene.width = 900
    scene.height = 600
    scene.background = vector(0.5,0.8,1)
    scene.userspin = True
    scene.userzoom = True
    scene.center = vector(15,0,15)

    ground = box(pos=vector(15,0,15), size=vector(30,0.1,30), color=vector(0.3,0.6,0.3))

    # خورشید بالاتر و کمی پشت جنگل
    sun = sphere(pos=vector(-5,8,40), radius=3, color=vector(1,0.8,0.2), emissive=True)
    sun_light = local_light(pos=sun.pos, color=vector(1,0.9,0.7))

    # ابرهای طبیعی‌تر (چند کره کوچک روی هم)
    for _ in range(5):
        base_x = random.uniform(0,30)
        base_y = random.uniform(6,10)
        base_z = random.uniform(0,30)
        num_spheres = random.randint(3,5)
        for _ in range(num_spheres):
            offset = vector(random.uniform(-1,1), random.uniform(-0.3,0.3), random.uniform(-1,1))
            r = random.uniform(1.0,1.8)
            sphere(pos=vector(base_x,base_y,base_z)+offset, radius=r,
                   color=color.white, opacity=0.6)

    print("Click on a tree to ignite it!")

    def on_click(evt):
        obj = scene.mouse.pick
        if obj:
            for tree in f.forestList:
                if tree:
                    if obj in tree.model_parts:
                        tree.changeBurning(True)
                        f.check_for_fire()

    scene.bind("click", on_click)

    while True:
        rate(5)
        f.check_for_fire()

if __name__ == "__main__":
    main()
