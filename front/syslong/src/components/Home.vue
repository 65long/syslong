<template>
    <el-container class="home-container">
        <el-header>toubu</el-header>
        <el-container>
             <el-aside width="100px">cebian</el-aside>
             <el-main>you ce zhuti quyu</el-main>
        </el-container>
    </el-container>
</template>

<script>
export default {
  name: 'Home',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  methods: {
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
