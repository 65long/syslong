<template>
  <div class="login_div">
  <div class="login">
    <div class="head-icon">
        <img src="../assets/logo.png" alt="">
    </div>
    <el-form ref='loginForm' :model='loginForm' :rules="loginRules" label-width='0px' class='login-form'>
        <el-form-item prop="username">
            <el-input v-model='loginForm.username' placeholder='username'>
            </el-input>
        </el-form-item>

        <el-form-item prop="password">
            <el-input v-model='loginForm.password' placeholder='password' type='password'></el-input>
        </el-form-item>

        <el-form-item class='login-btn'>
            <el-button type='primary' @click='login'>登录</el-button>
            <el-button type='info' @click="resetLoginForm">重置</el-button>
        </el-form-item>
    </el-form>
  </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
          username: [
            { required: true, message: '请输入用户名', trigger: 'blur' },
            { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'blur' },
            { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
          ]
      }
    }
  },
  methods: {
    login(){
     this.$axios.post('/rbac/login', this.loginForm)
       .then(res => {
          this.$message.success('login success');
          window.sessionStorage.setItem('token', res.data.token);
          this.$router.push({name: 'home'})
       })
       .catch(err => {
          this.$message.error('login failed---'+ err.message)
       })
    },
    resetLoginForm(){
      this.loginForm.username = '';
      this.loginForm.password = '';
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less" scoped>
.login_div{
  height: 100%;
  background-color: #2b4b6b;
}
.login {
  background-color: #fff;
  height: 300px;
  width: 450px;
  position: absolute;
  margin: 0;
  border-radius: 5px;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  .head-icon {
        height: 130px;
        width: 130px;
        border: 1px solid #eee;
        left: 50%;
        border-radius: 50%;
        position: absolute;
        transform: translate(-50%, -50%);
        img {
         height: 100%;
         width: 100%;
         border-radius: 50%;
         background-color: #eee;
        }
    }
}
.login-btn {
    display: flex;
    justify-content: flex-end;
}
.login-form {
   position: absolute;
   bottom: 0;
   width: 100%;
   padding: 0 20px;
   box-sizing: border-box;
}
</style>
