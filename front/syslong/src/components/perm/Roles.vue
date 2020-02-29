<template>
  <div>
    <!--面包屑导航区与-->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item><a href="/roles">角色管理</a></el-breadcrumb-item>
      <el-breadcrumb-item>角色列表</el-breadcrumb-item>
    </el-breadcrumb>
    <!--看卡片试图-->
    <el-card>
      123
    </el-card>
  </div>
</template>

<script>
    export default {
        name: "Roles"
    }
</script>

<style scoped>

</style>
