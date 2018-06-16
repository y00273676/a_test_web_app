{% extends 'index.tpl' %}
{% block container %}
<fieldset class="layui-elem-field site-demo-button">
  <legend>{{ name }}</legend>
  <div class="layui-btn-group">
    {% if  name =="测试" %}
    <button class="layui-btn" onclick="window.location.href='/db/test_pub'">
    {% end %}
    {% if  name =="发布" %}
    <button class="layui-btn" onclick="window.location.href='/db/verify_pub'">
    {% end %}
     发布数据库 
    </button>
    <button class="layui-btn" onclick="window.location.href='/db/get_db'">
     下载数据库
    </button>
  </div>
</fieldset> 
<table class="layui-table">
  <thead>
    <tr>
      <th>ID</th>
      <th>版本号</th>
      <th>发布时间</th>
    </tr>
  </thead>
  <tbody>
    {% for item in items %}
    <tr>
      <td>{{ item["id"] }}</td>
      <td>{{ item['version'] }}</td>
      <td>{{ item['create_time'] }}</td>
    </tr>
    {% end %}
  </tbody>
</table>
{% end %}
