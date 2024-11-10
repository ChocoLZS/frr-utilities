from jinja2 import Environment, FileSystemLoader
import os

# 设置 Jinja2 环境
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.node.conf')

# 行和列的最大值
max_row = 5
max_col = 10

# 创建输出目录
output_dir = 'nodes'
os.makedirs(output_dir, exist_ok=True)

def node_to_ip(row, col):
    return (row - 1) * 10 + (col - 1)

# 生成配置文件
for row in range(1, max_row + 1):
    for col in range(1, max_col + 1):
        filename = f'node-{row}-{col}.conf'
        filepath = os.path.join(output_dir, filename)

        right = (col % max_col) + 1
        top = (row % max_row) + 1
        left = (col-2) % max_col + 1
        bottom = (row-2) % max_row + 1
        with open(filepath, 'w') as f:
            f.write(template.render(row=row, col=col, node_self=f"{node_to_ip(row, col)}",
                                    right=f"{node_to_ip(row, right)}" , top=f"{node_to_ip(top, col)}",
                                    bottom=f"{node_to_ip(bottom, col)}", left=f"{node_to_ip(row, left)}"))