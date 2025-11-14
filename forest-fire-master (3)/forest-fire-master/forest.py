import random
from tree import Oak, Pine

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
        """به‌روزرسانی وضعیت آتش با سرعت متغیر بر اساس رطوبت"""
        burning_now = [t for t in self.forestList if t and t.burning]
        candidates = []

        for tree in self.forestList:
            if tree and not tree.burning:
                for other in burning_now:
                    if abs(tree.xpos - other.xpos) <= 1 and abs(tree.ypos - other.ypos) <= 1:
                        if random.random() < tree.probCatch:
                            candidates.append(tree)
                            break

        # تعیین سرعت گسترش بر اساس رطوبت (با توجه به probCatch هر درخت)
        if candidates:
            max_new = 1
            # اگر خشک است، کمی بیشتر شعله‌ور شود
            if burning_now and any(t.wetness == 1 for t in burning_now):
                max_new = 2  # در رطوبت 1، دو درخت جدید در هر گام روشن می‌شوند

            random.shuffle(candidates)
            for tree in candidates[:max_new]:
                tree.changeBurning(True)
