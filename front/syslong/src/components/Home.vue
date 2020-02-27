<template>
    <el-container class="home-container">
        <el-header>
          <div class="header-head">
            <img src="../assets/logo.png" alt="">
            <span>后台管理系统</span>
          </div>
          <el-button type="info" @click="logout">登出</el-button>
        </el-header>
        <el-container>
             <el-aside :width="aside_closed ? '20px': '200px'">
                <div @click="fold_aside" class="fold-button">||||</div>
                <el-menu background-color="#333744" text-color="#fff"
                         :collapse="aside_closed" :collapse-transition="false" active-text-color="#409EFF">
                    <el-submenu :index='menu1.path' v-for="menu1 in menuList" :key="menu1.path">
                        <template slot='title'>
                            <span>{{menu1.name}}</span>
                        </template>
                        <el-menu-item :index="menu2.path" v-for="menu2 in menu1.children" :key="menu2.path">
                            <template>
                                <span>{{menu2.name}}</span>
                            </template>
                        </el-menu-item>
                    </el-submenu>
                </el-menu>
             </el-aside>
             <el-main>
                <div v-for="item in menuList">
                  <p>{{item}}</p>
               </div>
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
      menuList: []
    }
  },
  created(){
    this.getMenu()
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
</style>
