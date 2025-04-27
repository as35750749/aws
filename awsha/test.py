import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap

# 1. 建立漸層背景
fig, ax = plt.subplots(figsize=(12, 7))
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))
cmap = LinearSegmentedColormap.from_list('bg_grad', ['#0f2027','#203a43','#2c5364'])
ax.imshow(gradient, aspect='auto', cmap=cmap, extent=(0,1,0,1), zorder=0)

# 2. 定義圓角面板函式
def add_panel(x, y, w, h, facecolor, edgecolor):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.02,rounding_size=0.02",
                         linewidth=1.5, edgecolor=edgecolor,
                         facecolor=facecolor, zorder=2,
                         mutation_aspect=1)
    ax.add_patch(box)
    return box

# 3. 視頻播放器區域
add_panel(0.05, 0.3, 0.6, 0.65, facecolor='#000000', edgecolor='#00bcd4')
ax.text(0.35, 0.9, 'LIVE STREAM', color='#00bcd4',
        fontsize=18, fontweight='bold', ha='center', va='center', zorder=3)

# 4. 聊天區域
add_panel(0.68, 0.3, 0.27, 0.65, facecolor='#1a1a2e', edgecolor='#e91e63')
ax.text(0.815, 0.9, 'Chat Room', color='#e91e63',
        fontsize=18, fontweight='bold', ha='center', va='center', zorder=3)

# 5. 用戶資訊區域
add_panel(0.05, 0.05, 0.9, 0.2, facecolor='#1f1f3f', edgecolor='#ffeb3b')
ax.text(0.5, 0.15, 'User Info & Controls', color='#ffeb3b',
        fontsize=16, ha='center', va='center', zorder=3)

# 6. 隱藏座標軸並顯示
ax.axis('off')
plt.tight_layout()
plt.show()
