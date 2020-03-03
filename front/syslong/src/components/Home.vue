<template>
    <el-container class="home-container">
        <el-header>
          <div class="header-head">
            <img src="../assets/logo.png" alt="">
            <span>后台管理系统</span>
          </div>
          <div class="header-loginstatus" v-if="active_user">
            <span >欢迎您 {{this.active_user}}</span>
            <el-button type="info" @click="logout" size="mini">登出</el-button>
          </div>
          <div class="header-loginstatus" v-else>
            <span ><router-link :to="{name: 'login'}">请登录</router-link></span>
          </div>


        </el-header>
        <el-container>
             <el-aside :width="aside_closed ? '40px': '200px'">
                <div @click="fold_aside" class="fold-button">||||</div>
                <!--router属性开启路由模式，跳向index属性绑定的值-->
                <!--unique-opened 保持只有一个子菜单开启-->
                <el-menu background-color="#373D41" text-color="#fff" router unique-opened
                         :collapse="aside_closed" :collapse-transition="false" active-text-color="#409EFF"
                         :default-active="active_path"
                >
                    <el-submenu :index='menu1.path' v-for="menu1 in menuList" :key="menu1.path">
                        <template slot='title'>
                            <span>{{menu1.name}}</span>
                        </template>
                        <el-menu-item :index="menu2.path" v-for="menu2 in menu1.children"
                                      :key="menu2.path" @click="saveActivePath(menu2.path)">
                            <template>
                                <span>{{menu2.name}}</span>
                            </template>
                        </el-menu-item>
                    </el-submenu>
                </el-menu>
             </el-aside>
             <el-main>
                <!--路由占位符,主题区域的-->
               <router-view></router-view>
             </el-main>
        </el-container>
    </el-container>
</template>

<script>
export default {
  name: 'Home',
  data () {
    return {
      aside_closed: false,
      active_path: '',
      active_user: '',
      menuList: []
    }
  },
  created(){
    this.getMenu();
    this.active_path = window.sessionStorage.getItem('active_path');
    this.active_user = window.sessionStorage.getItem('username')
  },
  methods: {
    getMenu(){
        this.$axios.get('rbac/menu')
          .then(res => {
            // this.$message.success('12341234');
            this.menuList = res.data.menu
          })
          .catch(err => {
            this.$message.error('getMenuError'+ err.message)
          })
    },
    //切换侧边菜单的折叠
    fold_aside(){
      this.aside_closed = !this.aside_closed;
    },
    logout(){
      window.sessionStorage.clear();
      this.$router.push({name: 'login'})
    },
    saveActivePath(active_path){
      // 保存当前的激活的位置，防止用户刷新丢失当前激活菜单
      window.sessionStorage.setItem('active_path', active_path)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less" scoped>
.home-container{
  height: 100%
}
.el-header{
  background-color: #373D41
}
.el-aside{
  background-color: #373D41
}
.el-main{
  background-color: #EAEDF1
}
.el-header{
    background-color: #373d41;
    display: flex;
    justify-content: space-between;
    padding-left: 0;
    align-items: center;
    color: #fff;
    font-size: 20px;
    div{
      display: flex;
      align-items: center;
      span{
        margin-left: 15px;
      }
      img {
        height: 60px;
        width: 60px;
        border-radius: 50%;
      }
    }
  }
  .fold-button{
    background-color: #1b6d85;
    font-size: 10px;
    color: #fff;
    line-height: 24px;
    text-align: center;
    cursor: pointer;
  }
  .header-loginstatus{
    font-size: 12px;
    color: #fffee8;
  }
</style>
