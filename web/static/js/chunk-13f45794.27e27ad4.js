(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-13f45794"],{"095e":function(t,e,a){"use strict";var s=a("465e"),r=a.n(s);r.a},"465e":function(t,e,a){},"92ef":function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"content-main"},[a("el-card",[a("el-row",{attrs:{gutter:20}},[a("el-col",{attrs:{span:8}},[a("el-row",{attrs:{span:3}},[t._v("我的头像")]),t._v(" "),a("el-row",{attrs:{span:21}},[a("div",{staticClass:"avatar-content"},[a("el-upload",{staticClass:"avatar-uploader",attrs:{"show-file-list":!1,action:t.uploadImgUrl,"before-upload":t.beforeAvatarUpload,"on-success":t.uploadSuccess,headers:t.headerObj,accept:"jpg,png"}},[t.avatar?a("img",{staticClass:"avatar",attrs:{src:t.avatar,title:"点击上传头像"}}):a("i",{staticClass:"el-icon-plus avatar-uploader-icon"}),t._v(" "),a("div",{staticClass:"el-upload__tip",attrs:{slot:"tip"},slot:"tip"},[t._v("只能上传jpg文件，且不超过200kb")])])],1)])],1),t._v(" "),a("el-col",{attrs:{span:16}},[a("el-row",{staticClass:"content-detail"},[a("el-col",{attrs:{span:8}},[t._v("昵称")]),t._v(" "),a("el-col",{attrs:{span:16}},[t._v(t._s(t.userInfo.nickname))])],1),t._v(" "),a("el-row",{staticClass:"content-detail"},[a("el-col",{attrs:{span:8}},[t._v("邮箱")]),t._v(" "),a("el-col",{attrs:{span:16}},[t._v(t._s(t.userInfo.email))])],1),t._v(" "),a("el-row",{staticClass:"content-detail"},[a("el-col",{attrs:{span:8}},[t._v("账号状态")]),t._v(" "),a("el-col",{attrs:{span:16}},[t._v("正常")])],1),t._v(" "),a("el-row",{staticClass:"content-detail"},[a("el-col",{attrs:{span:8}},[t._v("联系方式")]),t._v(" "),a("el-col",{attrs:{span:16}},[t._v(t._s(t.userInfo.mobile))])],1),t._v(" "),a("el-row",{staticClass:"content-detail"},[a("el-col",{attrs:{span:8}},[t._v("当前角色")]),t._v(" "),a("el-col",{attrs:{span:16}},[t._v(t._s(t.userInfo.role))])],1),t._v(" "),a("el-row",{staticClass:"content-detail"},[a("el-col",{attrs:{span:8}},[t._v("注册时间")]),t._v(" "),a("el-col",{attrs:{span:16}},[t._v(t._s(t.userInfo.date_joined))])],1),t._v(" "),a("el-row",{staticClass:"content-detail"},[a("el-col",{attrs:{span:8}},[t._v("上次登录")]),t._v(" "),a("el-col",{attrs:{span:16}},[t._v(t._s(t.userInfo.last_login))])],1)],1)],1)],1),t._v(" "),a("el-card",{staticClass:"box-card reset-pass",attrs:{shadow:"never"}},[a("el-row",{attrs:{gutter:20}},[a("el-col",{attrs:{span:3}},[a("el-button",{attrs:{type:"primary",size:"mini"},on:{click:t.showEditForm}},[t._v("修改密码")])],1),t._v(" "),a("el-col",{attrs:{span:3}},[a("el-checkbox",{on:{change:t.updateTagsConfig},model:{value:t.showTags,callback:function(e){t.showTags=e},expression:"showTags"}},[t._v("页签模式")])],1),t._v(" "),a("el-col",{attrs:{span:3}},[a("el-checkbox",{on:{change:t.updateAvatarConfig},model:{value:t.needShowAvatar,callback:function(e){t.needShowAvatar=e},expression:"needShowAvatar"}},[t._v("展示头像")])],1)],1)],1),t._v(" "),a("el-dialog",{attrs:{title:"修改密码",visible:t.editPwdVisible,width:"50%"},on:{"update:visible":function(e){t.editPwdVisible=e},close:t.resetChangePwdForm}},[a("el-form",{ref:"changePwdForm",attrs:{model:t.changePwdForm,rules:t.changePwdFormRules,size:"small","label-width":"88px"}},[a("el-form-item",{attrs:{label:"原密码",prop:"old_pwd"}},[a("el-input",{staticStyle:{width:"200px"},attrs:{type:"password","auto-complete":"on"},model:{value:t.changePwdForm.old_pwd,callback:function(e){t.$set(t.changePwdForm,"old_pwd",e)},expression:"changePwdForm.old_pwd"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"新密码",prop:"new_pwd"}},[a("el-input",{staticStyle:{width:"200px"},attrs:{type:"password","auto-complete":"on"},model:{value:t.changePwdForm.new_pwd,callback:function(e){t.$set(t.changePwdForm,"new_pwd",e)},expression:"changePwdForm.new_pwd"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"确认密码",prop:"repeat_pwd"}},[a("el-input",{staticStyle:{width:"200px"},attrs:{type:"password","auto-complete":"on"},nativeOn:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.submitEditPwd(e)}},model:{value:t.changePwdForm.repeat_pwd,callback:function(e){t.$set(t.changePwdForm,"repeat_pwd",e)},expression:"changePwdForm.repeat_pwd"}})],1)],1),t._v(" "),a("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(e){t.editPwdVisible=!1}}},[t._v("取 消")]),t._v(" "),a("el-button",{attrs:{type:"primary"},on:{click:t.submitEditPwd}},[t._v("确 定")])],1)],1)],1)},r=[],o=a("5f87"),n=a("c24f"),l={name:"Center",data:function(){var t=this,e=function(e,a,s){t.changePwdForm.new_pwd!==a?s(new Error("两次输入的密码不一致")):s()};return{showTags:this.$store.state.settings.tagsView,needShowAvatar:this.$store.state.settings.needShowAvatar,userInfo:Object(o["b"])(),uploadImgUrl:"http://127.0.0.1:8000/api/rbac/upload/user/headimg/",headerObj:{token:Object(o["a"])()},acceptType:"",editPwdVisible:!1,changePwdForm:{old_pwd:"",new_pwd:"",repeat_pwd:""},changePwdFormRules:{old_pwd:[{required:!0,message:"请输入密码",trigger:"blur"}],new_pwd:[{required:!0,message:"请输入新密码",trigger:"blur"},{min:6,max:20,message:"长度在 6 到 20 个字符",trigger:"blur"}],repeat_pwd:[{required:!0,validator:e,trigger:"blur"}]}}},computed:{avatar:function(){return this.$store.getters.avatar}},methods:{updateTagsConfig:function(t){this.$store.dispatch("settings/changeSetting",{key:"tagsView",value:t}),Object(o["g"])("tagsView",t)},updateAvatarConfig:function(t){this.$store.dispatch("settings/changeSetting",{key:"needShowAvatar",value:t}),Object(o["g"])("needShowAvatar",t)},resetChangePwdForm:function(){this.changePwdForm={}},submitEditPwd:function(){var t=this;this.$refs["changePwdForm"].validate((function(e){e?Object(n["b"])(t.changePwdForm).then((function(e){console.log(e),200===e.code?(t.$store.dispatch("user/logout",{},{root:!0}),t.$router.push({name:"center"})):t.$notify.error({title:"错误",message:e.message})})).catch((function(t){console.log(t)})):t.$notify.warning({title:"警告",message:"信息填写有误"})}))},showEditForm:function(){this.editPwdVisible=!this.editPwdVisible},uploadSuccess:function(t,e,a){this.$store.dispatch("user/changeAvatar",t.head_img,{root:!0})},beforeAvatarUpload:function(t){var e="image/jpeg"===t.type,a=t.size/1024/1024<.2;return e?a?e&&a:(this.$notify.error({title:"错误",message:"上传头像图片大小不能超过200kb!"}),a):(this.$notify.error({title:"错误",message:"上传头像图片只能是 JPG 格式!"}),e)}}},i=l,c=(a("095e"),a("2877")),d=Object(c["a"])(i,s,r,!1,null,"8b12ccd8",null);e["default"]=d.exports},c24f:function(t,e,a){"use strict";a.d(e,"a",(function(){return r})),a.d(e,"c",(function(){return o})),a.d(e,"d",(function(){return n})),a.d(e,"e",(function(){return l})),a.d(e,"b",(function(){return i}));var s=a("b775");function r(t){return Object(s["a"])({url:"/rbac/users/",method:"post",data:t})}function o(t){return Object(s["a"])({url:"/rbac/users/"+t+"/",method:"delete"})}function n(t,e){return Object(s["a"])({url:"/rbac/users/"+t+"/",method:"put",data:e})}function l(t){return Object(s["a"])({url:"/rbac/users/",method:"get",params:t})}function i(t){return Object(s["a"])({url:"/rbac/chagepwd/",method:"post",data:t})}}}]);