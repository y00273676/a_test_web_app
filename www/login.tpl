<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="renderer" content="webkit">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
  <link rel="stylesheet" href="{{  static_url('css/layui.css') }}"  media="all">
  <title>欢迎登陆雷客后台管理系统</title>
  <style type="text/css">
      .divForm{
          position: absolute;/*绝对定位*/
          width: 600px;
          height: 200px;
          
          text-align: center;/*(让div中的内容居中)*/
          top: 50%;
          left: 50%;
          margin-top: -200px;
          margin-left: -150px;
      }
  </style>
</head>
<body>
    <div class="divForm">
    <form id ="form1" class="layui-form layui-form-pane" action="/login" method="POST">
      <div class="layui-form-item">
        <div class="layui-input-inline">
          <h2>雷客后台管理系统</h2>
        </div>
      </div>
      <div class="layui-form-item">
        <label class="layui-form-label">用户名</label>
        <div class="layui-input-inline">
          <input type="text" name="uname" lay-verify="required" placeholder="请输入用户名" autocomplete="off" class="layui-input">
        </div>
      </div>
      <div class="layui-form-item">
        <label class="layui-form-label">密码</label>
        <div class="layui-input-inline">
          <input type="password" name="passwd" placeholder="请输入密码" autocomplete="off" class="layui-input">
        </div>
      </div>
      <div class="layui-form-item">
        <div class="layui-input-inline">
          <button class="layui-btn" id="btn1" type="submit">登陆</button>
        </div>
      </div>
    </form>
    </div>
<script src="{{ static_url('layui.js') }}" charset="utf-8"></script>
<!-- 注意：如果你直接复制所有代码到本地，上述js路径需要改成你本地的 -->
<script>
</script>
</body>
</html>
