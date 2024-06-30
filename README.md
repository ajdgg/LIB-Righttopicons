# LIB-Righttopicons
[有兽档案馆](https://youshou.wiki)用户页权限图标维护bot

## 配置

把.env.bot.dev复制为.env.bot，并修改里面的内容

如果邮箱配置部分如果没有配置，则不会发邮件

目前用于[Template:Right_topicons](https://youshou.wiki/wiki/Template:Right_topicons)

```
更改 main.py 中的

pattern = r"{{Right topicons\|用户=([^}]*)}}"

可以更换要匹配的模板
```
更改模板后如果权限名不同，要去```dara.json```修改

## 运行

```
python main.py
```

