<template>
    <el-container class="home-container">
        <el-header>toubu</el-header>
        <el-container>
             <el-aside width="130px">
                <el-menu >
                    <el-submenu :index='menu1.path' v-for="menu1 in menuList">
                        <template slot='title'>
                            <span>{{menu1.name}}</span>
                        </template>
                        <el-menu-item :index="menu2.path" v-for="menu2 in menu1.children">
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
      msg: 'Welcome to Your Vue.js App',
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
            this.$message.success('12341234')
            this.menuList = res.data.menu
          })
          .catch(err => {
            this.$message.error('getMenuError'+err.message)
          })
    },
    getData(){}
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
</style>
