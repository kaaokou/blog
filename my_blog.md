
### blog显示问题

>1.使用markdown + Pygments

```Python
# 定义过滤器，将txt转为html
@app.template_filter('md')
    def markdown_to_html(txt):
        from markdown import markdown
        # extra支持```，codehilite 自动生成高亮属性
        return markdown(txt, ['extra', 'codehilite'])
```

##### 生成代码样式，放入前端css样式中
pygmentize -S default -f html -a .codehilite > code.css


##### 评论数显示

# 抬头，望天