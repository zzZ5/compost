# compost
堆肥网站源代码

## 状态码

### 主要

| 状态码 | 消息     |
| ------ | -------- |
| 100    | 成功     |
| 0      | 未知错误 |


### 账号

| 状态码 | 消息             |
| ------ | ---------------- |
| 101    | 找不到该账号     |
| 102    | 权限不足         |
| 103    | 该账号已在设备中 |
| 104    | 该账号不在设备中 |

### 设备

| 状态码 | 消息         |
| ------ | ------------ |
| 111    | 找不到该设备 |
| 112    | 该设备已存在 |

### 服务器

| 状态码 | 消息               |
| ------ | ------------------ |
| 121    | 服务器获取信息失败 |

### 上传数据

| 状态码 | 消息         |
| ------ | ------------ |
| 131    | 上传数据错误 |

### 获取数据

| 状态码 | 消息         |
| ------ | ------------ |
| 141    | 请求码错误   |
| 142    | 请求格式错误 |

## API

### 登陆

`POST /account/login/`

请求：

```json
{
    "csrftoken": "DbbPqGAIBHCGrKmyxQAs0maxevcpiB5xiqJ0OEiyGjC0nbOP5PuO5N8A8lJydK0e",
    "name": "",
    "password": ""
}
```

响应：

```json
{
    "Cookie": {
        "csrftoken": "DbbPqGAIBHCGrKmyxQAs0maxevcpiB5xiqJ0OEiyGjC0nbOP5PuO5N8A8lJydK0e",        
        "sessionid": ""
    }
}
```

获取`sessionid`后才能进行后续大部分操作

### 获取服务器信息

`GET /get_server_info/`

请求头：无要求

响应：

```json
{
    "Code": 200,
    "Message": "",
    "Data": {
            "cpu_percent": 50,
            "virtual_memory_percent": 50
        }
}
```

| 变量名                 | 类型   | 举例                 | 说明             |
| ---------------------- | ------ | -------------------- | ---------------- |
| Code                   | Int    | 200                  | 返回状态码       |
| Message                | String | "服务器获取信息失败" | 状态码说明信息   |
| cpu_percent            | Float  | 2.7                  | 服务器cpu使用率  |
| virtual_memory_percent | Float  | 28.2                 | 服务器内存使用率 |

### 上传数据

`GET /submit/`

请求：

```json
{
    "key": "",
    "value": 25.5,
    "descript": ""
}
```

| 变量名   | 类型   | 可选  | 举例              | 说明                     |
| -------- | ------ | ----- | ----------------- | ------------------------ |
| key      | String | false | "ExampleKey12345" | 你的15位设备key          |
| value    | Float  | false | 25.5              | 设备测得的数据           |
| descript | String | true  | "℃"               | 数据说明，一般为数据单位 |

响应：

```json
{
    "Code": 200,
    "Message": "",
    "RequestKey": ""
}
```

| 变量名     | 类型   | 举例              | 说明                        |
| ---------- | ------ | ----------------- | --------------------------- |
| Code       | Int    | 100               | 返回状态码                  |
| Message    | String | "上传成功"        | 状态码说明信息              |
| Requestkey | String | "ExampleKey12345" | 你上传数据时用的15位设备key |

### 修改设备信息

`GET /equipment/<id>/modify_equipment/`

请求：

```json
{
    "Cookie": {
        "sessionid": ""
    },
    "name": "test",
    "descript": "设备描述"
}
```

| 变量名   | 类型   | 可选  | 举例       | 说明                             |
| -------- | ------ | ----- | ---------- | -------------------------------- |
| id       | Int    | false | 1          | 设备id                           |
| name     | String | true  | "test"     | 新的设备名(需要账号有管理员权限) |
| descript | String | false | "设备描述" | 新的设备描述                     |

响应：

```json
{
    "Code": 0,
    "Message": "未知错误！"
}
```

### 添加设备到我的账号/删除我账号中的设备

`GET /add_equipment/`

请求：

```json
{
    "Cookie": {
        "sessionid": ""
    },
    "name":"test",
    "action": "add",
}
```

| 变量名 | 类型   | 可选  | 举例     | 说明                            |
| ------ | ------ | ----- | -------- | ------------------------------- |
| name   | String | false | "test"   | 从我的账号中 添加/删除 的设备名 |
| action | String | false | "remove" | add/remove 添加或者删除         |


响应：

```json
{
    "Code": 0,
    "Message": "未知错误！"
}
```