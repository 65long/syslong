<template>
    <div>
      <!--面包屑导航区与-->
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item><a href="/users">用户管理</a></el-breadcrumb-item>
          <el-breadcrumb-item>用户列表</el-breadcrumb-item>
        </el-breadcrumb>
      <!--卡片试图-->
      <el-card>
        <!--搜索与添加区域-->
        <el-row :gutter="20">
          <el-col :span="7">
              <el-input placeholder="请输入内容" v-model="queryInfo.keyword">
                <el-button slot="append" icon="el-icon-search" @click="searchData"></el-button>
              </el-input>
          </el-col>
          <el-col :span="3">
              <el-button type="primary" @click="addUser">新增用户</el-button>
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
        <!--分页功能-->
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="queryInfo.page"
          :page-sizes="[5, 10, 20, 50, 100]"
          :page-size="queryInfo.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total">
        </el-pagination>
      </el-card>

      <!--这是添加用户对话框-->
      <el-dialog
        title="添加用户"
        :visible.sync="addDialogVisible"
        @close="retForm"
        width="50%">
        <!--这是内容主题区-->
        <el-form ref='addUserForm' :model='addUserForm' :rules="addUserRules" label-width='70px'>
            <el-form-item prop="username" label="用户名">
                <el-input v-model='addUserForm.username' placeholder='请输入用户名'>
                </el-input>
            </el-form-item>

            <el-form-item prop="password" label="密码">
                <el-input v-model='addUserForm.password' placeholder='请输入密码' type='password'></el-input>
            </el-form-item>
            <el-form-item prop="email" label="E-mail">
                <el-input v-model='addUserForm.email' placeholder='请输入邮箱'></el-input>
            </el-form-item>
            <el-form-item prop="mobile" label="手机">
                <el-input v-model='addUserForm.mobile' placeholder='请输入手机'></el-input>
            </el-form-item>
        </el-form>
        <!--底部按钮区域-->
        <span slot="footer" class="dialog-footer">
          <el-button @click="addDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitAdd">确 定</el-button>
        </span>
      </el-dialog>
    </div>
</template>

<script>
    export default {
        name: "Users",
        data(){
          // 定影校验手机和邮箱
          var checkMobile = (rule, value, callback) => {
            const regMobile = /^1[34578]\d{9}$/
            // 验证手机号
            if(regMobile.test(value)){
              return callback()
            }
            callback('请输入合法的手机号')
          };
          var checkEmail = (rule, value, callback) => {
            const regEmail = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
            // 验证手机号
            if(regEmail.test(value)){
              return callback()
            }
            callback('请输入正确的邮箱')
          };
          return {
            userList: [],
            queryInfo: {
              keyword: '',
              page: 1,
              size: 5,
            },
            total: 0,
            // 控制添加用户对话框的显示与否
            addDialogVisible: false,
            // 添加用户的表单
            addUserForm:{
              username: '',
              password: '',
              email: '',
              mobile: '',
            },
            // 添加用户表单的验证规则
            addUserRules: {
              username: [
                {required: true, message: '请输入用户名', trigger: 'blur'},
                {min: 6, max: 20, message: '用户名长度在6-20个字符之间', trigger: 'blur'},
              ],
              password: [
                {required: true, message: '请输入密码', trigger: 'blur'},
                {min: 6, max: 20, message: '密码长度在6-20个字符之间', trigger: 'blur'},
              ],
              email: [
                // {required: false, message: '请输入邮箱', trigger: 'blur'},
                {validator: checkEmail, trigger: 'blur'}
              ],
              mobile: [
                // {required: false, message: '请输入手机', trigger: 'blur'},
                {validator: checkMobile, trigger: 'blur'}
              ],
            },
          }
        },
        created(){
          this.getUserList();
        },
        methods:{
          getUserList(){
            // 获取用户列表
            this.$axios.get('rbac/users/', {params: this.queryInfo})
            .then(res => {
              // this.$message.success('12341234');
              this.userList = res.data.data;
              this.total = res.data.total;
            })
            .catch(err => {
              this.$message.error('getUserList'+ err.message)
            })
          },
          // 处理每页数量改变
          handleSizeChange(newSize){
            this.queryInfo.size = newSize;
            this.getUserList();

          },
          // 处理当前页码改变
          handleCurrentChange(newPage){
            this.queryInfo.page = newPage;
            this.getUserList();
          },
          searchData(){
            //初始化查询条件
            this.queryInfo.page = 1;
            this.queryInfo.size = 5;
            this.getUserList();
          },
          //显示添加对话框
          addUser(){
            this.addDialogVisible = true;
          },
          // 关闭对话框之前
          retForm(){
            this.$refs.addUserForm.resetFields()
          },
          // 提交用户数据
          submitAdd(){
            // 提交前的预验证
            this.$refs.addUserForm.validate(valid => {
              if(!valid){
                // 与验证不合法
                this.$message.error('填写信息错误');
                return
              }else{
                //与验证合法
                this.$axios.post('/rbac/users/', this.addUserForm)
                  .then( res => {
                    this.$message.success('添加用户成功');
                    this.addDialogVisible = false;
                  })
                  .catch(err => {
                    this.$message.error('添加用户失败')
                  })
              }
            });
          }
        }

    }
</script>

<style lang="less" scoped>

</style>
