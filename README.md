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

获取`sessionid`后才能进行后续操作

### 获取服务器信息

`GET /get_server_info/`

请求头：无要求

响应：

```json
{
    "Code": 0,
    "Message": "",
    "Data": {
            "cpu_percent": 50,
            "virtual_memory_percent": 50
        }
}
```