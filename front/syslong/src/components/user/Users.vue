<template>
    <div>
      <!--面包屑导航区与-->
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/users' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item><a href="/">用户管理</a></el-breadcrumb-item>
          <el-breadcrumb-item>用户列表</el-breadcrumb-item>
        </el-breadcrumb>
      <!--卡片试图-->
      <el-card>
        <!--搜索与添加区域-->
        <el-row :gutter="20">
          <el-col :span="7">
              <el-input placeholder="请输入内容">
                <el-button slot="append" icon="el-icon-search"></el-button>
              </el-input>
          </el-col>
          <el-col :span="3">
              <el-button type="primary">新增用户</el-button>
          </el-col>
        </el-row>
      </el-card>
    </div>
</template>

<script>
    export default {
        name: "Users"
    }
</script>

<style lang="less" scoped>

</style>
