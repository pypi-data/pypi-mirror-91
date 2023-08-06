# Rainbond Python

Rainbond python cloud native development base library.

## Instructions

```python
rainbond -c demo-component
```

### Parameter

处理请求与响应参数的通用类

```python
from rainbond_python.parameter import Parameter
```

#### 获取请求参数

通过 `Parameter` 类实例，可以获取以下信息：

- parameter.method: 请求类型
- parameter.headers: 请求头
- parameter.param_url: URL中传递的参数
- parameter.param_json: Json请求中的参数
- parameter.param_form: 表单请求中的参数

所有信息均为字典类型，通过 `json.dumps()` 可以直接作为响应返回：

```python
@app.route('/api/1.0/demo', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_demo():
    parameter = Parameter(request)
    if parameter.method == 'GET':
        return json.dumps(parameter.param_url, ensure_ascii=False), 200, []
    elif parameter.method == 'POST':
        return json.dumps(parameter.param_json, ensure_ascii=False), 200, []
    elif parameter.method == 'PUT':
        return json.dumps(parameter.param_json, ensure_ascii=False), 200, []
    elif parameter.method == 'DELETE':
        return json.dumps(parameter.param_json, ensure_ascii=False), 200, []
```

#### 校验参数内容

通过 `Parameter` 类的 `verification()` 方法，可以判断参数字典是否符合要求：

```python
    elif parameter.method == 'POST':
        if parameter.verification(checking=parameter.param_json, verify={'name': str, 'age': int}):
            return '请求参数正确', 200, []
        else:
            return '请求参数错误', 400, []
```

其中 `checking` 参数是需要校验的参数字典，通常传递 `parameter.param_url`、`parameter.param_json` 或 `parameter.param_form`。第二个 `verify` 参数则是校验内容字典，需要指定 *参数名* 和 *参数类型* 作为字典项。

### DBConnect

```python
from rainbond_python.db_connect import DBConnect
db = DBConnect(db='db_name', collection='collection_name')
```

#### Write a docu

```python
insert_dict = {'name': 'Xiao Ming', 'age': 23}
if db.write_one_docu(docu=insert_dict):
    print('Insert success')
else:
    print('Insert failure')
```

#### Does docu exist

```python
examine_dict = {'name': 'Xiao Ming'}
if db.does_it_exist(docu=examine_dict):
    print('Docu already exists')
else:
    print('Docu does not exist')
```

#### Update docu

##### Modify the first

```python
find_dict = {'name': 'Xiao Ming'}
modify_dict = {'$set': {'name': 'Xiao Hong'}}
if db.update_docu(find_docu=find_dict, modify_docu=modify_dict):
    print('Update success')
else:
    print('Update failure')
```

##### Modify all

```python
find_dict = {'age': 23}
modify_dict = {'$set': {'name': '23 year old'}}
if db.update_docu(find_docu=find_dict, modify_docu=modify_dict, many=True):
    print('Update all success')
else:
    print('Update all failure')
```

## Reference

- [Restful API](https://www.runoob.com/w3cnote/restful-architecture.html) : Representational State Transfer
- [12 Factor](https://12factor.net/zh_cn/) : The twelve-factor app is a methodology for building software-as-a-service apps
- [RainBond](https://www.rainbond.com/docs/) : Cloud native and easy-to-use application management platform
