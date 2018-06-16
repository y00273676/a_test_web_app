<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
  <title>雷客后台管理</title>
  <link rel="stylesheet" href="{{ static_url('css/layui.css') }}">
  {% block headjs %}
  <script src="{{ static_url('layui.js') }}"></script>
  <script src="http://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
  {% end %}
  {% block head %}{% end %}
</head>
<body class="layui-layout-body">
<div class="layui-layout layui-layout-admin">
  <div class="layui-header">
    <div class="layui-logo">雷客后台管理系统</div>
    <!-- 头部区域（可配合layui已有的水平导航） -->
    <ul class="layui-nav layui-layout-left">
      <li class="layui-nav-item"><a href="">控制台</a></li>
      <li class="layui-nav-item"><a href="">用户</a></li>
      <li class="layui-nav-item">
        <a href="javascript:;">其它系统</a>
        <dl class="layui-nav-child">
          <dd><a href="">邮件管理</a></dd>
          <dd><a href="">消息管理</a></dd>
          <dd><a href="">授权管理</a></dd>
        </dl>
      </li>
    </ul>
    <ul class="layui-nav layui-layout-right">
      <li class="layui-nav-item">
        <a href="javascript:;">
          <img src="http://t.cn/RCzsdCq" class="layui-nav-img">
          {{ user }}
        </a>
        <dl class="layui-nav-child">
          <dd><a href="">基本资料</a></dd>
          <dd><a href="">安全设置</a></dd>
        </dl>
      </li>
      <li class="layui-nav-item"><a href="/logout">退了</a></li>
    </ul>
  </div>
  
  <div class="layui-side layui-bg-black">
    <div class="layui-side-scroll">
      <!-- 左侧导航区域（可配合layui已有的垂直导航） -->
      <ul class="layui-nav layui-nav-tree"  lay-filter="test">
        <li class="layui-nav-item">
          <a class="" href="javascript:;">榜单|推荐|分类</a>
          <dl class="layui-nav-child">
            <dd><a href="/rank">榜单</a></dd>
            <dd><a href="/push">推荐</a></dd>
            <dd><a href="/class">分类</a></dd>
          </dl>
        </li>
        <li class="layui-nav-item">
          <a href="javascript:;">数据库管理</a>
          <dl class="layui-nav-child">
            <dd><a href="/db/test">测试</a></dd>
            <dd><a href="/db/verify">发布</a></dd>
          </dl>
        </li>
        <li class="layui-nav-item">
          <a href="javascript:;">运营管理</a>
          <dl class="layui-nav-child">
            <dd><a href="/jyauth">惊艳简版验证</a></dd>
          </dl>
        </li>
        <li class="layui-nav-item"><a href="">产品数据</a></li>
      </ul>
    </div>
  </div>
  
  <div class="layui-body">
    <!-- 内容主体区域 -->
	<div style="padding: 15px;">
		{% block container %}
		{% end %}
	</div>
  </div>
  
  <div class="layui-footer">
    <!-- 底部固定区域 -->
    雷客后台管理系统 
  </div>
</div>
<script>
//JavaScript代码区域
  layui.use('element', function(){
    var element = layui.element;
  
  });
</script>
{% block footjs %}
{% end %}
</body>
</html>
