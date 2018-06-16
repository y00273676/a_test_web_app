{% extends 'index.tpl' %}
{% block head %}
  <meta name="renderer" content="webkit">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
{% end %}
{% block container %}
<blockquote class="layui-elem-quote layui-text">
 惊艳PLUS简版验证:上传文件中只需要上传mac地址 
</blockquote>
              
<fieldset class="layui-elem-field layui-field-title" style="margin-top: 20px;">
  <legend>添加需要激活的mac地址</legend>
</fieldset>
<form class="layui-form" action="">
  <div class="layui-form-item">
    <label class="layui-form-label">上传文件</label>
      <button type="button" class="layui-btn" id="upload3"><i class="layui-icon">&#xe67c;</i>文件</button>
  </div>
  <div class="layui-form-item">
    <label class="layui-form-label">单一MAC添加</label>
    <div class="layui-input-block">
      <input type="text" name="add_mac" lay-verify="title" autocomplete="off" class="layui-input">
    </div>
  </div>
  <div class="layui-form-item">
    <label class="layui-form-label">单一MAC删除</label>
    <div class="layui-input-block">
      <input type="text" name="del_mac" lay-verify="title" autocomplete="off" class="layui-input">
    </div>
  </div>
  <div class="layui-form-item">
    <div class="layui-input-block">
      <button class="layui-btn" lay-submit="" lay-filter="*">立即提交</button>
      <button type="reset" class="layui-btn layui-btn-primary">重置</button>
    </div>
  </div>
</form>
<fieldset class="layui-elem-field layui-field-title" style="margin-top: 20px;">
  <legend>添加需要套餐的设备</legend>
</fieldset>
<form class="layui-form" action="">
  <div class="layui-form-item">
    <label class="layui-form-label">设备mac地址</label>
    <div class="layui-input-block">
      <input type="text" name="mac" lay-verify="title" autocomplete="off" class="layui-input">
    </div>
  </div>
  <div class="layui-form-item">
    <label class="layui-form-label">套餐选择</label>
    <div class="layui-input-block">
      <select name="meal" lay-filter="aihao">
        <option value="0">三年免费下载</option>
        <option value="1">两年免费下载</option>
        <option value="2">一年免费下载</option>
      </select>
    </div>
  </div>
  <div class="layui-form-item">
    <div class="layui-input-block">
      <button class="layui-btn" lay-submit="" lay-filter="addmeal">立即提交</button>
      <button type="reset" class="layui-btn layui-btn-primary">重置</button>
    </div>
  </div>
</form>
<ins class="adsbygoogle" style="display:inline-block;width:970px;height:90px" data-ad-client="ca-pub-6111334333458862" data-ad-slot="3820120620"></ins>
  
{% end %}          
{% block footjs %}
<script>
layui.use(['form'], function(){
  var form = layui.form
  form.on('submit(*)', function(data){
  $.ajax({
          type: 'GET',
          url: '/jyauth/upload',
          dataType: 'json',
          data: data.field,//往后台发送的是data.field，即一个{name：value}的数据结构
          async: true,
          success: function (result) {
              if (result.code == 1) {
                  alert('操作成功');
              } else {
                  alert('操作失败');
              }
          },
        });
        return false;
  });
});

layui.use(['form'], function(){
  var form = layui.form
  form.on('submit(addmeal)', function(data){
  $.ajax({
          type: 'GET',
          url: '/jyauth/addmeal',
          dataType: 'json',
          data: data.field,//往后台发送的是data.field，即一个{name：value}的数据结构
          async: true,
          success: function (result) {
              if (result.code == 1) {
                  alert('操作成功');
              } else {
                  alert('操作失败(可能重复添加)');
              }
          },
        });
        return false;
  });
});
layui.use('upload', function(){
  var $ = layui.jquery
  ,upload = layui.upload;

  upload.render({ //允许上传的文件后缀
    elem: '#upload3'
    ,url: '/jyauth'
    ,accept: 'file' //普通文件
    ,exts: 'txt' //只允许上传txt文件
    ,done: function(ret){
        alert('上传成功')
    }
  });
});
</script>
{% end %}
