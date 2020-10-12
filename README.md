## 如何使用Django-restfulwork框架来构建restful api

### 1.安装

> pip install rest_framework

安装完成后要在主settings.py里注册APP
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 子APP
    'loveword',
    # rest_framework框架其实也是一个子APP
    'rest_framework'
]
```


### 2.基本使用

**主urls.py模块：**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # home/为主URL，而include的作用是拼接APP目录下的urls.py文件中的path
    # 即此例的URL为：home/timer(必须按这种标准方法写URL)
    path('nmsl/', include("loveword.urls"))
]
```
<br>

**APP模块下的路由urls.py：**
```python
from django.urls import path
from . import views  # 导入views文件中的视图函数(标准写法)

urlpatterns = [
    path('demo/', views.demo, name='demo'),
    # 单函数路由写法
    path('detail/<int:pk>', views.detail, name='detail'),
    # class类作为路由
    path('news/', views.Info.as_view()),
    # rest-framework框架类作为路由
    path('drf/news/', views.DrfInfo.as_view())
]
```
<br>

**APP模块下的views.py：**

```python

```

### 实际问题

> Django models.save()的问题

Django views.py 引用models.py进行models.objects.create()然后进行.save的问题。我们获取前端携带的参数后是不能直接进行保存的，提交到数据库里面的。需要一个save方法

参考文章：https://blog.csdn.net/qq_40965177/article/details/83239634
<br>

> 关联表的必填on_delete参数的含义

从上面外键或一对多(ForeignKey)和一对一(OneToOneField)的参数中可以看出,都有on_delete参数,而 django 升级到2.0之后,表与表之间关联的时候,必须要写on_delete参数,否则会报异常。
参考文章：https://blog.csdn.net/buxianghejiu/article/details/79086011
<br>

> 默认db.sqlite3显示到pycharm右侧的Database栏来显示表数据

Django中数据库的建立步骤(models模块的使用)，比如MySQL：https://blog.csdn.net/zhangshuaijun123/article/details/84073927
参考文章：https://blog.csdn.net/qq_38945720/article/details/106032335

<br>

> Django默认请求头格式x-www-form-urlencoded

Django默认请求头格式：
```python
headers = {
    "Content-Type":"x-www-form-urlencoded"
}
```

**所以则可以存在问题：当别人的发送application/json或request payload等等数据格式时，我们Django就无法取到值**

**如何解决：** 由于我们无法通过request.POST来获取数据，但此时我们可以通过request.body或rest_framework框架自带的request.data方法

```python
# 方法一：request.body返回值是一个字节型
name = json.loads(request.body.decode('utf-8'))

# 方法二：rest_framework框架自带的request.data
name = request.data.name
```
