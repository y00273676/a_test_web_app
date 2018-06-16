{% extends 'index.tpl' %}
{% block head %}
  <meta name="renderer" content="webkit">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
{% end %}
{% block container %}
<blockquote class="layui-elem-quote layui-text">
 创建新版本分类提示：需要上传图片的压缩包、图片对应的坐标(json)、图片对应的歌曲(json) 
</blockquote>
              
<fieldset class="layui-elem-field layui-field-title" style="margin-top: 20px;">
  <legend>添加</legend>
</fieldset>
{% if name == "分类"%} 
<form class="layui-form" action="/class/add_tmp" method="post">
{% end %}
{% if name == "榜单"%} 
<form class="layui-form" action="/rank/add_tmp" method="post">
{% end %}
{% if name == "推荐"%} 
<form class="layui-form" action="/push/add_tmp" method="post">
{% end %}
  <div class="layui-form-item">
    <label class="layui-form-label">名字</label>
    <div class="layui-input-block">
      <input type="text" name="title" lay-verify="title" autocomplete="off" placeholder="格式:简体|繁体|英文" class="layui-input">
    </div>
  </div>
  
  <div class="layui-form-item">
    <label class="layui-form-label">产品选择框</label>
    <div class="layui-input-block">
      <select name="product" lay-filter="aihao">
        <option value=""></option>
        <option value="0">云十二PRO</option>
        <option value="1" selected="">惊艳PLUS</option>
        <option value="2">云十二PLUS</option>
      </select>
    </div>
  </div>
  
  <div class="layui-form-item">
    <label class="layui-form-label">输出选择框</label>
    <div class="layui-input-block">
      <select name="output" lay-filter="aihao">
        <option value=""></option>
        <option value="0">TV</option>
        <option value="1" selected="">VGA</option>
        <option value="2">IOS</option>
        <option value="3">ANDRIOD</option>
      </select>
    </div>
  </div>

  <div class="layui-form-item layui-form-text">
    <label class="layui-form-label">描述</label>
    <div class="layui-input-block">
      <textarea name= "desc"  placeholder="请输入内容" class="layui-textarea"></textarea>
    </div>
  </div>

  <div class="layui-form-item">
    <label class="layui-form-label">上传压缩包</label>
      <button type="button" class="layui-btn layui-btn-primary" id="upload1"><i class="layui-icon">&#xe67c;</i>图片压缩包</button><span id='yasuo' class=''></span>
      <br> 
    <label class="layui-form-label">上传坐标文件</label>
      <button type="button" class="layui-btn" id="upload2"><i class="layui-icon">&#xe67c;</i>坐标文件</button><span id='zuobiao' class=''></span>
      <br>
    <label class="layui-form-label">上传歌单文件</label>
      <button type="button" class="layui-btn" id="upload3"><i class="layui-icon">&#xe67c;</i>歌单文件</button>
      <div id='gedan-div'>
      </div>
  </div>

  <div class="layui-form-item">
    <div class="layui-input-block">
      <button class="layui-btn" lay-submit lay-filter="form1">立即提交</button>
      <button type="reset" class="layui-btn layui-btn-primary">重置</button>
    </div>
  </div>
</form>
 
<ins class="adsbygoogle" style="display:inline-block;width:970px;height:90px" data-ad-client="ca-pub-6111334333458862" data-ad-slot="3820120620"></ins>
  
{% end %}          
{% block footjs %}
<script>

$('#yasuo').hide()
$('#zuobiao').hide()

layui.use(['form'], function(){
  var form = layui.form
  form.on('submit(form1)', function(data){
    params = data.field;
    submit($,params);
    layer.msg(JSON.stringify(data.field));
    return false;
  });
  
});

layui.use('upload', function(){
  var $ = layui.jquery
  ,upload = layui.upload;

  upload.render({ //允许上传的文件后缀
    elem: '#upload3'
    {% if name == "分类"%}
    ,url: '/class/upload'
    {% end %}
    {% if name == "推荐"%}
    ,url: '/push/upload'
    {% end %}
    {% if name == "榜单"%}
    ,url: '/rank/upload'
    {% end %}
    ,accept: 'file' //普通文件
    ,exts: 'txt' //只允许上传txt文件
    ,done: function(ret){
        var name = ret.name
	    console.log(name)
        var go = `
            <div id='${name}-div'>
                <span id='${name}-span'>${name}</span><input name='${name}', class='' type='text'/>
            <div>
            `
        $('#gedan-div').append(go)
    }
  });

  upload.render({ //允许上传的文件后缀
    elem: '#upload2'
    {% if name == "分类"%}
    ,url: '/class/upload'
    {% end %}
    {% if name == "推荐"%}
    ,url: '/push/upload'
    {% end %}
    {% if name == "榜单"%}
    ,url: '/rank/upload'
    {% end %}
    ,accept: 'file' //普通文件
    ,exts: 'txt' //只允许上传txt文件
    ,done: function(ret){
        $('#zuobiao').html(ret.name)
        $('#zuobiao').show()
    }
  });

  upload.render({ //允许上传的文件后缀
    elem: '#upload1'
    {% if name == "分类"%}
    ,url: '/class/upload'
    {% end %}
    {% if name == "推荐"%}
    ,url: '/push/upload'
    {% end %}
    {% if name == "榜单"%}
    ,url: '/rank/upload'
    {% end %}
    ,accept: 'file' //普通文件
    ,exts: 'zip|rar|7z|tar|tgz' //只允许上传压缩文件
    ,done: function(ret){
        $('#yasuo').html(ret.name)
        $('#yasuo').show()
    }
  });
});
</script>
{% end %}
