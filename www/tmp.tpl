{% extends 'index.tpl' %}
{% block container %}
<fieldset class="layui-elem-field site-demo-button">
  <legend>{{ name }}</legend>
  <div class="layui-btn-group">
    {% if  name =="分类" %}
    <button class="layui-btn" onclick="window.location.href='/class/add'">
    {% end %}
    {% if  name =="推荐" %}
    <button class="layui-btn" onclick="window.location.href='/push/add'">
    {% end %}
    {% if  name =="榜单" %}
    <button class="layui-btn" onclick="window.location.href='/rank/add'">
    {% end %}
      <i class="layui-icon">&#xe608;</i> 添加
    </button>
  </div>
</fieldset> 
<table class="layui-table">
  <thead>
    <tr>
      <th>ID</th>
      <th>名字</th>
      <th>描述</th>
      <th>产品</th>
      <th>输出设备</th>
      <th>版本号</th>
      <th>已发布</th>
      <th>操作</th>
    </tr>
  </thead>
  <tbody>
    {% for item in items %}
    <tr>
      <td>{{ item["id"] }}</td>
      <td>{{ item["name"] }}</td>
      <td>{{ item["describe"] }}</td>
      <td>{{ item['product'] }}</td>
      <td>{{ item['output'] }}</td>
      <td>{{ item['version'] }}</td>
      <td>{{ '是' if item['is_pub'] else '否' }}</td>
      <td>
         {% if item['is_pub']==0 %}
             {% if  name =="分类" %}
             <button class="layui-btn" id="btnedit" onclick="window.location.href='/class/edit'">编辑</button>
             <button class="layui-btn" id="btndel" onclick="window.location.href='/class/del?id={{ item['id'] }}'">删除</button>
             <button class="layui-btn" id="btnpub" onclick="window.location.href='/class/pub?product={{ item['product'] }}&output={{ item['output'] }}&version={{ item['version'] }}&id={{ item['id'] }}'">发布</button>
             {% end %}
             {% if  name =="推荐" %}
             <button class="layui-btn" id="btnedit" onclick="window.location.href='/class/edit'">编辑</button>
             <button class="layui-btn" id="btndel" onclick="window.location.href='/push/del?id={{ item['id'] }}'">删除</button>
             <button class="layui-btn" id="btnpub" onclick="window.location.href='/push/pub?product={{ item['product'] }}&output={{ item['output'] }}&version={{ item['version'] }}&id={{ item['id'] }}'">发布</button>
             {% end %}
             {% if  name =="榜单" %}
             <button class="layui-btn" id="btnedit" onclick="window.location.href='/class/edit'">编辑</button>
             <button class="layui-btn" id="btndel" onclick="window.location.href='/rank/del?id={{ item['id'] }}'">删除</button>
             <button class="layui-btn" id="btnpub" onclick="window.location.href='/rank/pub?product={{ item['product'] }}&output={{ item['output'] }}&version={{ item['version'] }}&id={{ item['id'] }}'">发布</button>
             {% end %}
         {% end %}
      </td>
    </tr>
    {% end %}
  </tbody>
</table>
{% end %}
