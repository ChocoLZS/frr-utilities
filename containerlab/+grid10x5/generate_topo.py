from jinja2 import Environment, FileSystemLoader

# 设置 Jinja2 环境
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.clab.yml')

# 渲染模板
output = template.render()

# 将渲染结果写入文件
with open('grid.clab.yml', 'w') as f:
    f.write(output)