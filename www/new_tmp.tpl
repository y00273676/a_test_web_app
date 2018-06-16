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
  <legend>添加文件</legend>
</fieldset>
<form id= "uploadForm1" class="layui-form">
  <div class="layui-form-item">
    <label class="layui-form-label">上传进度</label>
    <progress></progress>
    <p id="progress">0 bytes</p>
    <p id="info"></p>
  </div>
  <div class="layui-form-item">
    <label class="layui-form-label">上传图片压缩包</label>
      <div class="layui-input-inline">
      <input type="file" name="file" class="layui-input"></input>
      </div>
      <button type="button" class="layui-btn" id="upload1" onclick="doUpload1()"><i class="layui-icon">&#xe67c;</i>上传</button>
  </div>
</form>

<form id= "uploadForm2" class="layui-form">
  <div class="layui-form-item">
    <label class="layui-form-label">上传歌单文件</label>
      <div class="layui-input-inline">
      <input type="file" name="file" class="layui-input"></input>
      </div>
      <button type="button" class="layui-btn" id="upload2" onclick="doUpload2()"><i class="layui-icon">&#xe67c;</i>上传</button>
  </div>

   <div class="layui-form-item">
     <label class="layui-form-label">已上传文件</label>
       <div id='yasuo-div'>
       </div>
       <div id='zuobiao-div'>
       </div>
       <div id='gedan_tmp-div'>
       </div>
   </div>
</form>

<fieldset class="layui-elem-field layui-field-title" style="margin-top: 20px;">
  <legend>添加描述及产品选项</legend>
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
      <input type="text" name="title" lay-verify="required" autocomplete="off" placeholder="请填写标题" class="layui-input">
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

   {% if name == "推荐" %}
   <div class="layui-form-item">
    <label class="layui-form-label">歌单描述</label>
      <div id='gedan-div'>
      </div>
   </div>
   {% end %}

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

$('#yasuo-div').hide()
$('#zuobiao-div').hide()
$('#gedan_tmp-div').hide()

layui.use(['form'], function(){
  var form = layui.form
  form.on('submit(form1)', function(data){
    params = data.field;
    submit($,params);
    layer.msg(JSON.stringify(data.field));
    return false;
  });
  
});
    var totalSize = 0;
    //绑定所有type=file的元素的onchange事件的处理函数
    $(':file').change(function() {
        var file = this.files[0]; //假设file标签没打开multiple属性，那么只取第一个文件就行了
        name = file.name;
        size = file.size;
        type = file.type;
        url = window.URL.createObjectURL(file); //获取本地文件的url，如果是图片文件，可用于预览图片
        $(this).next().html("文件名：" + name + " 文件类型：" + type + " 文件大小：" + size + " url: " + url);
        totalSize += size;
        $("#info").html("总大小: " + totalSize + "bytes");
    });

var doUpload1 = function(){
     var formData = new FormData($( "#uploadForm1" )[0]);
     $.ajax({
          {% if name == "分类"%}
          url: '/class/upload',
          {% end %}
          {% if name == "推荐"%}
          url: '/push/upload',
          {% end %}
          {% if name == "榜单"%}
          url: '/rank/upload',
          {% end %}
          type: 'POST',
          data: formData,
          cache: false,
          contentType: false,
          processData: false,
          xhr: function(){ //获取ajaxSettings中的xhr对象，为它的upload属性绑定progress事件的处理函数
          myXhr = $.ajaxSettings.xhr();
          if(myXhr.upload){ //检查upload属性是否存在
          //绑定progress事件的回调函数
          myXhr.upload.addEventListener('progress',progressHandlingFunction, false);
          }
          return myXhr; //xhr对象返回给jQuery使用
          },
          success: function (data) {
              alert('上传成功');
              var name = data.name
              var go = `
                 <span class='layui-form-text'>${name}</span>
              `
              $('#yasuo-div').append(go)
              $('#yasuo-div').show()
          },
          error: function (data) {
              alert('上传失败');
          }
     });
}

var doUpload2 = function(){
     var formData = new FormData($( "#uploadForm2" )[0]);
     $.ajax({
          {% if name == "分类"%}
          url: '/class/upload',
          {% end %}
          {% if name == "推荐"%}
          url: '/push/upload',
          {% end %}
          {% if name == "榜单"%}
          url: '/rank/upload',
          {% end %}
          type: 'POST',
          data: formData,
          cache: false,
          contentType: false,
          processData: false,
          xhr: function(){ //获取ajaxSettings中的xhr对象，为它的upload属性绑定progress事件的处理函数
          myXhr = $.ajaxSettings.xhr();
          if(myXhr.upload){ //检查upload属性是否存在
          //绑定progress事件的回调函数
          myXhr.upload.addEventListener('progress',progressHandlingFunction, false);
          }
          return myXhr; //xhr对象返回给jQuery使用
          },
          success: function (data) {
              alert('上传成功');
              var name = data.name
              {% if name == "推荐" %}
	          console.log(name)
              var go = `
                  <div id='${name}-div'>
                      <div class="layui-form-item">
                        <label class="layui-form-label">${name}</label>
                        <div class="layui-input-block">
                          <input type="text" name="${name}"  autocomplete="off" placeholder="请添加描述格式:标题|描述" class="layui-input">
                        </div>
                      </div>
                  <div>
                  `
              $('#gedan-div').append(go)
              {% end %}
              {% if name != "推荐" %}
              var go = `
                 <span class='layui-form-text'>${name}</span>
              `
              $('#gedan_tmp-div').append(go)
              $('#gedan_tmp-div').show()
              {% end %}
          },
          error: function (data) {
              alert('上传失败');
          }
     });
}

function progressHandlingFunction(e) {
        if (e.lengthComputable) {
            $('progress').attr({value : e.loaded, max : e.total}); //更新数据到进度条
            var percent = e.loaded/e.total*100;
            $('#progress').html(e.loaded + "/" + e.total+" bytes. " + percent.toFixed(2) + "%");
        }
    }

</script>
{% end %}
