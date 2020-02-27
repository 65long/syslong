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
        <!--数据表格区域-->
        <el-table
          :data="userList"
          style="width: 100%"
          stripe border>
          <el-table-column type="index"></el-table-column>

          <el-table-column prop="username" label="姓名" width="100"></el-table-column>
          <el-table-column prop="nickname" label="昵称" width="100"></el-table-column>
          <el-table-column prop="mobile" label="手机号" width="300"></el-table-column>

          <el-table-column label="操作">
            <template slot-scope="scope">
              <!--修改，删除，分配角色-->
              <el-button type="primary" icon="el-icon-edit" circle size="mini"></el-button>
              <el-button type="danger" icon="el-icon-delete" circle size="mini"></el-button>
              <!--分配角色，el-tooltip为文本提示按钮-->
              <el-tooltip class="item" effect="dark" content="分配角色" placement="top" :enterable="false">
                <el-button type="primary" icon="el-icon-setting" circle size="mini"></el-button>
              </el-tooltip>
            </template>
          </el-table-column>

        </el-table>
      </el-card>
    </div>
</template>

<script>
    export default {
        name: "Users",
        data(){
          return {
            userList: [],
            queryInfo: {
              keyword: '',
              page: 1,
              size: 10,
            }
          }
        },
        created(){
          this.getUserList();
        },
        methods:{
          getUserList(){
            this.$axios.get('rbac/users', {param: this.queryInfo})
            .then(res => {
              // this.$message.success('12341234');
              this.userList = res.data;
            })
            .catch(err => {
              this.$message.error('getUserList'+ err.message)
            })
          }
        }

    }
</script>

<style lang="less" scoped>

</style>
