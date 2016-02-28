<h1 id="0"> API 手册 </h1>

## 目录

>[1.0 系统相关 ](#1.0)

>[2.0 任务相关 ](#2.0)

>[2.1 创建媒体分析任务 ](#2.1)

>[2.2 获取媒体分析状态信息 ](#2.2)


<h4 id="2.1">  2.1. 创建媒体分析任务 </h4>
<pre><code>
[POST] http://ip:port/api/mediaparse/create
{
    "url"   : "xxx",
    "name"  : "media name"
}
返回值：
{
    "result" : "success",               # "success" or "error"
    "message" : "create task ok.",      # string messages
    "task_id" : 25 
}

字段说明：
"url"   : 媒体文件的路径
</code></pre>


<h4 id="2.2">  2.2. 获取媒体分析状态信息 </h4>
<pre><code>
[GET] http://ip:port/api/mediaparse/status/{task_id}
返回值：
{
    "result" : "success",               # "success" or "error"

}

</code></pre>