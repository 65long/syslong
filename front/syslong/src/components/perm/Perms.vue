<template>
  <div>
    <!--面包屑导航区与-->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item><a href="/perms">权限管理</a></el-breadcrumb-item>
      <el-breadcrumb-item>我的权限列表</el-breadcrumb-item>
    </el-breadcrumb>
    <!--卡片试图-->
    <el-card>
      <el-table :data="permsList" border stripe>
        <el-table-column type="index"></el-table-column>
        <el-table-column label="权限名称" prop="name"></el-table-column>
        <el-table-column label="权限路径" prop="path"></el-table-column>
        <el-table-column label="权限等级" prop="level">
          <template slot-scope="scope">
            <el-tag type="success" v-if="scope.row.level ==='一级'">一级权限</el-tag>
            <el-tag type="info" v-if="scope.row.level === '二级'">二级权限</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

  </div>
</template>

<script>
    export default {
        name: "Perms",
      data(){
          return {
            permsList: [],
          }
      },
      created(){
          this.getPermsList()
      },
      methods: {
          getPermsList(){
            // 获取权限列表
            this.$axios.get('/rbac/permslist/')
              .then(res => {
                this.$message.success('获取权限列表成功');
                this.permsList = res.data;
              })
              .catch(err => {
                this.$message.error('获取权限列表失败')
              })
          }
      }
    }
</script>

<style scoped lang="less">

</style>
